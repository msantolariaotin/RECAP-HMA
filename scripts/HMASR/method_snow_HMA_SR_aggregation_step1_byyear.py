'''
for yr in $(seq 1999 2016);do
python method_snow_HMA_SR_aggregation_step1_byyear.py ${yr}
done

'''

import xarray as xr
import pandas as pd
import numpy as np
import calendar as cld
import matplotlib.pyplot as plt
#import proplot as plot # New plot library (https://proplot.readthedocs.io/en/latest/)
#plot.rc['savefig.dpi'] = 300 # 1200 is too big! #https://proplot.readthedocs.io/en/latest/basics.html#Creating-figures
from scipy import stats
import xesmf as xe # For regridding (https://xesmf.readthedocs.io/en/latest/)

import glob
import os
import re
import sys

WY0=int(sys.argv[1]) #[WY_list[i]][0]
print(WY0)
WY1=str((WY0+1))[-2:]
print(WY1)

domain='HK'
lat_min, lat_max = 35, 43
lon_min, lon_max = 66, 79


path= f'/bettik/PROJECTS/pr-regional-climate/santolam/HMA_SR_daily_7km_{domain}/'+str(WY0)+'/'

list_files =glob.glob((path+f'HMA_SR_D_v01_N*_0E*_0_agg_16_WY{str(WY0)}_{str(WY1)}_SD_POST_MASKED_coarsen15x15.nc'))

fileNames = [os.path.basename(f) for f in list_files]

print(fileNames[0:2])

ds_raw = xr.open_mfdataset(path+f'HMA_SR_D_v01_N*_0E*_0_agg_16_WY{str(WY0)}_{str(WY1)}_SD_POST_MASKED_coarsen15x15.nc', parallel=True)

ds=ds_raw['SD_Post']
ds = ds.assign_coords(Day=pd.date_range(start=str(WY0)+'-10-01', periods=ds.Day.size, freq='D'))
ds = ds.rename({'Longitude': 'lon', 'Latitude': 'lat', 'Day': 'time'}).transpose("time", "lat", "lon")
ds.to_netcdf(path+f'HMA_SR_D_v01_WY{str(WY0)}_{str(WY1)}_{domain}_lat{lat_min}N{lat_max}N_lon{lon_min}E{lon_max}E_SD_POST_MASKED_coarsen15x15.nc')

print('save',path+f'HMA_SR_D_v01_WY{str(WY0)}_{str(WY1)}_{domain}_lat{lat_min}N{lat_max}N_lon{lon_min}E{lon_max}E_SD_POST_MASKED_coarsen15x15.nc')