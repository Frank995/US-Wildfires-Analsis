import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from functools import partial
from sklearn.linear_model import LinearRegression

from utils.widgets_utils import *
from utils.data_utils import STARTING_EPOCH
from utils.constants import FIRE_CAUSE_CODE_MAPPING


def display_widgets(*widgets):
    ''' Utility function to display all the necesary widgets. '''
    for widget in widgets:
        display(widget)

######### Q1 #########

def __plot_fires_trend(df: pd.DataFrame, slider_value: dict):
    ''' This function takes as input a pandas DataFrame and the current 
        value of the slider to show the time trend of fires in the USA.'''

    # Necessary to handle dynamic plotting
    with Q1_OUTPUT_HANDLER:

        # Compute the bins number given the bins size and the counts per each of them
        days_per_bin = slider_value['new'] * 30
        bins_number = round((df['datetime'].max() - df['datetime'].min()) \
            / dt.timedelta(days=days_per_bin))
        counts, bins = np.histogram(df['date'], bins=bins_number)

        # Get the central value for each bin and use it as X for linear regression
        mean_bins = np.array([(bins[i] + bins[i+1])/2 for i in range(len(counts))])
        date_bins = pd.to_datetime(mean_bins - STARTING_EPOCH, unit='D')

        # Train the model. Linear regression is likely very efficient and we can do it
        # without any problems.
        model = LinearRegression()
        model = model.fit(mean_bins.reshape(-1,1), counts)
        predictions = model.predict(mean_bins.reshape(-1,1))

        # Take the mean increment of fires per bin
        mean_increment = model.coef_[0] * (mean_bins[1] - mean_bins[0])

        # Plot the histograms, the regression line and some more info
        plt.bar(
            date_bins, counts,
            width=date_bins[1]-date_bins[0]-dt.timedelta(days=days_per_bin//2),
            align='edge', ec='k', linewidth=1, color='orange'
        )
        plt.plot(
            date_bins, predictions, color='blue',
            linestyle='dashed', linewidth=2, label='Regression line'
        )
        plt.annotate(
            f"{mean_increment:+.2f} fires per bin", xy=(0, 1), xytext=(12, -12), va='top',
             xycoords='axes fraction', textcoords='offset points'
        )
        
        plt.xlabel("Year")
        plt.ylabel("Number of fires")
        plt.title("Temporal trend of wildfires")
        plt.legend()
        
        # In order to make the transition smoother we want to delete the previous
        # output after we finished computations.
        Q1_OUTPUT_HANDLER.clear_output()
        plt.show()

def plot_q1(df: pd.DataFrame):
    ''' Main function to show the results for Q1. '''

    # Plot function with default values, then set up the handler and display widgets
    __plot_fires_trend(df, {'new': MONTHS_PER_BIN[DEFAULT]})
    Q1_SLIDER.observe(partial(__plot_fires_trend, df), names='value')
    display_widgets(Q1_SLIDER, Q1_OUTPUT_HANDLER)

######### Q3 #########

def __predict_fire_cause(model, _):
    ''' This function takes as input a sklearn compatible ML model
        and diplay a DataFrame with the probabilities per each class. '''

    with Q3_OUTPUT_HANDLER:
        size = Q3_SIZE_TEXT.value
        lat = Q3_LAT_TEXT.value
        lon = Q3_LAT_TEXT.value
        date = pd.Timestamp(Q3_DATE_PICKER.value).to_julian_date()
        probas = model.predict_proba([[size, lat, lon, date]])
        output = pd.DataFrame(
            [[FIRE_CAUSE_CODE_MAPPING[cause_code], prob] for prob, cause_code in zip(probas[0], model.classes_)],
            columns = ['Fire cause', 'Probability']
        )
        output = output.sort_values('Probability', ascending=False)
        Q3_OUTPUT_HANDLER.clear_output()
        display(output)
    

def plot_q3(model):
    ''' Main function to show the predictions for Q3. '''

    Q3_BUTTON.on_click(partial(__predict_fire_cause, model))
    display_widgets(Q3_SIZE_TEXT, Q3_LAT_TEXT, Q3_LON_TEXT, Q3_DATE_PICKER, Q3_BUTTON, Q3_OUTPUT_HANDLER)

