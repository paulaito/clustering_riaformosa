### 1: fishnet_overlap - get overlapped features between habitat and fishgrid

import geopandas as gpd

def fishnet_overlap(fishnet_gpkg, habitats_gpkg):
    # Read
    fishnet = gpd.read_file(fishnet_gpkg).to_crs(3763)
    habitats = gpd.read_file(habitats_gpkg).to_crs(3763)
    habitat_fish_net = habitats.overlay(fishnet, how='intersection')
    return habitat_fish_net

### 2: mask_dem - mask raster to include only habitat area
import geopandas as gpd
import rasterio as rio
import rasterio.mask
def mask_dem(dem_tif, habitats_gpkg, out_tif):
    # Open raster
    raster_o = rio.open(dem_tif)

    # Open mask, remove empty geometries and set crs (same as 4326)
    sg_mask = gpd.read_file(habitats_gpkg)
    sg_mask_narm = sg_mask[~sg_mask['geometry'].isna()].to_crs(4326)

    # Mask raster with gpkg
    out_image, out_transf = rasterio.mask.mask(raster_o, sg_mask_narm.geometry, invert = False)

    out_meta = raster_o.meta
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transf})
    
    # Write masked raster in disk
    with rio.open(out_tif, 'w', **out_meta) as dst:
            dst.write(out_image)


### 3: mask_dem_cats_gpkg - mask dem categories and export as demcat_habitat geopackages
from rasterio.features import shapes
import geopandas as gp
import fiona
import tempfile
from pathlib import Path
from rasterio.io import MemoryFile
import rasterio as rio
import numpy as np
from rasterio import mask
import pandas as pd

def mask_dem_multiple_cats_gpkg (dem_habitat, min_mid, mid, mid_max, max_value, demcat_habitat_gpkg):
     # Open and read dem tifs
     dem_habitat_o = rio.open(dem_habitat)
     dem_habitat_r = dem_habitat_o.read()

     dem_cat1 = np.where(dem_habitat_r <= min_mid, '1', 'nan')
     dem_cat2 = np.where((min_mid < dem_habitat_r) & (dem_habitat_r <= mid), '2', 'nan')
     dem_cat3 = np.where((mid < dem_habitat_r) & (dem_habitat_r <= mid_max), '3', 'nan')
     dem_cat4 = np.where((dem_habitat_r < max_value) &
                              (dem_habitat_r > mid_max), '4', 'nan')
     profile_ndvi = dem_habitat_o.profile
     
     demcats = [dem_cat1, dem_cat2, dem_cat3, dem_cat4]

     # Loop through all demcats
     
     cats = []
     i = 1

     for demcat in demcats:
        with MemoryFile() as memfile:        
            with memfile.open(**profile_ndvi) as ds:
                ds.write(demcat) # write water-only raster as a memory file

        ### Creating water mask gpkg: polygonize catx-only raster
            cat_mask = None
            with rio.Env():
                with rio.open(memfile) as src:
                    image = src.read(1).astype('float32') # first band
                    results = (
                    {'properties': {'raster_val': v}, 'geometry': s}
                    for i, (s, v) 
                    in enumerate(
                        shapes(image, mask=cat_mask, transform=src.transform)))           
        
        geoms = list(results)
        
        gdf = gpd.GeoDataFrame.from_features(geoms)
        gdf = gdf.dropna()
        gdf = gdf.set_crs(4326)
        gdf = gdf.assign(dem_cat=i)
        cats.append(gdf)

        i += 1
     
     habitats_demcat = gpd.GeoDataFrame(pd.concat(cats, ignore_index=True))
     habitats_demcat.to_file(demcat_habitat_gpkg, driver = 'GPKG')


def mask_dem_two_cats_gpkg (dem_habitat, min, mid, max, demcat_habitat_gpkg):
     # Open and read dem tifs
     dem_habitat_o = rio.open(dem_habitat)
     dem_habitat_r = dem_habitat_o.read()

     dem_cat1 = np.where((dem_habitat_r <= mid) & (dem_habitat_r >= min ), '1', 'nan')
     dem_cat2 = np.where((dem_habitat_r > mid) & (dem_habitat_r <= max), '2', 'nan')

     profile_ndvi = dem_habitat_o.profile
     
     demcats = [dem_cat1, dem_cat2]

     # Loop through all demcats
     
     cats = []
     i = 1

     for demcat in demcats:
        with MemoryFile() as memfile:        
            with memfile.open(**profile_ndvi) as ds:
                ds.write(demcat) # write water-only raster as a memory file

        ### Creating water mask gpkg: polygonize catx-only raster
            cat_mask = None
            with rio.Env():
                with rio.open(memfile) as src:
                    image = src.read(1).astype('float32') # first band
                    results = (
                    {'properties': {'raster_val': v}, 'geometry': s}
                    for i, (s, v) 
                    in enumerate(
                        shapes(image, mask=cat_mask, transform=src.transform)))           
        
        geoms = list(results)
        
        gdf = gpd.GeoDataFrame.from_features(geoms)
        gdf = gdf.dropna()
        gdf = gdf.set_crs(4326)
        gdf = gdf.assign(dem_cat=i)
        cats.append(gdf)

        i += 1
     
     habitats_demcat = gpd.GeoDataFrame(pd.concat(cats, ignore_index=True))
     habitats_demcat.to_file(demcat_habitat_gpkg, driver = 'GPKG')