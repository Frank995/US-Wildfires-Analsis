from functools import partial
from pandas import DataFrame
from geopandas import GeoDataFrame, GeoSeries
from ipywidgets import BoundedIntText
from shapely.geometry import Polygon, Point
from shapely.affinity import scale

from utils.widgets_utils import *
from utils.plotting_utils import display_widgets
from utils.constants import US_STATES_DICT

class MapPlottingHandler():
    def __init__(self, df: DataFrame, gdf_states: GeoDataFrame, gdf_counties: GeoDataFrame):
        # Plotting filters
        self.topn = TOP_N_COUNTIES[DEFAULT]
        self.timespan = YEARS_RANGE
        
        # Map layers to display
        self.states_layer = None
        self.topn_counties_layer = None
        self.bottom_counties_layer = None

        # Dataframes
        self.df = df
        self.gdf_states = gdf_states
        self.gdf_counties = gdf_counties

    def __get_us_map_layers(self):
        ''' This function takes as inputs the dataset and shapes files for US states 
            and counties, and save the layers for the counties with the most and
            the least wildfires.'''

        # Clear previous success message and print updating 
        Q2_OUTPUT_HANDLER.clear_output()
        print("Updating layers")

        # Filter the dataset according to the widgets and group by county
        fires_per_county = \
            self.df[self.df['year'] \
                .between(self.timespan[0], self.timespan[1])] \
                .groupby(['county', 'state'], as_index=False)['year'] \
                .count() \
                .sort_values('year', ascending=False) \
                .reset_index(drop=True)
        fires_per_county.columns = ['county', 'state', 'fires']

        # Group again by state this time
        fires_per_state = \
            fires_per_county \
                .groupby(['state'], as_index=False)['fires'] \
                .sum()
        fires_per_state = {row['state']: row['fires'] for _, row in fires_per_state.iterrows()}
        
        # Add the number of wildfires per state in the GeoDataFrame
        self.gdf_states['wildfires'] = self.gdf_states['NAME'].apply(lambda x: fires_per_state.get(US_STATES_DICT[x], 0))
        
        # Save the GeoDataFrame as bottom layer
        self.states_layer = self.gdf_states.explore(
            "wildfires", cmap="Oranges", tiles=None,
            style_kwds={'color':'black', 'opacity':0.7},
            tooltip=['wildfires']
        )

        # Compute top N counties per number of wildfires
        # NOTE: The problem is that the counties name in the dataset and in the shape file
        # do not always coincide if there are non english charachters or there are 
        # multiple words.
        # This is rarely the case, and fixing it goes beyond the aim of this assignment
        # so I'm just continuing in case it happens.
        topn_counties_points = []
        for ind, row in fires_per_county.iloc[:self.topn, :].iterrows():
            try:
                county_row = self.gdf_counties[self.gdf_counties['NAME'] == row['county']].reset_index(drop=True)
                topn_counties_points.append(Point(float(county_row.loc[0, 'INTPTLON']), float(county_row.loc[0, 'INTPTLAT'])))
            except:
                continue
        topn_counties_points = GeoSeries(
            topn_counties_points,
            crs="epsg:4269"
        )

        # Compute counties with only 1 wildfire
        bottom_counties_points = []
        for ind, row in fires_per_county.iterrows():
            if row['fires'] == 1:
                try:
                    county_row = self.gdf_counties[self.gdf_counties['NAME'] == row['county']].reset_index(drop=True)
                    bottom_counties_points.append(Point(float(county_row.loc[0, 'INTPTLON']), float(county_row.loc[0, 'INTPTLAT'])))
                except:
                    continue
        bottom_counties_points = GeoSeries(
            bottom_counties_points,
            crs="epsg:4269"
        )

        # Take the number o wildfires for the top N and similarly
        # for the counties with just 1
        topn_counties_fires = DataFrame(
            fires_per_county.loc[:(self.topn-1), 'fires'].to_numpy(),
            columns=["wildfires"],
        )
        bottom_counties_fires = DataFrame(
            [1]*len(bottom_counties_points),
            columns=["wildfires"],
        )

        # Save the GeoDataFrames to global variables
        self.topn_counties_layer = GeoDataFrame(
            geometry=topn_counties_points,
            data=topn_counties_fires,
        )

        self.bottom_counties_layer = GeoDataFrame(
            geometry=bottom_counties_points,
            data=bottom_counties_fires,
        )
        
        # Print success message
        Q2_OUTPUT_HANDLER.clear_output()
        print("Layers updated!")

    def update_q2_filters(self, _=None):
        ''' Update a global variable with filters and run function to generate layers '''
        self.topn = Q2_TEXT.value
        self.timespan = Q2_SLIDER.value
        
        with Q2_OUTPUT_HANDLER:
            self.__get_us_map_layers()

    def activate_q2(self):
        ''' Main function to show the results for Q2. '''

        # Differently from Q1 here I have to make an intermediate passage
        # The reason is that there are two widgets that point to the same
        # handler that can handle one input at a time. For this, I need to
        # store the values in a class variable, using the handler to
        # update it, and then call the plotting function.
        # Also run it once first to load the default layers.
        self.update_q2_filters()
        Q2_TEXT.observe(self.update_q2_filters)
        Q2_SLIDER.observe(self.update_q2_filters)
        display_widgets(Q2_TEXT, Q2_SLIDER, Q2_OUTPUT_HANDLER)
