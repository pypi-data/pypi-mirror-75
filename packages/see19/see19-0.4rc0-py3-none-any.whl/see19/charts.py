import math
import operator
import numpy as np
import pandas as pd
import copy
import functools
from abc import ABC, abstractmethod, abstractproperty

from bokeh.plotting import figure, output_file, ColumnDataSource
from bokeh.palettes import Category20, Viridis256
from bokeh.transform import dodge, linear_cmap
from bokeh.models import HoverTool, Label, LinearAxis, Range1d, Arrow, NormalHead, OpenHead, VeeHead
from bokeh.io import export_png

import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib.cm as cm
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from .helpers import accept_string_or_list
from .constants import META_COLS, MANUAL_CHART_LABELS

class BaseChart(ABC):
    """
    Base Class for common chart attributes and methods
    2 main roles:
        1) converts casestudy instance attributes to more useable form
        2) centralizes label formatting
    """

    base_kwargs = dict(
        regions=[], x_category='', y_category='', z_category='',
        title={},
        xlabel=True, ylabel=True, zlabel=True, cblabel=True,
        xlabel_params={}, ylabel_params={}, zlabel_params={}, cblabel_params={},
        xticks=True, yticks=True, zticks=True,
        xtick_params={}, ytick_params={}, ztick_params={},
        spines={'top': False, 'right': False},
        color_category='', palette_base='coolwarm', xy_cbar=(0, 0), wh_cbar=(.3, .2), 
        annotations=[], hlines=[], gridlines=True, tight=True,
        width=16, height=8, figsize=(), save_file=False, filename='', dpi=300,
    )

    def __init__(self, casestudy):
        self._casestudy = casestudy
        self.df = self._casestudy.df.copy(deep=True)
        self.start_hurdle = self._casestudy.start_hurdle
        self.start_factor = self._casestudy.start_factor
        self.count_dma = self._casestudy.count_dma
        self.temp_scale = self._casestudy.temp_scale

        self.regions = self._casestudy.regions
        self.degrees = '\xb0' if self.temp_scale in ['C', 'F'] else ''
        
        self._make_labels()
        self.is_multiplots = False
        self.is_3D = False
        self.ALLOWED_AXIS_LABELS = ['xlabel', 'ylabel', 'zlabel', 'cblabel']
        self.make_kwargs = {**self.chart_kwargs, **self.base_kwargs}
    
    def _make_labels(self):
        """
        One big ugly label maker for all the elements of the dataset
        That can be used in the charts
        """
        # Next, Make Basic Labels for Count Types
        self.labels = {}
        for cat in self._casestudy.ALL_COUNT_CATS:
            self.labels[cat] = self._count_type_label_maker(cat)

        # Add Manual Labels First
        self.labels = {**self.labels, **MANUAL_CHART_LABELS}
        self.labels['date'] = 'Date'
        self.labels['temp'] = 'Temperature ({}{})'.format(self.degrees, self.temp_scale)
        self.labels['dewpoint'] = 'Dewpoint ({}{})'.format(self.degrees, self.temp_scale)

        if self.start_factor == 'date':
            self.labels = {
                **self.labels,
                'days_' + self.start_factor: 'Days Since {}'.format(self.start_hurdle.strftime('%B %d, %Y')),
            }
        else:
            self.labels = {
                **self.labels,
                'days_' + self.start_factor: 'Days Since {} {}'.format(self.start_hurdle, self.labels[self.start_factor]),
                'days_to_max_' + self.start_factor : 'Days Since {} {} Until Max Fatality Rate'.format(self.start_hurdle, self.labels[self.start_factor]),
            }

        if self._casestudy.age_ranges:
            self.labels ={**self.labels, **{age_range + '_%': self._age_range_label_maker(age_range) for age_range in self._casestudy.age_ranges}}
        if self._casestudy.factor_dmas:
            for factor, dma in self._casestudy.factor_dmas.items():
                self.labels[factor + '_dma'] = self.labels[factor] + ' {}DMA'.format(dma)
        if self._casestudy.mobi_dmas:
            for factor, dma in self._casestudy.mobi_dmas.items():
                self.labels[factor + '_dma'] = self.labels[factor] + ' {}DMA'.format(dma)
        if self._casestudy.causes:
            self.labels = {**self.labels, **{cause + '_%': self._cause_of_death_label_maker(cause) for cause in self._casestudy.causes}}

        # Add case to test comp labels
        self.labels['cases_per_test'] = 'Confirmed Cases Per Test'
        self.labels['tests_per_case'] = 'Tests per Confirmed Case'

        for append in self._casestudy.COUNT_APPENDS:
            factor = 'cases{}_per_test{}'.format(append, append) 
            factor_split = factor.split('_per_')
            self.labels[factor] = self._count_type_label_maker(factor_split[0]) + ' Per ' + self._count_type_label_maker(factor_split[1])

        self.labels['c_sum'] = 'Sum of Containment Categories'
        self.labels['e_sum'] = 'Sum of Economic Categories'
        self.labels['h_sum'] = 'Sum of Health Categories'
        self.labels['key3_sum'] = 'Sum of Key 3 Categories'
        self.labels['custom_sum'] = 'Custom Subcategory Sum'

    def _count_type_label_maker(self, cat):
        factor_split = cat.split('_')
        start = 'Daily' if 'new' in cat else 'Cumulative'
        per1K = ' per 1K' if '1K' in cat else ''
        per1M = ' per 1M' if '1M' in cat else ''
        density = ' / Person / {} KM\u00b2'.format('Land' if 'land_KM2' in cat else 'City') if 'KM2' in cat else ''
        dma = ' ({}DMA)'.format(self.count_dma) if 'dma' in cat else ''
        lognat = '\n(Natural Log)' if 'lognat' in cat else ''
        log = '\n(Log Base 10)' if 'log' in cat and 'lognat' not in cat else ''
        
        return '{} {}{}{}{}{}'.format(start, factor_split[0].capitalize(), per1K if per1K else per1M, density, dma, lognat if lognat else log)       
    
    def _age_range_label_maker(self, age_range):
        if '_' in age_range:
            return '% of Population Between ' + age_range[1:3] + ' & ' + age_range[-3:-1]
        elif 'PLUS' in age_range:
            return '% of Population Over ' + age_range[1:3]

    def _cause_of_death_label_maker(self, cause):
        return self.labels[cause] + ' as % of Population'

    def _title_maker(self, fig, kwargs):
        """
        For loop to handle dynamic number titles with dynamic positions
        Allowed kwargs are determined by the matplotlib function utilized
        """
        # Identify 3D plot via attribute of the 3DAxisSubplot object
        if kwargs['title']:
            if self.is_3D:
                fig.axes[0].text2D(**kwargs['title'])
            else:                
                fig.suptitle(**kwargs['title'])

    def _set_axis_labels(self, fig, kwargs):
        """
        Method to aggregate axislabel formating

        Allows a label string to be passed as kwargs within the axislabel dict.
        If a string is not passed, the label is assigned the default value.

        Process:
        1) Check if each axis label is set to True or False (i.e. xlabel = True). 
           If False, remove label_params from kwargs.
           This ensures the label will not be set
        2) make dict of axis_label name and associated params
        3) assert that parameters ending in `label_params` are allowed axis_labels
        4) loop thru each set of parameters:
            1) assign default text if text is not passed
            2) call appropriate set_label method based on nature of axis passed and label (cb and xlabel/ylabel/zlabel)
        """
        for axis_label in self.ALLOWED_AXIS_LABELS:
            if not kwargs[axis_label]:
                kwargs.pop(axis_label + '_params')

        pairs = {
            key.split('_params')[0]: key 
            for key, value in kwargs.items() 
            if 'label_params' in key and kwargs[key.split('_params')[0]]
        }
        assert all(pair in self.ALLOWED_AXIS_LABELS for pair in pairs.keys())
        
        for label, params in pairs.items():    
            kwargs[params]['ylabel' if label == 'cblabel' else label ] = kwargs['label_defaults'][label]
            
            if label == 'cblabel':
                # For now, cblabel is set on the yaxis; must change if want to change position of colorbar
                kwargs['cb'].set_ylabel(**kwargs[params])
            else:
                # Dynamically call the set_{}label function on the axis object
                # in general, the first axis in the figure will be the axis with the main labels
                ax = fig.axes[0]
                
                getattr(ax, 'set_' + label)(**kwargs[params])
 
    def _format_ticks(self, fig, kwargs):
        ax = fig.axes[0]

        # Format datetime axis
        for cat in self.axis_cats:
            if 'date' == kwargs[cat]:
                days = mdates.DayLocator()
                months = mdates.MonthLocator()
                months_fmt = mdates.DateFormatter('%b')

                dateaxis = getattr(ax, 'xaxis') if 'x' in cat else getattr(ax, 'yaxis')
                    
                dateaxis.set_major_locator(months)
                dateaxis.set_major_formatter(months_fmt)

        # Adjust Natural Log axis to more understandable units
        for axis in ['x', 'y', 'z']:
            if 'log' in kwargs['{}_category'.format(axis)]:
                ticks = getattr(fig.axes[0], 'get_{}ticks'.format(axis))()

                if 'lognat' in kwargs['{}_category'.format(axis)]:
                    ticklabels = np.exp(ticks)
                else:
                    ticklabels = 10**np.array(ticks)
                factors = []
                for label in ticklabels:
                    factor = [i for i in range(10) if round(label, i) != 0]
                    
                    factors.append(factor[0])
                ticklabels = [round(label, factors[i]) for i, label in enumerate(ticklabels)]
                getattr(fig.axes[0], 'set_{}ticklabels'.format(axis))(ticklabels)

        basetick_kwargs = {
            'pad': 4, 'labelsize': 10,
        }
        # Set tick params
        for key in kwargs:
            if 'tick_params' in key:
                kwargs[key] = self._set_default_kwargs(basetick_kwargs, kwargs[key])
                if kwargs[key[0] + 'ticks']:
                    ax.tick_params(axis=key[0], which='major',  **kwargs[key])

    def _format_spines(self, fig, kwargs):
        if not self.is_multiplots:
            for spine, val in kwargs['spines'].items():
                fig.axes[0].spines[spine].set_visible(val)

    def _set_default_kwargs(self, defaults, kwargs):
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value
        return kwargs

    @property
    @abstractmethod
    def chart_kwargs(self):
        """
        Returns a dictionary of kwargs specific to the child chart class make() method
        """
        return {}

    @abstractmethod
    def make(self):
        """
        Main implementation method for child chart class
        """
        pass

    def _not_supported(self, **kwargs):
        not_supported = [k for k in kwargs.keys() if k not in self.make_kwargs]
        fmt_tup = (
            ' '.join(not_supported), 
            's' if len(not_supported) > 1 else '',
            'are' if len(not_supported) > 1 else 'is',
        )
        if not_supported:
            raise ValueError('{} parameter{} {} not supported. See guide and/or source code for supported kwargs'.format(*fmt_tup))

    @classmethod
    def makedeco(cls, makefunc):
        """
        Decorator to handle common keywords and code among child class make() functions
        """
        def wrapper(self, *args, **kwargs):
            """
            base_kwargs = default values of parameters among all child class make() functions
            if the base_kwarg is not present in **kwargs, then the base_kwargs is added to kwargs
            """
            # Check if kwargs are supported and set any defaults
            self._not_supported(**kwargs)
            kwargs = self._set_default_kwargs(self.make_kwargs, kwargs)

            self.axis_cats = ['x_category', 'y_category', 'z_category']
            
            if kwargs['figsize']:
                kwargs['width'] = kwargs['figsize'][0]
                kwargs['height'] = kwargs['figsize'][1]

            ### Pre-child error handling ###
            for kw in kwargs:
                if ('title' == kw or '_params' in kw) and not isinstance(kwargs[kw], dict):
                    raise TypeError('`{}` must be a dictionary of params for the corresponding matplotlib object: https://matplotlib.org/'.format(kw))

            if kwargs['save_file'] and not kwargs['filename']:
                AssertionError('When `save_file=True`, filename must be provided')

            ### Pre-child processing ###
            # Filter for given regions
            kwargs['df'] = self.df.copy(deep=True)
            if kwargs['regions']:
                kwargs['regions'] = accept_string_or_list(kwargs['regions'])
                kwargs['df'] = kwargs['df'][
                    kwargs['df']['region_name'].isin(kwargs['regions']) |
                    kwargs['df']['region_id'].isin(kwargs['regions']) |
                    kwargs['df']['region_code'].isin(kwargs['regions'])
                ]
            else:
                kwargs['regions'] = copy.deepcopy(self.regions)

            for cat in self.axis_cats:
                if kwargs[cat] == 'days':
                    kwargs['df'].days = kwargs['df'].days.dt.days

            ### child function processing ###
            plt, fig, kwargs = makefunc(self, *args, **kwargs)

            ### check if colorbar present ###
            if 'parasite_axes.AxesHostAxes' in str(fig.axes):
                cb_index = [i for i, ax in enumerate(str(fig.axes).split(',')) if 'parasite_axes.AxesHostAxes' in ax].pop()
                kwargs['cb'] = fig.axes[cb_index]
            else:
                kwargs['cblabel'] = False

            ### check if multiple subplots ###
            if 'cb' in kwargs and len(fig.axes) > 2:
                self.is_multiplots = True
            elif len(fig.axes) > 1:
                self.is_multiplots = True

            self.is_3D = '_axis3don' in fig.axes[0].__dict__ and fig.axes[0]._axis3don
            if not self.is_3D:
                kwargs['zlabel'] = False
                kwargs['zticks'] = False

            ### post-child processing ###
            self._title_maker(fig, kwargs)
            self._set_axis_labels(fig, kwargs)
            self._format_ticks(fig, kwargs)
            self._format_spines(fig, kwargs)

            for annot in kwargs['annotations']:
                plt.text(*annot, transform=fig.axes[0].transAxes)

            for hline in kwargs['hlines']:
                plt.axhline(hline)

            if kwargs['save_file']:
                plt.savefig(kwargs['filename'], bbox_inches='tight', dpi=kwargs['dpi'])
            
        return wrapper

