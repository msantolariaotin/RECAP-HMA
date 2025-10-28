###
## HMA SR 
##
###

I have adapted the work done by Mickael Lalande(links below), to extract daily data from two small subdomains at a higher resolution of HMA SR dataset

All his work is described here:

https://sourcesup.renater.fr/wiki/wiki-glace/library:external:mickael_lalande_modelling_climate_trends_and_variability_in_the_himalaya_to_understand_cryosphere_changes_2020-2023_cosupervised_by_g._krinner_and_m._menegoz

https://github.com/mickaellalande/PhD/tree/master/SCF_parameterizations/0_aggregation

Data informatin can be found here:

High Mountain Asia UCLA Daily Snow Reanalysis, Version 1
Data set id: HMA_SR_D
DOI: 10.5067/HNAUGJQXSCVU

Liu, Y., Fang, Y. & Margulis, S. A. (2021). High Mountain Asia UCLA Daily Snow Reanalysis. (HMA_SR_D, Version 1). [Data Set]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/HNAUGJQXSCVU. [describe subset used if applicable]. Date Accessed 10-28-2025.


https://nsidc.org/data/hma_sr_d/versions/1

Please see the User Guide before: https://nsidc.org/sites/default/files/hma_sr_d-v001-userguide_1.pdf

How to run scripts:
Usually there is a notebook that will describe the procedure of the script for one year as an example, and the associated .py where I run in bash introducing the year with 'sys'.


The raw data is composed by tiles, you can see it as for each degree of latitude, there are the number of longitude where there are aggroupated all the pixel at almost 500 m of resolution.

Step 0: aggregation of files at raw resolution for a subdomain and coarsen grid to 7km

To see an example (one year):
method_snow_HMA_SR_aggregation_step0.ipynb

To run:

for yr in $(seq 1999 2016);do
python method_snow_HMA_SR_aggregation_step0_byyear.py ${yr}
done

This script will select a subdomain HK (Hindu Kush region) and CH (Central Himalaya) that was used to compare MAR simulations  over the Pamir and Nepal (Santolaria-Otín et al., in prep). 

Then aggregate by average all the pixels at 500 m resolutions over a 7kmx7km domain, to do so we use the coarsen function in python and masking the permanent snow in HMA SR which is not good:
https://docs.xarray.dev/en/stable/generated/xarray.DataArray.coarsen.html

HMA_SR_resolution is 16 arc sec ~ 0.493 km; 

7 km (~ resolution wanted)= N x 0.493 km => N = 7/ 0.493= 14 ~ 15 ( to use multiple 5 in coarsen f(x))

method_snow_HMA_SR_aggregation_step0_byyear.py

Step1: aggregation of files at 7km of the subdomain and create one dataset

To see an example (one year):
method_snow_HMA_SR_aggregation_step1.ipynb

To run:

for yr in $(seq 1999 2016);do
python method_snow_HMA_SR_aggregation_step1_byyear.py ${yr}
done

