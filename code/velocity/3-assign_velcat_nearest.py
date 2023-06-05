# Assign velcat category according to nearest velocity point
from clustering_riaformosa.code.functions import fishnet_overlap
import geopandas as gpd
import pandas as pd
from shapely.ops import nearest_points

# Inputs
fishnet_gpkg = "./clustering_riaformosa/output/habitats/fishnet_riaformosa.gpkg"
sm_habitats_gpkg = "./clustering_riaformosa/output/habitats/sm_habitats.gpkg"
sg_habitats_gpkg = "./clustering_riaformosa/output/habitats/sg_habitats.gpkg"
points_velcat_gpkg = "./clustering_riaformosa/output/velocity_analysis/cluster/velcat_clustered_points.gpkg"

# Outputs
sg_vel_cat_fishnet_gpkg = './clustering_riaformosa/output/velocity_analysis/cluster/sg_velcat_fishnet.gpkg'
sm_vel_cat_fishnet_gpkg = './clustering_riaformosa/output/velocity_analysis/cluster/sm_velcat_fishnet.gpkg'

# Get fishnet features overlapping with habitats
sg_fishnet = fishnet_overlap(fishnet_gpkg, sg_habitats_gpkg)
sm_fishnet = fishnet_overlap(fishnet_gpkg, sm_habitats_gpkg)

# Read velocity points and get geometry
points_velcat = gpd.read_file(points_velcat_gpkg).to_crs(3763)
geoms = points_velcat['geometry']

# Convert into shapely MultiPoint (correct Type to be used in nearest_points)
points_multi = geoms.unary_union

# Get habitat fishnet geometryies
sg_geoms = pd.DataFrame(sg_fishnet['geometry'])
sm_geoms = pd.DataFrame(sm_fishnet['geometry'])

# Create dictionary - keys: geometries; values: cluster_label
dict = pd.Series(points_velcat.vel_cat.values,index=geoms.values).to_dict()

poly_cat_sg = []
poly_cat_sm = []

# Find closest point from each polygon, and set its velcat accordingly
for index,row in sg_geoms.iterrows():
    point_poly, point_velcat_sg = nearest_points(row, points_multi)
    cur_cat_sg = dict[point_velcat_sg[0]]
    poly_cat_sg.append(cur_cat_sg)

for index,row in sm_geoms.iterrows():
    point_poly, point_velcat_sm = nearest_points(row, points_multi)
    cur_cat_sm = dict[point_velcat_sm[0]]
    poly_cat_sm.append(cur_cat_sm)

# Add new column with cluster_label
sg_fishnet['vel_cat'] = poly_cat_sg
sm_fishnet['vel_cat'] = poly_cat_sm

# Save to file
sg_fishnet.to_file(sg_vel_cat_fishnet_gpkg, driver='GPKG')
sm_fishnet.to_file(sm_vel_cat_fishnet_gpkg, driver='GPKG')