class CompChart2D(BaseChart):
    """
    Matplotlib-based x/y 2D plot; replaces the Bokeh-based 2D chart as of version 0.3.6
    """    
    @property
    def chart_kwargs(self):
        return dict(
            overlay='', 
            olay_params={}, 
            legend=True,
            line_params={}, 
            legend_params={}, 
            colors=[],
        )

    @BaseChart.makedeco
    def make(self, *args, **kwargs):
        overlay = kwargs['overlay']
    
        if overlay and kwargs['df'].region_id.unique().shape[0] > 1:
            raise ValueError('`overlay` is only available when a single region is provided')
    
        x_category = kwargs['x_category']
        y_category = kwargs['y_category']
        
        fig, ax = plt.subplots(figsize=(kwargs['width'], kwargs['height']))

        for region_name, df_group in kwargs['df'].groupby('region_name'):
            x = df_group[x_category]
            y = df_group[y_category]

            ax.plot(x, y, label=region_name, **kwargs['line_params'])

            if overlay:
                ax_olay = ax.twinx()
                ax_olay.bar(x, kwargs['df'][overlay], **kwargs['olay_params'])

        # Set Line Colors
        if not kwargs['colors']:
            cmap = cm.get_cmap(kwargs['palette_base'])
            colors = [cmap(i) for i in np.linspace(0, 1, len(ax.lines))]
        else:
            colors = kwargs['colors']
        for i, j in enumerate(ax.lines):
            j.set_color(colors[i])
        
        legend_kwargs = {
            'loc': 'best', 
            'handletextpad': 0.3, 'handlelength': 0.2,
            'fontsize': 6,
        }
        legend_kwargs = self._set_default_kwargs(legend_kwargs, kwargs['legend_params'])
        if kwargs['legend']:
            plt.legend(**legend_kwargs)
        
        ax.set_xlim(kwargs['df'][x_category].min(), kwargs['df'][x_category].max())
        ax.set_ylim(kwargs['df'][y_category].min(), kwargs['df'][y_category].max())

        # Add label defaults
        kwargs['label_defaults'] = {
            'xlabel': self.labels['days_' + self.start_factor if x_category == 'days' else x_category],
            'ylabel': self.labels[y_category],
        }
        
        return plt, fig, kwargs

