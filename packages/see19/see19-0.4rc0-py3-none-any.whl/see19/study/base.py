import numpy as np
import pandas as pd
from datetime import datetime as dt
import warnings

from tqdm.auto import tqdm

from ..helpers import accept_string_or_list, ProgressBar, numbafuncs as nbf
from ..charts import CompChart2D, CompChart4D, HeatMap, BarCharts, ScatterFlow, SubStrindexScatter
from .. import constants

def set_constants(cls):
    cons = {k:v for k,v in constants.__dict__.items() if '__' not in k}
    for name, value in cons.items():
        setattr(cls, name, value)
    return cls

@set_constants
class BaseStudy:
    """
    Class for filtering the baseframe dataset, analysing, and generating graphs
    """

    def __init__(
        self, baseframe, count_dma=3, count_categories=[], factors=[], 
        regions=[], countries=[], excluded_regions=[], excluded_countries=[], 
        factor_dmas={}, mobi_dmas={}, 
        start_factor='deaths', start_hurdle=1, tail_factor='', tail_hurdle=1.2, 
        log=False, lognat=False, 
        min_deaths=0, min_days_from_start=0, 
        smooth=True,
        country_level=False, world_averages=False,
        temp_scale='C', 
        custom_sum=[],
        favor_earlier=False, factors_to_favor_earlier=[],
        interpolate=True, interpolate_categories=[], interpolation_method={'method': 'linear'},
        use_pbar=True
        ):

        # Base DataFrame
        self.baseframe = baseframe
        
        # Period used for Daily moving average of count categories
        self.count_dma = count_dma
        
        # Limit the casestudy df to certain count categories
        self.count_categories = accept_string_or_list(count_categories)
        self.count_categories = [cat for cat in self.count_categories if cat not in self.COUNT_TYPES]
        # Factors in focus for analysis
        self.factors = [factors] if isinstance(factors, str) else factors
        self.factor_dmas = factor_dmas
        
        # To remove specific regions or countries from the dataset
        self.regions = accept_string_or_list(regions)
        self.countries = accept_string_or_list(countries)
        self.excluded_regions = accept_string_or_list(excluded_regions)
        self.excluded_countries = accept_string_or_list(excluded_countries)
                
        # For now, Interpolate is strictly for COUNT_TYPES with NaNs
        self.interpolate = interpolate
        self.interpolate_categories = self.COUNT_TYPES if not interpolate_categories else interpolate_categories
        self.interpolation_method = interpolation_method

        # Hurdles to filter data and isolate regions/timeframes most pertinent to analysis
        self.log = log
        self.lognat = lognat
        self.min_deaths = min_deaths
        self.start_hurdle = start_hurdle
        self.start_factor = start_factor
        self.tail_hurdle = tail_hurdle
        self.tail_factor = tail_factor
        self.min_days_from_start = min_days_from_start
        
        self.country_level = country_level
        self.world_averages = world_averages
        self.smooth = False if country_level else smooth
        
        self.favor_earlier = True if factors_to_favor_earlier else favor_earlier
        self.factors_to_favor_earlier = accept_string_or_list(factors_to_favor_earlier)
        self.ALLOWED_FACTORS_TO_FAVOR_EARLIER = ['key3_sum', 'h_sum', 'e_sum', 'c_sum'] + self.STRINDEX_CATS
        self.custom_sum = custom_sum
        self.temp_scale = temp_scale
        
        # FACTORS
        self.temp_msmts = [msmt for msmt in self.TEMP_MSMTS if msmt in self.factors]
        self.polluts = [factor for factor in self.factors if factor in self.POLLUTS]        
        self.age_ranges = [factor for factor in self.factors if factor in self.ALL_RANGES]
        self.causes = [factor for factor in self.factors if factor in self.CAUSES]
        self.strindex_factors = [factor for factor in self.factors if factor in self.STRINDEX_CATS]
        
        self.mobis = [factor for factor in self.factors if factor in [*self.GMOBIS, *self.AMOBIS]]
        self.mobi_dmas = mobi_dmas
        
        self.pop_cats = self.age_ranges + self.causes

        if 'visitors' in factors:
            self.pop_cats.append('visitors')
        if 'gdp' in factors:
            self.pop_cats.append('gdp')

        if self.country_level:
            warnings.warn('smoothing is unavailable when country_level=True', stacklevel=2)
            if self.mobis:
                raise AttributeError("""
                    Google and Apple mobility factors {} are not available when country_level=True
                """.format(self.mobis)
            )
        else:
            countries_w_regions = [region for region in self.regions if region in self.COUNTRIES_W_REGIONS + self.COUNTRIES_W_REGIONS_LONG]
            if countries_w_regions:
                raise AttributeError(""""
                    {} ha{} subregions. To treat aggregate the country data, set `country_level=True` 
                """.format(', '.join(countries_w_regions), 's' if len(countries_w_regions) == 1 else 've'))

        if not all(factor in self.ALLOWED_FACTORS_TO_FAVOR_EARLIER for factor in self.factors_to_favor_earlier):
            raise AttributeError("""
                Only the following categories can included in factors_to_favor_earlier: {}
        """.format(' '.join(self.ALLOWED_FACTORS_TO_FAVOR_EARLIER)))

        if not all(factor in self.ALLOWED_FACTORS_TO_FAVOR_EARLIER for factor in self.factors_to_favor_earlier):
            raise AttributeError("""
                Only the following categories can included in factors_to_favor_earlier: {}
        """.format(' '.join(self.ALLOWED_FACTORS_TO_FAVOR_EARLIER)))

        if isinstance(self.factor_dmas, dict):
            dma_not_available = [key for key in self.factor_dmas.keys() if key not in self.DYNAMIC]
            if dma_not_available:
                raise AttributeError("""
                    DMA or growth not available for {}. Only available for {}.
                """.format(' ,'.join(dma_not_available), ' ,'.join(self.DYNAMIC)))
        
        ### ELIMATE THE GEORGIA COLLISION; GA, USA and the country/region Georgia
        if any(usa in self.countries for usa in ['USA', 'United State of America (the']) and 'Georgia' not in self.countries:
            self.excluded_countries += ['Georgia']

        self.use_pbar = use_pbar
        self.PBAR_CHECKPOINTS = {
            'country': {
                'desc': 'Aggregating to Country Level',
                'func': self._agg_to_country_level,
                'live': self.country_level,
            },
            'smoothing': {
                'desc': 'Apply Smoothing',
                'func': self._smoothing,
                'live': self.smooth,
            },
            'regions': {
                'desc': 'Process Regions',
                'func': self._process_cols,
                'live': True,
            },
        }

    def __new__(cls, *args, **kwargs):
        if cls is BaseStudy:
            warnings.warn('{}{}{}{}'.format(
                'It looks like you called BaseStudy directly. ',
                'This is not recommended. ', 
                'Ray provides significant performance ',
                'improvements and certain BaseStudy methods are not optimized.',
                ), stacklevel=2)
        return super().__new__(cls)

    def __getattr__(cls, name):
        chartnames = [
            'compchart', 'compchart4d', 
            'heatmap', 'barcharts', 
            'scatterflow', 'substrinscat', 'df'
        ]
        if name in chartnames:
            raise AttributeError('{} is only instantiated after a call to make. Did you call make()??'.format(name))
        else:
            raise AttributeError('{} has no attribute {}'.format(cls.__class__.__name__, name))

    def total_cases(self, date, regions=None):        
        """
        Parameter
        _________
        date:   type str, from '%Y-%m-%df' e.g. '2020-05-05'

        Returns
        ________
        type float, total global cases as of specified date
        """
        baseframe = self.baseframe.copy(deep=True)
        if regions:
            baseframe = baseframe[baseframe.region_name.isin(regions)]

        return baseframe[baseframe.date == date].cases.sum()

    def total_deaths(self, date, regions=None):
        """
        Parameter
        _________
        date:   type str, from '%Y-%m-%df' e.g. '2020-05-05'

        Returns 
        ________
        type float, total global fatalities as of specified date
        """
        baseframe = self.baseframe.copy(deep=True)
        if regions:
            baseframe = baseframe[baseframe.region_name.isin(regions)]
        
        return baseframe[baseframe.date == date].deaths.sum()

    def _smoothing(self, df):
        """
        Applies nieve smoothing to both negative daily count values
        and to very large daily increases

        First, search and collect region/date/count combinations with negative values
        and very large positive values (daily growth > 10x)
        Exclude Jan 1 dates as this is the region crossover date and will result in
        negative values each time
        """
        counts_w_negs = {}
        counts_w_jumps = {}

        for count_type in self.COUNT_TYPES:
            new = df[count_type].diff()
            filter_negs = new < 0
            filter_jan1 = (df.date != dt(2020,1,1))
            counts_w_negs[count_type] = df[filter_negs & filter_jan1][['region_id', 'region_name', 'date', count_type]]

            growth = new / new.shift(1)
            filter_jump = (10 < growth) & (growth < np.inf)
            filter_early_jumps = new / df[count_type] < .1
            counts_w_jumps[count_type] = df[filter_jump & filter_early_jumps][['region_id', 'region_name', 'date', count_type]]
        
        pbar = tqdm(total=sum(df.shape[0] for df in counts_w_negs.values()), position=1, leave=False)
        for count_type, df_negs in counts_w_negs.items():
            for i, row in df_negs.iterrows():
                df_reg = df[df.region_id == row.region_id]
                prenegs = df_reg[(df_reg.date < row.date) ][count_type]
                recount = nbf.redistribute(prenegs.values, row[count_type])
                
                df.at[prenegs.index, count_type] = recount
                df.at[i, count_type] = np.nan
                
                df.loc[prenegs.index[-1]:df_reg.index[-1], count_type] = \
                    df.loc[prenegs.index[-1]:df_reg.index[-1], count_type].interpolate(method='linear')
                pbar.update(1)
        pbar.close()

        pbar = tqdm(total=sum(df.shape[0] for df in counts_w_jumps.values()), disable=not self.use_pbar, position=1, leave=False)
        for count_type, df_jumps in counts_w_jumps.items():
            for i, row in df_jumps.iterrows():
                prejump = df[(df.date < row.date) & (df.region_id == row.region_id)][['date', count_type]]
                if not prejump.empty:
                    args = [
                        prejump[count_type].diff().values,
                        prejump[count_type].values, 
                        row[count_type],
                        np.array([])
                    ]                        
                    recount = nbf.redistribute_jumps(*args)
                    
                    df.at[prejump.index, count_type] = recount
                pbar.update(1)
        pbar.close()
        return df

    def _agg_to_country_level(self, baseframe):
        # Different aggregation approaches for columns
        FIRST_ROW = ['travel_year', 'gdp_year', 'year', 'country', 'country_id', 'country_code']
        SUMS = self.COUNT_TYPES + self.ALL_RANGES + self.CAUSES + ['visitors', 'gdp', 'land_KM2', 'city_KM2', 'population']
        AVERAGES = self.STRINDEX_CATS + self.MSMTS
        EXCLUDES = self.POLLUTS + self.GMOBIS + self.AMOBIS
        
        # Filter baseframe
        df_subs = baseframe[baseframe.country_code.isin(self.COUNTRIES_W_REGIONS)]

        # Loop through each country 
        dfs_country = []
        for code, df_group in df_subs.groupby('country_code'):
            region_id = 'id_for_' + code
            region_name = 'name_for_' + code
            region_code = code
            country_dict = df_group.iloc[0][FIRST_ROW]

            # Group each country frame by date, then aggregate column values on the date
            country_dicts = []
            for date, df_date in df_group.groupby('date'):
                country_dict = {'region_id': region_id, 'region_code':region_code, 'region_name': region_name, **country_dict}
                country_dict['date'] = date

                for sum_ in SUMS:
                    country_dict[sum_] = df_date[sum_].sum()
                for avg in AVERAGES:
                    country_dict[avg] = df_date[avg].mean()   

                country_dict['land_dens'] = country_dict['population'] / country_dict['land_KM2']
                country_dict['city_dens'] = country_dict['population'] / country_dict['city_KM2']
                country_dicts.append(country_dict)
            
            df_country = pd.DataFrame(country_dicts)
            dfs_country.append(df_country)
            
        df_countries = pd.concat(dfs_country)

        df_nosubs = baseframe[~baseframe.country_code.isin(self.COUNTRIES_W_REGIONS)]

        # Exclude values that don't aggregate across regions easily
        df_nosubs = df_nosubs.drop(EXCLUDES, axis=1)
        
        return pd.concat([df_nosubs, df_countries]).reset_index(drop=True)

    @staticmethod
    def _groupwork(df_group, self):
        df_group = df_group.copy(deep=True)
        
        if self.interpolate:
            for factor in self.interpolate_categories:
                df_group[factor] = df_group[factor].interpolate(**self.interpolation_method)
        
        for count_type in self.COUNT_TYPES:
            df_group[count_type + '_new'] = df_group[count_type].diff()
            df_group[count_type + '_dma'] = df_group[count_type].rolling(window=self.count_dma).mean()
            df_group[count_type + '_new_dma'] = df_group[count_type + '_new'].rolling(window=self.count_dma).mean()

        df_group['cases_per_test'] = df_group['cases'] / df_group['tests']
        df_group['tests_per_case'] = df_group['tests'] / df_group['cases']
        for append in self.COUNT_APPENDS:
            df_group['cases{}_per_test{}'.format(append, append)] = df_group['cases{}'.format(append)] / df_group['tests{}'.format(append)]

        for count_cat in self.BASECOUNT_CATS:
            df_group[count_cat + '_per_1K'] = df_group[count_cat] / df_group['population'] * 1000
            df_group[count_cat + '_per_1M'] = df_group[count_cat] / df_group['population'] * 1000000
            df_group[count_cat + '_per_person_per_land_KM2'] = df_group[count_cat] / (df_group['land_dens'])
            df_group[count_cat + '_per_person_per_city_KM2'] = df_group[count_cat] / (df_group['city_dens'])
        
        if self.log:
            with np.errstate(divide='ignore', invalid='ignore'):
                for cat in self.BASE_PLUS_PER_CATS:
                    df_group[cat + '_log'] = np.log10(df_group[cat].values)

        if self.lognat:
            with np.errstate(divide='ignore', invalid='ignore'):
                for cat in self.BASE_PLUS_PER_CATS:
                    df_group[cat + '_lognat'] = np.log(df_group[cat].values)
        
        for col in df_group.columns:
            if col not in self.CASE_COLS:
                df_group['growth_' + col] = df_group[col] / df_group[col].shift(1)

        # Filter dataframe for count categories
        if self.count_categories:
            df_group = df_group[self.CASE_COLS + self.count_categories + self.factors]

        # Forward fill any nans in the strindex categories. For some, the entire columns is nans, so fill those with 0s.
        if self.strindex_factors:
            df_group[self.strindex_factors] = df_group[self.strindex_factors].fillna(method='ffill')
            df_group[self.strindex_factors] = df_group[self.strindex_factors].fillna(0)

        # SUM certain strindex categories
        if all(cat in self.factors for cat in self.CONTAIN_CATS):
            df_group['c_sum'] = df_group[self.CONTAIN_CATS].sum(axis=1)
        
        if all(cat in self.factors for cat in self.ECON_CATS):
            df_group['e_sum'] = df_group[self.ECON_CATS].sum(axis=1)

        if all(cat in self.factors for cat in self.HEALTH_CATS):
            df_group['h_sum'] = df_group[self.HEALTH_CATS].sum(axis=1)

        if all(cat in self.factors for cat in self.KEY3_CATS):
            df_group['key3_sum'] = df_group[self.KEY3_CATS].sum(axis=1)

        if self.favor_earlier:
            for factor in self.factors_to_favor_earlier:
                df_group[factor + '_earlier'] = nbf.earlier_is_better(df_group[factor])
        
        # Adjust factors for percentage of population
        if self.pop_cats:
            for pop_cat in self.pop_cats:
                df_group[pop_cat + '_%'] = df_group[pop_cat] / df_group['population']
        
        # Unit conversions for chosen temperature scale
        if self.temp_msmts:
            for temp_msmt in self.temp_msmts:
                if self.temp_scale == 'C':
                    df_group[temp_msmt] = df_group[temp_msmt] - 273.15                            
                elif self.temp_scale == 'F':
                    df_group[temp_msmt] = df_group[temp_msmt] * 9 / 5 - 459.67

        if self.factor_dmas:
            # Return empty dataframe if any factor has only NaNs for the time period and the region
            for factor, dma in self.factor_dmas.items():
                df_group[factor + '_dma'] = df_group[factor].rolling(window=dma).mean()
                df_group[factor + '_growth'] = df_group[factor] / df_group[factor].shift(1)
                df_group[factor + '_growth_dma'] = df_group[factor + '_growth'].rolling(window=dma).mean()
        
        if self.mobis:
            for mobi in self.mobis:
                df_group[mobi] /= 100
                df_group[mobi + '_growth'] = df_group[mobi] + 1
            for mobi, dma in self.mobi_dmas.items():
                
                df_group[mobi + '_growth_dma'] = df_group[mobi + '_growth'].rolling(window=dma).mean()
                df_group[mobi + '_dma'] = df_group[mobi + '_growth_dma'] - 1

        # Filter observations on the front end
        # If there are no observations that satisfy the hurdle
        # set df_group to empty 
        if self.start_factor:
            hurdle_index = df_group[df_group[self.start_factor] >= self.start_hurdle].index
            
            if hurdle_index.size >= 1:
                first_row = hurdle_index[0]
                df_group = df_group.loc[first_row:]
            else:
                df_group = pd.DataFrame()

        # Filter observations on the tailend
        if self.tail_factor:
            if (df_group[self.tail_factor] >= self.tail_hurdle).any():
                last_row = df_group[df_group[self.tail_factor] >= self.tail_hurdle].index[-1]
                df_group = df_group.loc[:last_row]
            else:
                df_group = pd.DataFrame()

        if not df_group.empty:
            # Indicates the number of days since the hurdle was met
            df_group['days'] = df_group['date'] - df_group['date'].iloc[0]

        # If region data does not cover enough days, return empty Dataframe
        if len(df_group) < self.min_days_from_start:
            df_group = pd.DataFrame()

        return df_group            

    def _process_cols(self, df):
        new_dfs = []
        looplen = df.region_id.unique().shape[0]
        for i, df_group in tqdm(df.groupby('region_id'), disable=not self.use_pbar, total=looplen, position=1, leave=False):
            new_dfs.append(BaseStudy._groupwork(df_group, self))       
        return new_dfs

    def _filter_regions(self, df):
        if self.regions:
            df = df[
                df['region_name'].isin(self.regions) |
                df['region_id'].isin(self.regions) |
                df['region_code'].isin(self.regions)
            ]
        
        if self.countries:    
            df = df[
                df['country'].isin(self.countries) | 
                df['country_code'].isin(self.countries) |
                df['country_id'].isin(self.countries)
            ]
        
        if self.excluded_regions:
            df = df[~(
                df['region_name'].isin(self.excluded_regions) |
                df['region_id'].isin(self.excluded_regions) |
                df['region_code'].isin(self.excluded_regions)
            )]
        
        if self.excluded_countries:
            df = df[~(
                df['country'].isin(self.excluded_countries) | 
                df['country_code'].isin(self.excluded_countries) |
                df['country_id'].isin(self.excluded_countries)
            )]
        return df       

    def _filter_min_death(self, df):
        """
        Remove regions that don't meet a minimum death threshold if start_hurdle provided
        This must be completed before the main loop, because the shift may look to 
        dates that occur BEFORE the start_hurdle. These will be cutoff in the main the loop
        """
        if self.start_factor == 'deaths' or self.min_deaths:
            min_deaths = self.min_deaths if self.min_deaths else self.start_hurdle
            max_deaths = df.groupby('region_id')['deaths'].max()
            regions_above_threshold = max_deaths.where(max_deaths > min_deaths).dropna().index.values
            df = df[df['region_id'].isin(regions_above_threshold)]

        return df

    def _setup_pbar(self, init_desc:str=None):
        # Initiate progress bar object, start the bar,
        # then wrap functions that are pbar checkpoints
        init_desc = init_desc if init_desc else 'Creating CaseStudy'
        
        live_checks = [(v['func'], v['desc']) for k,v in self.PBAR_CHECKPOINTS.items() if v['live']]
        pbar = ProgressBar(num_checks=len(live_checks), init_desc=init_desc)
        pbar.wrap_multiple(self, live_checks)
             
        return pbar

    def _make_charts(self):
        # Chart inner classes; pass the casestudy instance to make 
        # attributes accesible at the chart level
        if hasattr(self, 'df'):
            self.compchart = CompChart2D(self)
            self.compchart4d = CompChart4D(self)
            self.heatmap = HeatMap(self)
            self.barcharts = BarCharts(self)
            self.scatterflow = ScatterFlow(self)
            self.substrinscat = SubStrindexScatter(self)
        else:
            raise ValueError('Use the make() method to create the casestudy dataframe, then _make_charts will work')

    def make(self, baseframe=None, country_level=False, world_averages=False):
        """
        Filters and processes the base dataframe to isolate specific data for analysis

        A baseframe can be provided directly to augment outside of the standard usage
        """
        df = self.baseframe.copy(deep=True) if not baseframe else baseframe

        if self.country_level or country_level:
            df = self._agg_to_country_level(df)
        
        df = self._filter_regions(df)

        # Reset regions attribute so that it reflects
        # the actual remaining   regions in the dataframe        
        self.regions = df.region_name.unique().tolist()

        # Shrink DF to include only columns for factors in focus
        df = df[self.CASE_COLS + self.factors]
        df = self._filter_min_death(df)
    
        if self.smooth:
            df = self._smoothing(df)
        
        # Process additional columns and amend existing as per object instantiation
        # Concat to move forward
        dfs = self._process_cols(df)

        df = pd.concat(dfs)
    
        # Handle -inf values arising from taking natural log
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.sort_values(by=['region_id', 'date'])
        
        # Find world averages for each column on each date
        if self.world_averages or world_averages:
            globe_rows = []
            for date, df_date in df.groupby('date'):
                globe_row = ['REDID_FOR_WORLD_AVGS', 'COUNTRY_FOR_WORLD_AVGS', 'AVG', 'WorldAvg', 'WLDAVG', 'WorldAvg'] 
                globe_row += [date]

                df_date = df_date[[col for col in df_date.columns if col not in ['region_id', 'country_id', 'region_code', 'region_name','country_code', 'country', 'date']]]
                globe_row += df_date.mean().tolist()
                
                globe_row = [round(i, 2) if isinstance(i, float) else i for i in globe_row]
                globe_rows.append(globe_row)
            
            df_globe = pd.DataFrame(globe_rows, columns=df.columns)
            df = df.append(df_globe).sort_values(by=['region_name', 'date'])

        self.df = df.sort_values(by=['region_id', 'date'])
        self._make_charts()
