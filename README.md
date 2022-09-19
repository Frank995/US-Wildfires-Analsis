# US-Wildfires-Analsis

This repository contains a notebook with the analysis of the open dataset: <a href="https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires">US Wildfires</a>. I'm going to show some preliminary exploratory data analysis and a ML model to answer the following questions:
<ul>
    <li>Have wildfires become more or less frequent over time?</li>
    <li>What counties are the most and least fire-prone?</li>
    <li>Given the size, location and date, can you predict the cause of a fire wildfire?</li>
</ul> 

The code was tested in Python 3.9 but older version may work as well. I would advise to use conda to create a separate environment to make sure it works.

## How to reproduce

<ol>
    <li>Download and extract the repository</li>
    <li>Sign in to Kaggle, download the dataset from the link above, extract the sqlite file and put it in the files folder of the repo<</li>
    <li>Download st99_d00.dbf/.shp/.shx from <a href="https://github.com/matplotlib/basemap/tree/master/examples">here</a> and put them in the files folder</li>
    <li>Download the tl_2019_us_county.zip file from <a href="https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-county-and-equivalent-national-shapefile">here</a>, extract it and put the .dbf/.shp/.shx in the files folder
    <li>(Optional) Create a conda environment with Python 3.9</li>
    <li>Make sure you have the latest version of the requirements or install them anew</li>
</ol> 

You can create a new conda environment by running:
```
conda create -n env_name
```
To install the requirements you need to run:
```
pip install -r requirements.txt
```