class CompChart2DBokeh(BaseChart):
    """
    This is the original 2D chart built in Bokeh; it was replaced 
    for better consistency of parameter inputs as of version 0.3.6
    """
    @property
    def chart_kwargs(self):
        return {}

    def _bar_incrementer(self, labels):
        """
        Used to space multiple bars around y-axis point
        """
        num_labels = len(labels)
        midpoint = num_labels / 2 if num_labels % 2 == 0 else num_labels / 2 - 0.5
        offset = self.base_inc * midpoint
        even_offset = self.base_inc / 2 if num_labels % 2 == 0 else 0

        return [i * self.base_inc - offset + even_offset for i in range(num_labels)]
    
    def _multiline_source(self, palette_shift=0):
        """
        Function to prepare dataframe for use in chart
        Loops through each region group
        """
        days = []
        values_by_region = []
        region_order = []
        for region_id, df_group in self.df_comp.groupby('region_id'):
            values = list(df_group[self.comp_category].values)
            days.append([i for i in range(len(values))])
            values_by_region.append(values)
            region_order.append(df_group.region_name.iloc[0])
        
        return {'x': days, 'y': values_by_region, 'regions': region_order}
    
    def _vbar_source(self):
        values_by_region = {}
        dates_by_region = {}
        for i, df_group in self.df_comp.groupby('region_name'):
            values = list(df_group[self.comp_category].values)
            dates = list(df_group['date'].dt.strftime('%b %d'))

            # If the counts for region are less than the max, add 0s until it matches the size of the longest region
            if len(values) < self.max_length:
                values += [0 for i in range(self.max_length - len(values))]
                dates += ['n/a' for i in range(self.max_length - len(dates))]

            values_by_region[i] = values
            dates_by_region[i + '_date'] = dates
        
        return {'x': self.days, **values_by_region, **dates_by_region}
    
    def make(
            self, comp_category='deaths_new_dma_per_1M', regions=None,
            comp_type='vbar', overlay=None, title='', legend_title='Region: Start Date',
            palette_base=Viridis256, palette_flip=False, palette_shift=0, 
            multiline_labels=True, label_offsets={}, fs_labels=8, 
            legend=False, legend_location='top_right',
            x_fontsize=10, y_fontsize=10,
            fs_xticks=16, fs_yticks=16, fs_overlay=10,
            fs_legend=8, h_legend=20, w_legend=20,
            width=750, height=500, base_inc=.25,
            save_file=False, filename=None, annotations=[],
            bg_color='white', bg_alpha=1, border_color='white', border_alpha=1,
        ):
        self.df_comp = self.df[self.df[comp_category].notna()].copy(deep=True)
        
        # If regions are passed, filter the dataframe and reset attributes
        # via `_chart_setup`
        if regions:
            regions = [regions] if isinstance(regions, str) else regions
            self.df_comp = self.df_comp[self.df_comp['region_name'].isin(regions)]
        else:
            regions = list(self.regions)
        
        # Setup additional class attributes
        self.comp_category = comp_category
        self.comp_type = comp_type
        self.palette_base = palette_base
        self.base_inc = base_inc
        self.max_length = self.df.groupby('region_id')['days'].max().max().days + 1
        self.days = [i for i in range(self.max_length)]

        # Set chart attributes
        fs_labels = str(fs_labels) + 'pt'
        min_y = self.df_comp[comp_category].min()
        min_y += min_y * .01
        max_y = self.df_comp[comp_category].max()
        if max_y < 0:
            max_y -= max_y * .1
        else:
            max_y += max_y * .1

        p = figure(
            y_range=Range1d(start=min_y, end=max_y),
            plot_height=height, plot_width=width,
            min_border=0,
            toolbar_location=None,
            title=title,
        )

        # Create the Color Palette
        # An extra color is added and changes in the coloridx are limited
        # to all but the last item, to allow for shifting of palette
        # via palette_shift
        palette_base = np.array(palette_base)
        coloridx = np.round(np.linspace(0, len(palette_base) - 1, len(regions) + 1)).astype(int)
        if palette_flip:
            coloridx[:-1] = coloridx[:-1][::-1]
        if palette_shift:
            coloridx[:-1] += palette_shift
        palette = palette_base[coloridx]
        
        if comp_type == 'multiline':
            ml_data = self._multiline_source()
            ml_data['color'] = palette[:-1]
            source_ml = ColumnDataSource(ml_data)
            p.multi_line(xs='x', ys='y', line_color='color', legend_group='regions', line_width=5, source=source_ml)

            # Setup labels for each line
            if multiline_labels:
                for i in range(len(ml_data['x'])):
                    x_label = int(ml_data['x'][i][-1])
                    y_label = ml_data['y'][i][-1]
                    x_offset = -20
                    y_offset = 5
                    label_region = ml_data['regions'][i]

                    if label_region in label_offsets.keys():
                        x_offset += label_offsets[label_region]['x_offset']
                        y_offset += label_offsets[label_region]['y_offset']
    
                    label = Label(
                        x=x_label, y=y_label, 
                        x_offset=x_offset, y_offset=y_offset,
                        text_font_size=fs_labels, text_color=palette[i], text_alpha=.8,
                        text=label_region, text_font_style='bold',
                        render_mode='canvas'
                    )
                    p.add_layout(label)

        if comp_type == 'vbar':
            vbar_data = self._vbar_source()
            vbar_source = ColumnDataSource(vbar_data)
            increments = self._bar_incrementer(regions)
            
            legend_items = []
            for i, region in enumerate(regions):
                region_start = vbar_data['{}_date'.format(region)][0]
                legend_label = region + ': {}'.format(region_start)

                v = p.vbar(
                    x=dodge('x', increments[i], range=p.x_range), top=region, width=.3, 
                   source=vbar_source, color=palette[i], legend_label=legend_label,
                )
        
        p.legend.visible = legend

        if legend_title:
            p.legend.title = 'Region: Start Date'

        p.legend.location = legend_location
        p.legend.border_line_color = 'black'
        p.legend.glyph_height = h_legend
        p.legend.glyph_width = w_legend
        p.legend.label_height = h_legend
        p.legend.label_width = h_legend

        p.legend.label_text_font_size = str(fs_legend) + 'pt'
        p.legend.background_fill_alpha = 0.0
        p.legend.border_line_alpha = 0.0

        p.xaxis.axis_label = self.labels['days_' + self.start_factor]
        p.xaxis.axis_label_text_font_size = str(x_fontsize) + 'pt'
        p.xaxis.major_label_text_font_size = str(fs_xticks) + 'pt'

        p.yaxis.axis_label = self.labels[comp_category]
        p.yaxis.axis_label_text_font_size = str(y_fontsize) + 'pt'
        p.yaxis.major_label_text_font_size = str(fs_yticks) + 'pt'

        p.xaxis.major_tick_line_color = None
        p.xgrid.grid_line_color = None

        p.min_border = 20

        if overlay:
            overlay_days = []
            overlay_by_region = []
            for region_id, df_group in self.df_comp.groupby('region_id'):
                overlays = list(df_group[overlay].dropna().values)
                overlay_days.append([i for i in range(len(overlays))])
                overlay_by_region.append(overlays)
                
            data2 = {'x': overlay_days, 'y': overlay_by_region, 'color': palette[:-1]}
            source2 = ColumnDataSource(data=data2)
            start = min(olay for region in overlay_by_region for olay in region) * 0.8
            end = max(olay for region in overlay_by_region for olay in region) * 1.1
            p.extra_y_ranges = {overlay: Range1d(start=start, end=end)}
            p.multi_line(xs='x', ys='y', line_color='color', line_width=4, source=source2,
                      y_range_name=overlay, alpha=.3,
            )

            right_axis_label = self.labels[overlay]
            p.add_layout(LinearAxis(y_range_name='{}'.format(overlay), axis_label=right_axis_label, axis_label_text_font_size=str(fs_overlay) + 'pt'), 'right')

        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.outline_line_color = border_color

        p.background_fill_color = bg_color
        p.background_fill_alpha = bg_alpha
        p.border_fill_color = border_color
        p.border_fill_alpha = border_alpha

        for annot in annotations:
            p.add_layout(Label(**annot))

        if save_file:
            export_png(p, filename=filename)

        return p

