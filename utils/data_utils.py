''' Utility file to store loading functions.
    When loading a file they first check if the file exists,
    if it does, then the md5 sum must match otherwise
    it will raise an error. '''

import os
import hashlib
import logging
import pickle as pkl
import sqlite3 as sql

from typing import Tuple, Union
from pandas import DataFrame, to_datetime
from geopandas import GeoDataFrame, read_file

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

DB_FILENAME = "files/FPA_FOD_20170508.sqlite"
DB_MD5 = "568e679d022f6df0dc1d23a139cdc2ce"
DB_LINK = "https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires"

RETRIEVAL_QUERY = '''
    select OBJECTID, DISCOVERY_DATE, FIPS_NAME, STATE, FIRE_SIZE, LATITUDE, LONGITUDE, STAT_CAUSE_CODE
    from Fires
'''

STARTING_EPOCH = to_datetime(0, unit='s').to_julian_date()


SHAPEFILES_EXTENSIONS = ('.shp', '.shx', '.dbf')
US_STATES_FILENAME = 'files/st99_d00'
US_STATES_MD5S = ('7250fd0b8f38dfeecec6613c61d63b2c', '005ea08c4d3227e477f7ab48618c7861', '50f74f27cc52d91ebf7e2ce893b6dc47')
US_STATES_LINK = "https://github.com/matplotlib/basemap/tree/master/examples"
US_COUNTIES_FILENAME = 'files/tl_2019_us_county'
US_COUNTIES_MD5S = ('994e2150e134113fa9f145aa8edae916', '47f281444c863727ed2cd82d6ea55326', '548896c7bd489dc5d78eb1958dffe21c')
US_COUNTIES_LINK = "https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-county-and-equivalent-national-shapefile"

ML_FILENAME = "files/lgbm_model.pkl"
ML_MD5 = "afb4d80de26f3fb7348b022e3b73a6cd"

##########################################

def check_md5sum(filename: str, expected_md5sum: str, output_name: str = "File", download_link: str = '') -> bool:
    ''' Function to check the md5 file of the file to be imported and the one expected.
        Params:
            filename: path of the file to load 
            expected_md5sum: expected md5 string of the file to load 
            output_name (optional): how to name the file in logging messages
            download_link (optional): download link of the file '''
    if os.path.exists(filename):
        file_md5 = hashlib.md5(open(filename,'rb').read()).hexdigest()
        if file_md5 == expected_md5sum:
            logging.info(f"{output_name} found")
            return True
        else:
            logging.error(f"{output_name} found but MD5 sum doesn't correspond, please download the file again.")
            if download_link:
                logging.error(download_link)
            return False
    else:
        logging.error(f"{output_name} not found, please download the file from:")
        if download_link:
            logging.error(download_link)
        return False

def load_dataset() -> Union[DataFrame, None]:
    ''' Check if the dataset is present, and load it. '''
    if not check_md5sum(DB_FILENAME, DB_MD5, output_name="Dataset", download_link=DB_LINK):
        return
    
    connection = sql.connect(DB_FILENAME)

    # Once we have the connection we could just import it all
    # into a pandas DataFrame, but to spare some memory I'm just
    # going to import the columns that I need.
    df = DataFrame(
        connection.execute(RETRIEVAL_QUERY).fetchall(),
        columns=['id','date','county','state','size','lat','lon','cause']
    )
    logging.info(f"Dataset loaded")
    return df

def preprocess_dataset(df: DataFrame) -> DataFrame:
    ''' Preprocess the dataset to have all the necessary columns. '''

    # Convert the datetime column in the julian format to a more readable one
    df['datetime'] = to_datetime(df['date'] - STARTING_EPOCH, unit='D')

    # Extract the year out of the date
    # I could have selected the year in the original query but this is
    # more efficient.
    df['year'] = df['datetime'].dt.year

    return df

def load_shapefiles() -> Union[Tuple[GeoDataFrame], None]:
    ''' Check if the shape files of USA are present, and load them. '''
    not_found_files = 0

    for extension, real_md5 in zip(SHAPEFILES_EXTENSIONS, US_STATES_MD5S):
        not_found_files += not check_md5sum(US_STATES_FILENAME+extension, real_md5, output_name=f"US states map {extension}", download_link=US_STATES_LINK)

    # I could have put this code in another nested for loop above to avoid repetitions, but
    # I prefered to keep it like this to make it more readable.
    for extension, real_md5 in zip(SHAPEFILES_EXTENSIONS, US_COUNTIES_MD5S):
        not_found_files += not check_md5sum(US_COUNTIES_FILENAME+extension, real_md5, output_name=f"US counties map {extension}", download_link=US_COUNTIES_LINK)

    if not_found_files:
        logging.error("Loading aborted for missing files")
        return 

    logging.info("Loading shape files as geo dataframes")
    us_states_df = read_file(US_STATES_FILENAME+'.shp')
    us_states_df.crs = "epsg:4326"
    us_states_df = us_states_df.to_crs("EPSG:4269")

    us_counties_df = read_file(US_COUNTIES_FILENAME+'.shp') #read_file(US_COUNTIES_FILENAME+'.shp')
    us_counties_df.crs = "epsg:4326"
    us_counties_df = us_counties_df.to_crs("EPSG:4269")
    logging.info("Loading done")

    return us_states_df, us_counties_df

def load_ml_model():
    ''' Check if the ML model is present, and load it. '''
    if not check_md5sum(ML_FILENAME, ML_MD5, output_name="ML model"):
        return

    with open(ML_FILENAME, mode='rb') as f:
        model = pkl.load(f)

    logging.info(f"ML model loaded")
    
    return model
