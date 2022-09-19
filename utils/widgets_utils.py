''' Files to keep widgets and their constants. '''

import ipywidgets as widgets

MINIMUM = 0
DEFAULT = 1
MAXIMUM = 2

MONTHS_PER_BIN = (3, 5, 12) #minimum, default, maximum
TOP_N_COUNTIES = (1, 3, 20)
YEARS_RANGE = (1992, 2015)

Q1_OUTPUT_HANDLER = widgets.Output()

Q1_SLIDER = widgets.IntSlider(
        value=MONTHS_PER_BIN[DEFAULT],
        min=MONTHS_PER_BIN[MINIMUM],
        max=MONTHS_PER_BIN[MAXIMUM],
        step=1,
        description='Months/bin: ',
        continuous_update=False
    )

Q2_OUTPUT_HANDLER = widgets.Output()

Q2_TEXT = widgets.BoundedIntText(
    value=TOP_N_COUNTIES[DEFAULT],
    min=TOP_N_COUNTIES[MINIMUM],
    max=TOP_N_COUNTIES[MAXIMUM],
    step=1,
    description='Top N: '
)

Q2_SLIDER = widgets.IntRangeSlider(
    value=[min(YEARS_RANGE), max(YEARS_RANGE)],
    min=min(YEARS_RANGE),
    max=max(YEARS_RANGE),
    step=1,
    description='Time span: ',
    continuous_update=False
)

Q3_OUTPUT_HANDLER = widgets.Output()

Q3_SIZE_TEXT = widgets.FloatText(
    value=0,
    description='Fire size (in acres): '
)

Q3_LAT_TEXT = widgets.FloatText(
    value=0,
    description='Latitude (as decimal): '
)

Q3_LON_TEXT = widgets.FloatText(
    value=0,
    description='Longitude (as decimal): '
)

Q3_DATE_PICKER = widgets.DatePicker(
    description='Pick a date between 1992 and 2015'
)

Q3_BUTTON = widgets.Button(
    description='Predict probabilities',
    button_style='info',
    icon='check'
)