class CompChart4D(BaseChart):
    """
    Class for 4D bar charts
    
    Utilizes matplotlib
    
    Inherits `__init__`, attributes, and methods from BaseChart
    
    ***NOTE***
    
    matplotlib 3d bar charts can have issues with clipping and depth. these can be overcome by
    building the chart manually, one bar at a time, as per this answer from astroMonkey on stackoverflow:
    
    https://stackoverflow.com/questions/18602660/matplotlib-bar3d-clipping-problems/37374864#comment108302737_37374864
    """

    def _sph2cart(self, r, theta, phi):
        """
        For manual bar creation:
        transforms spherical to cartesian 
        """
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return x, y, z

    def _sphview(self, ax):
        """
        For manual bar creation:
        returns the camera position for 3D axes in spherical coordinates
        """
        r = np.square(np.max([ax.get_xlim(), ax.get_ylim()], 1)).sum()
        theta, phi = np.radians((90-ax.elev, ax.azim))
        return r, theta, phi

    def _ravzip(self, *itr):
        '''flatten and zip arrays'''
        return zip(*map(np.ravel, itr))
  
    def _data_morph_for_bar4d(self, df, z_category, color_category, comp_size:int=None, rank_category=None):
        rank_category = rank_category if rank_category else z_category
        
        cols_to_keep = list(set([z_category, rank_category]))
        
        if color_category:
            cols_to_keep += [color_category] 
        
        df = df[['region_id', 'region_name', 'region_code', 'country', 'date', 'days'] + cols_to_keep]
        df = df.dropna()
        
        dfs = []
        for region_id, df_group in df.groupby('region_id'):
            if (df_group[z_category].isnull()).any():
                df_group = df_group.loc[df_group.index[df_group[z_category].notna()]]
                df_group = df_group.reset_index().drop('index', axis=1)
            
            dfs.append(df_group)
        
        df = pd.concat(dfs) if dfs else df

        region_names = df.sort_values(rank_category, ascending=False)['region_name'].unique()[:comp_size]
        df = df[df.region_name.isin(region_names)]
        
        df.region_name = pd.Categorical(df.region_name, region_names)
        df = df.sort_values(by=['region_name', 'date'])
        
        return df
    
    def _grey_maker(self, rgb_value):
        return [rgb_value / 255 for i in range(3)] + [1.0]
    
    @property
    def chart_kwargs(self):
        return dict(
            comp_size=None, 
            rank_category=None,
            zaxis_left=False, 
            color_interval=(), bar_color='orange', 
            grid_grey= 87, pane_grey=200, tick_grey=30,
        )

    @BaseChart.makedeco
    def make(self, *args, **kwargs):
        # Setup class features through comp function
        regions = kwargs['regions']
        z_category=kwargs['z_category']
        color_category = kwargs['color_category']
        comp_size = kwargs['comp_size'] if kwargs['comp_size'] else len(regions)
        
        # Prep data for 4d
        self.df_chart = self._data_morph_for_bar4d(kwargs['df'], z_category, color_category, comp_size, kwargs['rank_category'])
        
        """
        ### Create Base Grid and variables for building the plot manually ###
        """        
        x_length = self.df_chart.region_name.unique().shape[0]
        y_length = self.df_chart['days'].max().days + 1
        
        Y, X = np.mgrid[:y_length, :x_length]
        grid = np.array([X, Y])
        (dx,), (dy,) = 0.8*np.diff(X[0,:2]), 0.8*np.diff(Y[:2,0])
        
        # Zarray for zaxis values and farrray for color selection
        # both zarray and farray must be padded to much the size of the 2d x & y arrays
        zarrays = []
        farrays = []
        for i, group in self.df_chart.groupby('region_name', observed=True):
            len_array = len(group[z_category].values)
            end_pad = y_length - len_array
            padded_zarray = np.pad(group[z_category].values, (0, end_pad), 'constant', )
            zarrays.append(padded_zarray)   
            
            if color_category:
                padded_farray = np.pad(group[color_category].values, (0, end_pad), 'constant', constant_values=(0, -1))
            else:
                # If color is not variable, farray padded with -2, to indicate alpha of 0 later on
                padded_farray = np.pad(np.full_like(group[z_category].values, -2), (0, end_pad), 'constant', constant_values=(0, -1))
            
            farrays.append(padded_farray)

        Z = np.stack((zarrays)).T
        M = np.stack((farrays)).T if farrays else np.full_like(Z, -2)
       
        """
        ### Instantiate the  plot ###
        """ 
        # Main Plot
        fig = plt.figure(figsize=(kwargs['width'], kwargs['height']))
        ax = plt.subplot(projection='3d')

        # Plot colors
        grid_rgba = self._grey_maker(kwargs['grid_grey'])
        pane_rgba = self._grey_maker(kwargs['pane_grey'])
        tick_rgba = self._grey_maker(kwargs['tick_grey'])
        
        # Color Bar must be defined before the 3d plot is built
        if color_category:
            color_min, color_max = kwargs['color_interval'] if kwargs['color_interval'] else (self.df_chart[color_category].min(), self.df_chart[color_category].max())
            norm = mpc.Normalize(vmin=color_min, vmax=color_max)
            cmap = cm.get_cmap(kwargs['palette_base'])

            cax = inset_axes(ax,
               width="60%",  # width = 5% of parent_bbox width
               height="1%",  # height : 50%
               loc='lower left',
               bbox_to_anchor=(*kwargs['xy_cbar'], *kwargs['wh_cbar']),
               bbox_transform=ax.transAxes,
               borderpad=0,
            )
            cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), extend='both', cax=cax)
             
        # Establish plot visual characteristics
        xyz = np.array(self._sph2cart(*self._sphview(ax)), ndmin=3).T       #camera position in xyz
        zo = np.multiply([X, Y, np.zeros_like(Z)], xyz).sum(0)  #"distance" of each bar from camera
        bars = np.empty(X.shape, dtype=object)

        #Build plot ... each loop is a bar
        for i, (x, y, dz, m, o) in enumerate(self._ravzip(X, Y, Z, M, zo)):
            if m == -1:
                color = 'white'
                alpha = 0
            elif m == -2:
                color = kwargs['bar_color']
                alpha = 1
            else:
                color = cmap(norm(m))
                alpha = 1
            j, k = divmod(i, x_length)
            bars[j, k] = pl = ax.bar3d(x, y, 0, dx, dy, dz, color=color, alpha=alpha)
            pl._sort_zpos = o
        
        """
        ### AXIS FORMATS ###
        """
        # Set ticklabels
        # If labels close to end of axis, truncate their names to fit in image
        region_codes = self.df_chart.region_code.unique()
        if kwargs['xticks']:
            xticklabels = [code for code in region_codes]
            for i in range(1, 7):
                if len(xticklabels[-i]) > 7:
                    xticklabels[-i] = xticklabels[-i][:6] + '.'
            ax.set_xticks(np.arange(len(region_codes)))
            ax.set_xticklabels(xticklabels, color=tick_rgba)
            kwargs['xlabel'] = False
        else:
            xticklabels = ['' for code in region_codes]
            ax.set_xticklabels(xticklabels, color=tick_rgba)
        
        # Remove every nth label for multiples over 40 regions
        # Over 100 regions, forget the labels
        if len(regions) > 50 and len(regions) <= 100:
            for label in ax.xaxis.get_ticklabels()[:: math.ceil(len(regions) / 40)]:
                label.set_visible(False)
        elif len(regions) > 100:
            for label in ax.xaxis.get_ticklabels():
                label.set_visible(False)

        """
        ### Move Z-Axis to Left Side ###
        """
        if kwargs['zaxis_left']:
            tmp_planes = ax.zaxis._PLANES 
            ax.zaxis._PLANES = ( tmp_planes[2], tmp_planes[3], 
                tmp_planes[0], tmp_planes[1], 
                tmp_planes[4], tmp_planes[5]
            )

            view_2 = (25, -65)
            init_view = view_2
            ax.view_init(*init_view)

        """
        ### GRID AND PANE FORMATS ###
        """
        # Remove gridlines if preferred
        ax.grid(kwargs['gridlines'])
        plt.rcParams['grid.color'] = grid_rgba
        ax.w_xaxis.set_pane_color(pane_rgba)
        ax.w_yaxis.set_pane_color(pane_rgba)
        ax.w_zaxis.set_pane_color(pane_rgba)

        # For tight layout
        plt.subplots_adjust(left=0, bottom=-.3, right=1, top=1, wspace=0, hspace=0)

        """
        ### Wrapper Formats ### 
        """
        # Tick Params
        kwargs['xtick_params']['color'] = pane_rgba
        kwargs['ytick_params']['color'] = pane_rgba
        kwargs['ztick_params']['color'] = tick_rgba

        # Titles
        if 's' in kwargs['title'] and kwargs['title']['s']:
            title_kwargs = {
                'bbox': {'boxstyle': 'round4', 'facecolor': pane_rgba, 'alpha': 1, 'edgecolor': grid_rgba},
                'color': tick_rgba,
                'transform': ax.transAxes,
            }
            kwargs['title'] = {**kwargs['title'], **title_kwargs}

        # Set Label Defaults
        if not kwargs['xticks']:
            kwargs['xlabel_params']['xlabel'] = 'Regions'
            kwargs['xlabel_params']['color'] = tick_rgba
        for label in ['ylabel', 'zlabel']:
            kwargs[label + '_params']['color'] = tick_rgba
        
        kwargs['label_defaults'] = {
            'xlabel': self.labels[self.start_factor],
            'ylabel': self.labels['days_' + self.start_factor], 
            'zlabel': self.labels[z_category], 
            'cblabel': self.labels[color_category],
        }

        return plt, fig, kwargs

