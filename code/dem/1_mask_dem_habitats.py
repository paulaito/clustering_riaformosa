from clustering_riaformosa.code.functions import mask_dem

# Inputs
dem_tif = "./clustering_riaformosa/data/dem/riaformosa_dem_ROI_georef_reproj.tif"

sg_habitats_gpkg = "./clustering_riaformosa/output/habitats/sg_habitats.gpkg"
sg_intertidal_gpkg = "./clustering_riaformosa/output/habitats/sg_intertidal_habitats.gpkg"
sm_low_gpkg = "./clustering_riaformosa/output/habitats/sm_low_habitats.gpkg"


# Outputs
dem_sg_tif = "./clustering_riaformosa/output/dem/dem_sg.tif"
dem_sg_intertidal_tif = "./clustering_riaformosa/output/dem/dem_sg_intertidal.tif"
dem_sm_low_tif = "./clustering_riaformosa/output/dem/dem_sm_low.tif"

# Mask dem with habitats geopackages
mask_dem(dem_tif, sg_habitats_gpkg, dem_sg_tif)
mask_dem(dem_tif, sm_low_gpkg, dem_sm_low_tif)
mask_dem(dem_tif, sg_intertidal_gpkg, dem_sg_intertidal_tif)

