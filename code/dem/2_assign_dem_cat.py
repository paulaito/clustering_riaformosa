# Assign DEM categories on DEM habitats rasters (dem_sg_intertidal.tif and dem_sm.tif)
## and export as gpkg

import rasterio as rio
from clustering_riaformosa.code.functions import mask_dem_two_cats_gpkg
import matplotlib.pyplot as plt
import numpy as np
from rasterio.plot import show_hist

# Inputs (DEM masked habitats)
dem_sg_intertidal_tif = "./clustering_riaformosa/output/dem/dem_sg_intertidal.tif"
dem_sm_low_tif = "./clustering_riaformosa/output/dem/dem_sm_low.tif"

# Output (categorized)
sg_intertidal_dem_cat = "./clustering_riaformosa/output/dem/cluster/sg_dem_cat_intertidal.gpkg"
sm_low_dem_cat = "./clustering_riaformosa/output/dem/cluster/sm_low_dem_cat.gpkg"

hist_sg_intertidal_dem = "./clustering_riaformosa/output/dem/hist/hist_sg_intertidal_dem_values.png"
hist_sm_low_dem = "./clustering_riaformosa/output/dem/hist/hist_sm_low_dem_values.png"


###### SEAGRASS INTERTIDAL ######

# Open and read dem tifs
dem_sg_intertidal_o = rio.open(dem_sg_intertidal_tif)
dem_sg_intertidal_r = dem_sg_intertidal_o.read()

# Define limits of categories
max_value = dem_sg_intertidal_o.statistics(1).max
min_value = dem_sg_intertidal_o.statistics(1).min
median = np.median(dem_sg_intertidal_r[dem_sg_intertidal_r < max_value])

# Assign dem categories to seagrass intertidal
mask_dem_two_cats_gpkg(dem_sg_intertidal_tif, min_value, median, max_value, sg_intertidal_dem_cat)

# Plot histogram
plt.clf()
fig, axhist = plt.subplots(1)
show_hist(dem_sg_intertidal_o, bins=200, histtype='stepfilled',
          lw=0.0, stacked=False, alpha=0.5, ax=axhist)
axhist.set_title('Seagrass intertidal elevation histogram')
axhist.set_xlabel('DEM value')
axhist.get_legend().remove()
plt.savefig(hist_sg_intertidal_dem)


###### SALTMARSH LOW (INTERTIDAL) ######

dem_sm_o = rio.open(dem_sm_low_tif)
dem_sm_r = dem_sm_o.read()

# Define limits
max_value_sm = dem_sm_o.statistics(1).max
min_value_sm = dem_sm_o.statistics(1).min
median_sm = np.median(dem_sm_r[dem_sm_r < max_value_sm])

# Assign dem categories to saltmarsh
mask_dem_two_cats_gpkg(dem_sm_low_tif, min_value_sm, median_sm, max_value_sm, sm_low_dem_cat)

# Plot histogram
plt.clf()
fig, axhist = plt.subplots(1)
show_hist(dem_sm_o, bins=200, histtype='stepfilled',
          lw=0.0, stacked=False, alpha=0.5, ax=axhist)
axhist.set_title('Saltmarsh elevation histogram')
axhist.set_xlabel('DEM value')
axhist.get_legend().remove()
plt.savefig(hist_sm_low_dem)