class HeatMap(BaseChart):
    """
    Class for Heat Maps comparing a infection rates and a data factor

    Utilizes matplotlib
    """    
    def _data_morph_for_heatmap(self, df, x_category, y_category, color_category, x_start, color_start, comp_size:int=None, rank_category=''):
        rank_category = rank_category if rank_category else x_category

        # Filter for variables in the compsize
        comp_region_ids = list(df.sort_values(rank_category, ascending=False)['region_id'].unique())[:comp_size]
        df = df[df['region_id'].isin(comp_region_ids)]
        
        map_list = []
        for region_id, df_group in df.groupby('region_id'):
            map_dict = {}
            map_dict['region_id'] = region_id
            map_dict['region_id'] = region_id
            map_dict['region_name'] = df_group['region_name'].iloc[0]
            map_dict[y_category] = df_group[y_category].max()

            if x_category == 'days_to_max':
                max_idx = df_group[x_category].argmax()
                map_dict[x_category] = df_group.iloc[max_idx].days.days
            elif 'earlier' in x_category:
                map_dict[x_category] = df_group[x_category].mean()
            else:
                comp_idx = df_group[x_category].argmax() if x_start == 'max' else 0
                map_dict[x_category] = df_group[x_category].iloc[comp_idx]
                
            if color_category:
                color_idx = df_group[color_category].argmax() if color_start == 'max' else 0
                map_dict[color_category] = df_group[color_category].iloc[color_idx]

            map_list.append(map_dict)

        df_hm = pd.DataFrame(map_list)
        df_hm = df_hm.sort_values(by=x_category, ascending=False)
        
        return df_hm

    def box_stats(self, x_category, color_category, date, dirxn, xbox, ybox, factor_in_the_box='', inverse=False):
        if dirxn == 'greater':
            comp = operator.lt if inverse else operator.gt
            box_params = (comp(self.df_chart[x_category], xbox) & \
                (self.df_chart[x_category] > ybox)
            )
        elif dirxn == 'lesser':
            comp = operator.ge if inverse else operator.le
            box_params = (comp(self.df_chart[x_category], xbox) & \
                (self.df_chart[x_category] <= ybox)
            )
            
        df_box = self.df_chart[box_params]
 
        total_deaths = self._casestudy.total_deaths(date)
        box_deaths = self._casestudy.total_deaths(date, df_box.region_name.tolist())
        kwargs = {
            'df': df_box,
            'num_regs': df_box.shape[0],
            'all_deaths': box_deaths / total_deaths,
            self.labels[x_category]: df_box[x_category].mean(),            
        }
        if factor_in_the_box == 'z_category':
            kwargs[self.labels[x_category]] = df_box[x_category].mean()
        if factor_in_the_box == 'color_category':
            kwargs[self.labels[color_category]] = df_box[color_category].mean()
        return kwargs

    @property
    def chart_kwargs(self):
        return dict(
            rank_category=None, comp_size=None,
            x_start='start_hurdle', color_start='',
            hexsize=27, bins=None, rects=[],
        )

    @BaseChart.makedeco
    def make(self, *args, **kwargs):
        factor_starts = ['start_hurdle', 'max']
        x_category = kwargs['x_category']
        y_category = kwargs['y_category']
        color_category = kwargs['color_category']
        x_start = kwargs['x_start']
        color_start = kwargs['color_start']

        if x_start not in factor_starts:
            raise AttributeError("""
                x_start must be one of {}
        """.format(factor_starts))

        if color_start and color_start not in factor_starts:
            raise AttributeError("""
                color_start must be an empty string or one of {}
        """.format(factor_starts))

        # Prep data for 4d
        self.df_chart = self._data_morph_for_heatmap(kwargs['df'], x_category, y_category, color_category, x_start, color_start, kwargs['comp_size'], kwargs['rank_category'])
        x = self.df_chart[x_category]
        y = self.df_chart[y_category]
        c = self.df_chart[color_category] if color_category else x

        fig, ax = plt.subplots(figsize=(kwargs['width'], kwargs['height']))
        h = ax.hexbin(x, y, C=c, gridsize=kwargs['hexsize'], cmap=kwargs['palette_base'], bins=kwargs['bins'])

        if color_category:
            norm = mpc.Normalize(vmin=c.min(), vmax=c.max())
            cmap = cm.get_cmap(kwargs['palette_base'])
            
            cax = inset_axes(ax,
                width='3%',
                height='33%',
                loc='lower left',
                bbox_to_anchor=(1.03, 0., .3, 1),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )
            cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), extend='both', cax=cax)
            
        if kwargs['rects']:
            self.box_dfs = {}
            for i, rect in enumerate(kwargs['rects']):
                rect_patch = plt.Rectangle(*rect['args'], **rect['kwargs'])
                ax.add_patch(rect_patch)
                box_stats = self.box_stats(x_category, color_category, rect['date'], rect['dirxn'], *rect['args'][0], rect['factor_in_the_box'], rect['inverse'])
                self.box_dfs[i] = box_stats.pop('df')

                if rect['text']:
                    box_length = 35
                    text = 'Box {}{}'.format(i+1, ' ' * box_length)
                    text += '\n{}:{}{}'.format('# of Regions', ' ' * (box_length - 10), box_stats.pop('num_regs'))
                    text += '\n{}:{}{:.0%}'.format('% of All Deaths', ' ' * (box_length - 14), box_stats.pop('all_deaths'))
                    for statname, val in box_stats.items():
                        text += '\n{}:{}{:.{}}'.format(statname,' ' * (box_length - len(statname) - 5), val, '0%' if '%' in statname else '0f')
                    plt.text(
                        rect['x_text'], rect['y_text'], text, 
                        {'alpha': 1, 'color': 'black', 'style': 'italic', 'fontsize': 12, 'ha': rect['ha'], 'va': 'center', 'bbox':dict(facecolor=rect['kwargs']['color'], alpha=rect['alpha'], edgecolor='white')}
                    )

        # Label Defaults
        kwargs['label_defaults'] = {
            'xlabel': self.labels['days_to_max_' + self.start_factor if x_category == 'days_to_max' else x_category],
            'ylabel': self.labels[y_category], 
            'cblabel': self.labels[color_category],
        }

        return plt, fig, kwargs

