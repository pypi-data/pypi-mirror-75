from datetime import datetime as dt
import numpy as np
import pandas as pd
import warnings

from nptyping import NDArray, Float64
import ray
from tqdm.auto import tqdm

from ..helpers import accept_string_or_list, ProgressBar, numbafuncs as nbf
from .base import BaseStudy

class RayStudy(BaseStudy):
    def __init__(self, *args, **kwargs):
        use_ray = kwargs.pop('use_ray') if 'use_ray' in kwargs else True
        super().__init__(*args, **kwargs)
        self.use_ray = use_ray

        self.PBAR_CHECKPOINTS['ray'] = {
            'desc': 'Initialize ray', 
            'func': self._init_ray,
            'live': self._ray_conditions(),
        }

        if not self.use_ray:
            warnings.warn('{}{}{}'.format(
                'use_ray set to False. This is not recommended. ',
                'Ray provides significant performance improvements ',
                'and certain BaseStudy methods are not optimized.'
                ), stacklevel=3
            )

    @ProgressBar.wrap_make
    def make(self, *args, **kwargs):
        self._init_ray()
        super().make(*args, **kwargs)
        self._reset_checkpoint()

    def _reset_checkpoint(self):
        self.PBAR_CHECKPOINTS['ray']['live'] = self._ray_conditions()

    def _ray_conditions(self):
        return all([
            not ray.is_initialized(),
            self.use_ray
        ])

    def _init_ray(self):
        if self._ray_conditions():
            ray.init()

    @staticmethod
    def ray_iterator(obj_ids):
        while obj_ids:
            done, obj_ids = ray.wait(obj_ids)
            yield ray.get(done[0])

    @staticmethod
    @ray.remote
    def _region_changes(df, region_id, count_type, dates):
        df_reg = df[df.region_id == region_id][['date', count_type]]
        
        recount = np.array([])
        last_date = dates[-1]
        for date in dates:
            recount = RayStudy._change(df_reg, count_type, date, recount)
           
        no_negs = df_reg[df_reg.date > dates[-1]][count_type].values
        values = np.append(recount, no_negs)
        
        return {'region_id': region_id, 'count_type': count_type, 'values': values}
    
    @staticmethod
    def _change(df_reg, count_type, date, recount:NDArray[Float64]):
        """
        Redistribute negative values on a specific date back through the time-series
        
        This function addresses multiple negative counts in the time-series by carrying forward
        the recount of previous negatives. This is the `recount` variable.    
        
        `prechange` is the portion of the series that must be recalculated back to the date of the
        latest recalculation. If recount is empty, the start of preneg is the start of the whole series.
        i.e. recount.size == 0 and neglen == 0 
        
        `prechange` and `count_on_date` are passed to `redistribute_negatives`, which takes the count when
        the negative was experienced and multiplies by the distribution of prechange over the value the day prior
        
        This results in count_on_date shifting forward one time slot in the array, which is not ideal but
        maintains the shape of the series.
        
        After `redistribute_negatives` is called, the array is too short by one item. To fill it in, we look forward
        in the time series to the next value and linear interpolate from our last value to that next value
        (simply using mean). If the recount is occuring on the very last datapoint, then the last value 
        in recount is simply repeated.
        
        If there has already been a recount, `prechange` is filtered to remove that section of values, because the
        original dataframe still has the uncorrected values.
        
        recount is substituted into that section values via np.concatenate
        """
        df_pre = df_reg[df_reg.date < date]
        df_on = df_reg[df_reg.date == date]
        df_post = df_reg[df_reg.date > date]
        
        neglen = len(recount) if recount.size > 0 else 0        
        prechange = df_pre[count_type].values[neglen:]

        count_on_date = df_on[count_type].values[0]
        
        if recount.size != 0:
            prechange = np.concatenate([recount, prechange])
        
        recount = nbf.redistribute(prechange, count_on_date)

        if df_post[count_type].shape[0] >= 1:
            count_on_next = df_post[count_type].values[0]
            midpoint = np.array([np.mean(np.array([recount[-1], count_on_next]))])
        else:
            midpoint = recount[-1]
        return np.append(recount, midpoint)
            
    def _smoothing(self, df):
        if not self.use_ray:
            return super()._smoothing(df)
        else:
            regs_w_change = {}
            for count_type in self.COUNT_TYPES:
                filter_negs = df[count_type].diff() < 0
                filter_jan1 = (df.date != dt(2020,1,1))
                df_negs = df[filter_negs & filter_jan1][['region_id', 'region_name', 'date', count_type]]

                # Filters out count changes where the increase in count isn't at least 4x
                # larger than the increase the previous day
                filter_v_prior_new = ((df[count_type].diff() / df[count_type].diff().shift(1)) > 4)
                
                # Filters out jumps where the increse is no more than 25% and no less than .01% of total cumulative
                # this ensures that large jumps early in the pandemic are not redistributed
                # as large jumps were likely a true characteristic of the pandemic at that time
                filter_v_total = ((df[count_type].diff() / df[count_type]) < .25) \
                    & ((df[count_type].diff() / df[count_type]) > .01)
                df_jumps = df[filter_v_prior_new & filter_v_total][['region_id', 'region_name', 'date', count_type]]

                df_change = pd.concat([df_negs, df_jumps]).sort_values(by=['region_id', 'date'])
                
                for region_id in df_change.region_id.unique():
                    if region_id in regs_w_change:
                        regs_w_change[region_id] = {**regs_w_change[region_id], count_type: df_change[df_change.region_id==region_id].date.values}
                    else:
                        regs_w_change[region_id] = {count_type: df_change[df_change.region_id==region_id].date.values}
            
            dfid = ray.put(df)
            obj_ids = [RayStudy._region_changes.remote(dfid, region_id, count_type, dates) \
                for region_id, count_types in regs_w_change.items() \
                for count_type, dates in count_types.items()
            ]

            for smoothed in tqdm(RayStudy.ray_iterator(obj_ids), disable=not self.use_pbar, desc='changes', total=len(obj_ids), position=1, leave=False):
                df.loc[df.region_id == smoothed['region_id'], smoothed['count_type']] = smoothed['values']
            return df

    def _process_cols(self, df):
        if not self.use_ray:
            return super()._process_cols(df)
        else:
            complex_attrs = [
                'baseframe', 'regions', 
                '_init_ray', '_filter_regions', 
                '_agg_to_country_level', '_smoothing', '_raysmoothing',
                '_process_cols', 'PBAR_CHECKPOINTS',
                'compchart', 'compchart4d', 'heatmap', 'scatterflow', 'substrinscat',
                'barcharts', 'df',
            ]
            ray_kwargs = {k:v for k,v in self.__dict__.items() if k not in complex_attrs}
            
            dfid = ray.put(df)
            selfid = ray.put(ray_kwargs)

            groupids = [RayStudy._raywork.remote(region_id, dfid, selfid)
                for region_id 
                in df.region_id.unique()
            ]
            dfs = []
            pbar = tqdm(RayStudy.ray_iterator(groupids), disable=not self.use_pbar, total=len(groupids), position=1, leave=False)
            for df_group in pbar:
                dfs.append(df_group)

            return dfs

    @staticmethod
    @ray.remote
    def _raywork(region_id, df, kwargs):
        df_group = df[df.region_id == region_id].copy(deep=True)
        df_group = df_group.copy(deep=True)
        for count_type in RayStudy.COUNT_TYPES:
            if kwargs['interpolate']:
                df_group[count_type] = df_group[count_type].interpolate(**kwargs['interpolation_method'])

            df_group[count_type + '_new'] = nbf.diff(df_group[count_type].values)          
            df_group[count_type + '_dma'] = nbf.roll_mean(df_group[count_type].values, n=kwargs['count_dma'])
            df_group[count_type + '_new_dma'] = nbf.roll_mean(df_group[count_type + '_new'].values, n=kwargs['count_dma'])
            
        df_group['cases_per_test'] = nbf.div(df_group['cases'].values, df_group['tests'].values)
        df_group['tests_per_case'] = nbf.div(df_group['tests'].values, df_group['cases'].values)
        for append in RayStudy.COUNT_APPENDS:
            df_group['cases{}_per_test{}'.format(append, append)] = nbf.div(df_group['cases{}'.format(append)].values, df_group['tests{}'.format(append)].values)

        for count_cat in RayStudy.BASECOUNT_CATS:   
            df_group[count_cat + '_per_1K'] = nbf.div(df_group[count_cat].values, df_group['population'].values) * 1000
            df_group[count_cat + '_per_1M'] = nbf.div(df_group[count_cat].values, df_group['population'].values) * 1000000
            df_group[count_cat + '_per_person_per_land_KM2'] = nbf.div(df_group[count_cat].values, df_group['land_dens'].values)
            df_group[count_cat + '_per_person_per_city_KM2'] = nbf.div(df_group[count_cat].values, df_group['city_dens'].values)
        
        if kwargs['log']:
            with np.errstate(divide='ignore', invalid='ignore'):
                for cat in RayStudy.BASE_PLUS_PER_CATS:
                    df_group[cat + '_log'] = nbf.log10(df_group[cat].fillna(0).values)
        if kwargs['lognat']:
            with np.errstate(divide='ignore', invalid='ignore'):
                for cat in RayStudy.BASE_PLUS_PER_CATS:
                    df_group[cat + '_lognat'] = nbf.log(df_group[cat].fillna(0).values)
        
        for col in df_group.columns:
            if col not in RayStudy.CASE_COLS:
                df_group['growth_' + col] = nbf.growth(df_group[col].values)

        # Filter dataframe for count categories
        if kwargs['count_categories']:
            df_group = df_group[RayStudy.CASE_COLS + kwargs['count_categories'] + kwargs['factors']]

        # Forward fill any nans in the strindex categories. For some, the entire columns is nans, so fill those with 0s.
        if kwargs['strindex_factors']:
            df_group[kwargs['strindex_factors']] = df_group[kwargs['strindex_factors']].fillna(method='ffill')
            df_group[kwargs['strindex_factors']] = df_group[kwargs['strindex_factors']].fillna(0)

        # SUM certain strindex categories
        if all(cat in kwargs['factors'] for cat in RayStudy.CONTAIN_CATS):
            df_group['c_sum'] = nbf.sum_axis(df_group[RayStudy.CONTAIN_CATS].values)
        
        if all(cat in kwargs['factors'] for cat in RayStudy.ECON_CATS):
            df_group['e_sum'] = nbf.sum_axis(df_group[RayStudy.ECON_CATS].values)

        if all(cat in kwargs['factors'] for cat in RayStudy.HEALTH_CATS):
            df_group['h_sum'] = nbf.sum_axis(df_group[RayStudy.HEALTH_CATS].values)

        if all(cat in kwargs['factors'] for cat in RayStudy.KEY3_CATS):
            df_group['key3_sum'] = nbf.sum_axis(df_group[RayStudy.KEY3_CATS].values)

        if kwargs['favor_earlier']:
            for factor in kwargs['factors_to_favor_earlier']:
                df_group[factor + '_earlier'] = nbf.earlier_is_better(df_group[factor].values)
        
        # Adjust factors for percentage of population
        if kwargs['pop_cats']:
            for pop_cat in kwargs['pop_cats']:
                df_group[pop_cat + '_%'] = nbf.div(df_group[pop_cat].values, df_group['population'].values)
        
        # Unit conversions for chosen temperature scale
        if kwargs['temp_msmts']:
            for temp_msmt in kwargs['temp_msmts']:
                if kwargs['temp_scale'] == 'C':
                    df_group[temp_msmt] = df_group[temp_msmt].values - 273.15                            
                elif kwargs['temp_scale'] == 'F':
                    df_group[temp_msmt] = df_group[temp_msmt].values * 9 / 5 - 459.67

        
        if kwargs['factor_dmas']:
            for factor, dma in kwargs['factor_dmas'].items():
                df_group[factor + '_dma'] = nbf.roll_mean(df_group[factor].values, n=dma)
                df_group[factor + '_growth'] = nbf.growth(df_group[factor].values)                
                df_group[factor + '_growth_dma'] = nbf.roll_mean(df_group[factor + '_growth'].values, n=dma)
        
        if kwargs['mobis']:
            for mobi in kwargs['mobis']:
                df_group[mobi] = df_group[mobi].values / 100
                df_group[mobi + '_growth'] = df_group[mobi].values + 1
            for mobi, dma in kwargs['mobi_dmas'].items():
                df_group[mobi + '_growth_dma'] = nbf.roll_mean(df_group[mobi + '_growth'].values, n=dma)
                df_group[mobi + '_dma'] = df_group[mobi + '_growth_dma'].values - 1

        # Filter observations on the front end
        # If there are no observations that satisfy the hurdle
        # set df_group to empty 
        if kwargs['start_factor']:
            hurdle_index = df_group[df_group[kwargs['start_factor']] >= kwargs['start_hurdle']].index
            
            if hurdle_index.size >= 1:
                first_row = hurdle_index[0]
                df_group = df_group.loc[first_row:]
            else:
                df_group = pd.DataFrame()

        # Filter observations on the tailend
        if kwargs['tail_factor']:
            if (df_group[kwargs['tail_factor']] >= kwargs['tail_hurdle']).any():
                last_row = df_group[df_group[kwargs['tail_factor']] >= kwargs['tail_hurdle']].index[-1]
                df_group = df_group.loc[:last_row]
            else:
                df_group = pd.DataFrame()

        if not df_group.empty:
            # Indicates the number of days since the hurdle was met
            df_group['days'] = df_group['date'].values - df_group['date'].values[0]

        # If region data does not cover enough days, return empty Dataframe
        if len(df_group) < kwargs['min_days_from_start']:
            df_group = pd.DataFrame()
            
        return df_group

