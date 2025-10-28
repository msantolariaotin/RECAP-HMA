'''
for yr in $(seq 2000 2016);do
python method_snow_HMA_SR_aggregation_step0_byyear.py ${yr}
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


# define lat/lon selection range
#domain='HK'
#print(domain)
#lat_min, lat_max = 35, 43;
#lon_min, lon_max = 66, 79;

domain='CH'
print(domain)
lat_min, lat_max = 24, 32
lon_min, lon_max = 80, 91


path_out_main = '/bettik/PROJECTS/pr-regional-climate/santolam/HMA_SR_daily_7km_'+domain+'/'+str(WY0)
os.makedirs(path_out_main, exist_ok=True)

path = '/bettik/PROJECTS/pr-regional-climate/inputs/HMA_SR_D/'+str(WY0)+'/'

path_out = '/bettik/PROJECTS/pr-regional-climate/santolam/HMA_SR_daily_7km_'+domain+'/'+str(WY0)+'/'

##HMA_SR_daily_7km_CH

list_files =glob.glob((path+f'HMA_SR_D_v01_N*_*E*_0_agg_16_WY{str(WY0)}_{str(WY1)}_SD_POST.nc'))

fileNames = [os.path.basename(f) for f in list_files]
#    for ds_name in ['SD_POST']:
#        print(ds_name)
#        list_files = [f for f in os.listdir(path) if ds_name in f]

#print(list_files[0:10])
print(fileNames[0:2])


#

##Selecting subdomain range, year and taking only SD_Post and Mask
year=str(WY0)
# base directory
data_dir = f"/bettik/PROJECTS/pr-regional-climate/inputs/HMA_SR_D/{year}/"


# regex to extract N## and E### from filenames
pattern = re.compile(r"N(\d+)_0E(\d+)_")

# lists to store filepaths
sd_post_files = []
mask_files = []

# loop through directory files
for fname in os.listdir(data_dir):
    match = pattern.search(fname)
    if match:
        lat = int(match.group(1))
        lon = int(match.group(2))
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            fullpath = os.path.join(data_dir, fname)
            if fname.endswith("_SD_POST.nc"):
                sd_post_files.append(fullpath)
            elif fname.endswith("_MASK.nc"):
                mask_files.append(fullpath)

# sort alphabetically (optional, but helps align lat/lon ordering)
sd_post_files.sort()
mask_files.sort()

#print("SD_POST files:")
#for f in sd_post_files:
#    print(f)

#print("\nMASK files:")
#for f in mask_files:
#    print(f)
    
for k in range(len(sd_post_files)):
    #print(k)
    ds_test=xr.open_dataset(sd_post_files[k])['SD_Post']
    ds_mask_test=xr.open_dataset(mask_files[k])['Non_seasonal_snow_mask']
    ds_new_test=ds_test.isel(Stats=0).where(ds_mask_test== 0).coarsen(Latitude=15, Longitude=15).mean()
#print(ds_new_test)
    fileName_new= sd_post_files[k].split('/'+str(year)+'/')[1].split('.nc')[0]+ '_MASKED_coarsen15x15.nc'
#path = '/mnt/lalandmi/equipes/C2H/HMASR/HMA_SR_D/'+WY+'/'
    path_out = f'/bettik/PROJECTS/pr-regional-climate/santolam/HMA_SR_daily_7km_{domain}/{year}/'   
    ds_new_test.to_netcdf(path_out+fileName_new)
print('save:',path_out)