class BarCharts(BaseChart):
    @property
    def chart_kwargs(self):
        return dict(
            as_of=None, categories=[], 
            sort_cols=[], feature_regions=[], 
            subtitles={'fontsize': 16}, 
            axes_xticks={'labelsize': 14}, axes_yticks={'labelsize': 14},
            bar_colors=['red', 'magenta', 'blue'],
        )

    def _data_morph_for_barcharts(self, df, as_of=None):
        # All figures as of specified date
        if as_of:
            df = df[df.date == self.as_of]

        first_counts = ['region_name', 'population', 'city_dens']
        first_counts += [a + b for a in [*self._casestudy.ALL_RANGES, *self._casestudy.MAJOR_CAUSES, 'gdp', 'visitors_%'] for b in ['', '_%']]
        last_counts = self._casestudy.COUNT_TYPES + [a + b for a in self._casestudy.COUNT_TYPES for b in self._casestudy.PER_APPENDS]
        max_counts = [a + '_new_dma' + b for a in self._casestudy.COUNT_TYPES for b in self._casestudy.PER_APPENDS]
        max_counts += ['uvb_dma', 'temp_dma', 'cases_per_test']
        max_counts += ['cases' + a + '_per_test' + a for a in self._casestudy.COUNT_APPENDS]
        max_counts += [a + b for a in self._casestudy.STRINDEX_CATS for b in ['', '_dma']]
        mobi_counts = [a + b for a in self._casestudy.mobi_dmas.keys() for b in ['', '_dma']]
                
        groups = []
        for region_id, df_group in df.groupby('region_id'):
            groupdict = {}
            groupdict['region_id'] = region_id
            groupdict['region_code'] = df_group.region_code.iloc[0]

            for col in df_group.columns:
                if col in first_counts:
                    groupdict[col] = df_group[col].iloc[0]
                if col in last_counts:
                    groupdict[col] = df_group[col].iloc[-1]
                if col in max_counts:
                    groupdict[col] = df_group[col].max()
                if col in mobi_counts:
                    groupdict[col] = -df_group[col].min()
            groups.append(groupdict)

        df_comp = pd.DataFrame(groups)
        df_comp = df_comp.sort_values(by='deaths', ascending=False)
        
        df_comp = df_comp.T
        df_comp.columns = df_comp.iloc[1]
        df_comp = df_comp.drop(['region_name'])
        
        return df_comp

    @BaseChart.makedeco
    def make(self, *args, **kwargs):
        # Eliminates tick param formating in the wrapper
        categories = kwargs['categories']
        bar_colors = kwargs['bar_colors']
        kwargs['xticks'] = False
        kwargs['yticks'] = False

        df_bcs = kwargs['df'][[*META_COLS, *[col for col in categories if col not in META_COLS]]]        
        
        self.df_chart = self._data_morph_for_barcharts(df_bcs, kwargs['as_of'])
        if kwargs['sort_cols']:
            self.df_chart = self.df_chart.sort_values(by=kwargs['sort_cols'], axis=1, ascending=False)
        
        categories = accept_string_or_list(categories if categories else self._casestudy.factors)
        if len(categories) > 1:
            if len(categories) % 2 != 0:
                categories.append('')
            categories = np.array(categories).reshape(-1, 2)
        else:
            categories = np.array(categories)
        
        fig, axs = plt.subplots(*categories.shape, figsize=(kwargs['width'], kwargs['height']))
        
        color_key = {feature: bar_colors[0] for feature in kwargs['feature_regions']}
        color_key['AVG'] = bar_colors[1]
        c = [color_key[region] if region in color_key.keys() else bar_colors[2] for region in self.df_chart.columns]

        if not isinstance(axs, np.ndarray):
            axs = np.array([axs])
        for i, factor in np.ndenumerate(categories):
            if factor:
                if axs.shape == (2,):
                    i = i[1]
                
                df_fact = self.df_chart.sort_values(by=factor, axis=1, ascending=False)
                x = df_fact.loc['region_code']
                y = df_fact.loc[factor].tolist()
                
                axs[i].bar(x, y, color=c, width=.5)

                axs[i].tick_params(axis='x', **kwargs['axes_xticks'])
                axs[i].tick_params(axis='y', **kwargs['axes_yticks'])
                axs[i].set_title(self.labels[factor], **kwargs['subtitles'])
                axs[i].margins(0.01, None)
            else:
                axs[i].tick_params(axis='both', which='both', length=0)
                axs[i].spines['right'].set_visible(False)
                axs[i].spines['top'].set_visible(False)
                axs[i].spines['left'].set_visible(False)
                axs[i].spines['bottom'].set_visible(False)

                plt.setp(axs[i].get_xticklabels(), visible=False)
                plt.setp(axs[i].get_yticklabels(), visible=False)
        
        plt.subplots_adjust(hspace=0.25)

        # Label defaults
        kwargs['label_defaults'] = {'xlabel': '', 'ylabel': ''}

        return plt, fig, kwargs

