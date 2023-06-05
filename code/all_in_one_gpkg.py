# Merge dem and velcats into: one gpkg per habitat, and one gpkg with all
import geopandas as gpd
import pandas as pd

# Inputs
sg_vel_cat_fishnet_gpkg = './clustering_riaformosa/output/velocity_analysis/cluster/sg_velcat_fishnet.gpkg'
sg_intertidal_dem_cat = "./clustering_riaformosa/output/dem/cluster/sg_dem_cat_intertidal.gpkg"

sm_vel_cat_fishnet_gpkg = './clustering_riaformosa/output/velocity_analysis/cluster/sm_velcat_fishnet.gpkg'
sm_low_dem_cat = "./clustering_riaformosa/output/dem/cluster/sm_low_dem_cat.gpkg"

# Output
sg_intertidal_vel_dem_cat_gpkg = "./clustering_riaformosa/output/RESULTS/sg_intertidal_vel_dem_cat.gpkg"
sm_low_vel_dem_cat_gpkg = "./clustering_riaformosa/output/RESULTS/sm_vel_dem_cat.gpkg"

# Read files
sg_vel_cat_fishnet = gpd.read_file(sg_vel_cat_fishnet_gpkg).to_crs(3763)
sg_intertidal_vel_cat_fishnet = sg_vel_cat_fishnet.loc[sg_vel_cat_fishnet['habitat_class'] == "seagrass_intertidal"]
sg_intertidal_dem_cat = gpd.read_file(sg_intertidal_dem_cat).to_crs(3763)

sm_vel_cat_fishnet = gpd.read_file(sm_vel_cat_fishnet_gpkg).to_crs(3763)
sm_low_vel_cat_fishnet = sm_vel_cat_fishnet.loc[sm_vel_cat_fishnet['habitat_class'] == "saltmarsh_low"]
sm_dem_cat = gpd.read_file(sm_low_dem_cat).to_crs(3763)

# One gdf per habitat with both cats
sg_intertidal_vel_dem_cat = sg_intertidal_dem_cat.overlay(sg_intertidal_vel_cat_fishnet, how='intersection').dissolve(by=['dem_cat', 'vel_cat'], as_index=False).explode(ignore_index=True)
sm_vel_dem_cat = sm_dem_cat.overlay(sm_low_vel_cat_fishnet, how='intersection').dissolve(by=['dem_cat', 'vel_cat'], as_index=False).explode(ignore_index=True)

vel_cats = {1: 'low_vel',
            2: 'medium_vel',
            3: 'high_vel'
}

dem_cats = {1: 'low_elev',
            2: 'high_elev'
}

# Add categories names
sg_intertidal_vel_dem_cat['vel_cat_name'] = sg_intertidal_vel_dem_cat['vel_cat'].replace(vel_cats)
sg_intertidal_vel_dem_cat['dem_cat_name'] = sg_intertidal_vel_dem_cat['dem_cat'].replace(dem_cats)
sg_intertidal_vel_dem_cat['area_m2'] = sg_intertidal_vel_dem_cat.area

sm_vel_dem_cat['vel_cat_name'] = sm_vel_dem_cat['vel_cat'].replace(vel_cats)
sm_vel_dem_cat['dem_cat_name'] = sm_vel_dem_cat['dem_cat'].replace(dem_cats)
sm_vel_dem_cat['area_m2'] = sm_vel_dem_cat.area

cols = ['habitat_class', 'dem_cat', 'dem_cat_name', 'vel_cat', 'vel_cat_name', 'area_m2', 'geometry']

# Write final results to file! Yay :)
gpd.GeoDataFrame(sg_intertidal_vel_dem_cat[cols]).to_file(sg_intertidal_vel_dem_cat_gpkg, driver='GPKG')
gpd.GeoDataFrame(sm_vel_dem_cat[cols]).to_file(sm_low_vel_dem_cat_gpkg, driver='GPKG')