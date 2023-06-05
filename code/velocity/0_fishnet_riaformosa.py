# Create fishnet in Ria Formosa extent

## (Code adapted from spatial-dev.guru)
## https://spatial-dev.guru/2022/05/22/create-fishnet-grid-using-geopandas-and-shapely/

import geopandas as gpd
from shapely import geometry

# Input and output
sm_habitats_gpkg = "./clustering_riaformosa/output/habitats/sm_habitats.gpkg" # it crosses through entire Ria
fishnet_gpkg = "./clustering_riaformosa/output/fishnet_riaformosa.gpkg"

# Single grid (square) size in meters
square_size = 50

# Read gdf
gdf = gpd.read_file(sm_habitats_gpkg).to_crs('3763')

# Get the extent of the shapefile
total_bounds = gdf.total_bounds
# Get minX, minY, maxX, maxY
minX, minY, maxX, maxY = total_bounds
# Create a fishnet
x, y = (minX, minY)
geom_array = []

while y <= maxY:
    while x <= maxX:
        geom = geometry.Polygon([(x,y), (x, y+square_size), (x+square_size, y+square_size), (x+square_size, y), (x, y)])
        geom_array.append(geom)
        x += square_size
    x = minX
    y += square_size
    
fishnet = gpd.GeoDataFrame(geom_array, columns=['geometry']).set_crs('EPSG:3763')
fishnet.to_file(fishnet_gpkg, driver='GPKG')