class ScatterFlow(BaseChart):
    """
    Chart for comparing regions on a single different category over time
    Category values are shown by color of data point for that region at that time
    """
    @property
    def chart_kwargs(self):
        return dict(y_category='', marker='s', ms=100)

    @BaseChart.makedeco
    def make(self,  *args, **kwargs):
        if not kwargs['y_category']:
            raise ValueError('You must provide a y_category')

        df = kwargs['df']

        try:
            num_regions = df.region_name.unique().shape[0]
            num_rows_w_max_days = df[df.days == df.days.max()].shape[0]
            assert num_regions == num_rows_w_max_days
        except AssertionError as e:
            raise ValueError('For Scatterflow charts, the CaseStudy df must be structured '
                'such that each region has the same number '
                'of entires (i.e. same number of `days` values). '
                'Suggest setting start_hurdle=date and selecting a specific date.'
            )
        
        regions = kwargs['regions']
        category = kwargs['y_category']

        df = df[['date', 'region_code', 'region_name', 'days', category]]
        df = df.sort_values(by=['region_code', 'days'], ascending=[False, True])
        self.df_chart = df

        vals = df[category].values
        region_keys = np.arange(1, len(regions) + 1)
        region_codes = df.region_code.unique()        
        max_days = df.days.dt.days.max()
        
        xs = np.tile(np.arange(max_days + 1), len(regions))
        ys = np.repeat(region_keys, max_days + 1)
        cs = np.where(np.isnan(vals), 0, vals)
        
        fig, ax = plt.subplots(figsize=(kwargs['width'], kwargs['height']))
        cmap = plt.cm.get_cmap(kwargs['palette_base'])
        sc = ax.scatter(xs, ys, marker=kwargs['marker'], s=kwargs['ms'], c=cs, vmin=cs.min(), vmax=cs.max(), cmap=cmap)
      
        cax = inset_axes(ax,
            width='6%',
            height='30%',
            loc='lower right',
            bbox_to_anchor=(*kwargs['xy_cbar'], *kwargs['wh_cbar']),
            bbox_transform=ax.transAxes,
            borderpad=0,
        )
        cb = fig.colorbar(
            sc, extend='both', 
            cax=cax, orientation='vertical',
        )
        cax.yaxis.set_ticks_position('right')
        cax.yaxis.set_label_position('right')

        ax.set_yticks(region_keys)
        yticklabels = [' '.join(list(region_code)) for region_code in region_codes]
        ax.set_yticklabels(yticklabels)
    
        """
        ### Wrapper Formats ### 
        """
        kwargs['label_defaults'] = {
            'xlabel': self.labels['days_' + self.start_factor],
            'ylabel': 'Regions', 
            'cblabel': self.labels[category],
        }

        return plt, fig, kwargs

class SubStrindexScatter(BaseChart):
    """
    Chart provides ScatterFlow for single region across the various subcategories of the Oxford Stringency Index
    Multiple regions supported via grid plot arrangement.
    Plot / grid size automatically adapted for the number of regions provided
    """

    def _inputs_for_scatter(self, df, region):
        df_reg = df[df.region_name == region][['date', 'days', *reversed(self._casestudy.STRINDEX_SUBCATS)]]
        xs = np.repeat(df_reg.days.dt.days, np.array([*reversed(self._casestudy.STRINDEX_SUBCATS)]).shape[0])
        ys = np.tile(self.subcats_keys, len(df_reg.days))
        
        zs = []
        for x in df_reg.days.values:
            counts = []
            for y in self.subcats_keys:
                count = df_reg[df_reg.days == x][self.subcats_key[y]].iloc[0]
                counts.append(count)
            zs.append(counts)
        zs = np.array(zs).flatten()

        return xs, ys, zs

    @property
    def chart_kwargs(self):
        return dict(
            xy_legend=(0, 0), 
            legend={'title': {}, 'text': {}}, 
            subtitles={}
        )

    @BaseChart.makedeco
    def make(self, *args, **kwargs):
        regions = kwargs['regions']
        legend = kwargs['legend']

        
        self.subcats_keys = np.arange(1, len(self._casestudy.STRINDEX_SUBCATS) + 1)
        self.subcats_key = {tup[0]: tup[1] for tup in zip(self.subcats_keys, reversed(self._casestudy.STRINDEX_SUBCATS))}

        input_key = {reg: self._inputs_for_scatter(kwargs['df'], reg) for reg in regions}
        
        # Shape grid into appropriate size for number of regions
        # Create empty plot for first box and last box
        if len(regions) > 1 and len(regions) <= 3:
            regions.insert(0, '')
            if len(regions) % 2 != 0:
                regions += ['']
            regions = np.array(regions).reshape(-1, 2)
        elif len(regions) > 3 and len(regions) <= 8: 
            regions.insert(0, '')
            while True:
                if len(regions) % 3 != 0:
                    regions += ['']
                else:
                    break
            regions = np.array(regions).reshape(-1, 3)
        elif len(regions) > 8: 
            regions.insert(0, '')
            while True:
                if len(regions) % 4 != 0:
                    regions += ['']
                else:
                    break
            regions = np.array(regions).reshape(-1, 4)
        else:
            regions = np.array(regions)
        
        fig, axs = plt.subplots(*regions.shape, figsize=(kwargs['width'], kwargs['height']))
        cmap = plt.cm.get_cmap(kwargs['palette_base'], 4)

        strindex_labels = [self.labels[val] for val in self.subcats_key.values()]
        if not isinstance(axs, np.ndarray):
            axs = np.array([axs])
        for i, region in np.ndenumerate(regions):    
            if region:
                i = i[1] if axs.shape == (2,) else i
                xs, ys, zs = input_key[region]
                sc = axs[i].scatter(xs, ys, c=zs, vmin=zs.min(), vmax=zs.max(), cmap=cmap)
                axs[i].set_yticks(self.subcats_keys)
                axs[i].set_yticklabels(self.subcats_key.values() if regions.size > 1 else strindex_labels)

                if len(regions) > 1:
                    axs[i].set_title(region, **kwargs['subtitles'])
            else:
                # Add legend in the first box
                if i == (0,0):
                    title_kwargs = {
                        'label': 'LEGEND', 'alpha': 1, 'color': 'black', 'va': 'center', 
                        'fontweight': 'demi', 'fontsize': 12,
                    }
                    legend['title'] = self._set_default_kwargs(title_kwargs, legend['title'])
                    axs[i].set_title(**legend['title']) 

                    legend_text = ''
                    for val in reversed(list(self.subcats_key.values())):
                        legend_text += '\n{}: {}'.format(val, self.labels[val])
                    text_kwargs = { 
                        's': legend_text,
                        'alpha': 1, 'color': 'black', 'fontsize': 12, 'ha': 'left', 'va': 'center', 
                        'bbox':dict(facecolor='white', alpha=1, edgecolor='white')
                    }
                    legend['text'] = self._set_default_kwargs(text_kwargs, legend['text'])                    
                    axs[i].text(*kwargs['xy_legend'], **legend['text'])

                # Remove spines and other features for first and last box
                axs[i].tick_params(axis='both', which='both', length=0)
                axs[i].spines['right'].set_visible(False)
                axs[i].spines['top'].set_visible(False)
                axs[i].spines['left'].set_visible(False)
                axs[i].spines['bottom'].set_visible(False)

                plt.setp(axs[i].get_xticklabels(), visible=False)
                plt.setp(axs[i].get_yticklabels(), visible=False)

        # COLOR BAR SETUP
        if regions.size == 1:
            axis_for_color_bar = axs[0] 
            cb_ticks_pos = 'right'
            cb_label_pos = 'right'
        else:
            axis_for_color_bar = axs[0, 0]
            cb_ticks_pos = 'left'
            cb_label_pos = 'left'
        cax = inset_axes(axis_for_color_bar,
            width='6%',
            height='70%',
            loc='lower left',
            bbox_to_anchor=(*kwargs['xy_cbar'], *kwargs['wh_cbar']),
            bbox_transform=axis_for_color_bar.transAxes,
            borderpad=0,
        )
        cb = fig.colorbar(sc, extend='both', cax=cax, orientation='vertical')
        cax.yaxis.set_ticks_position(cb_ticks_pos)
        cax.yaxis.set_label_position(cb_label_pos)

        plt.subplots_adjust(left=.1, bottom=.1, right=1, top=1, wspace=0.2, hspace=0.22)

        # Add label defaults
        kwargs['label_defaults'] = {
            'xlabel': self.labels['days_' + self.start_factor] if len(regions) == 1 else '',
            'ylabel': None, 
            'cblabel': 'Score',
        }
        return plt, fig, kwargs
