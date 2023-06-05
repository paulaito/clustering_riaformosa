# Merge clustered data with points data and export as gpkg
import geopandas as gpd
import pandas as pd

# Inputs
clustered_csv = './clustering_riaformosa/output/velocity_analysis/cluster/velcat_clustered.csv'
points_csv = './clustering_riaformosa/data/velocity_analysis/selected_points.csv'

# Output
points_velcat = "./clustering_riaformosa/output/velocity_analysis/cluster/velcat_clustered_points.gpkg"

clustered = pd.read_csv(clustered_csv)
points = pd.read_csv(points_csv).rename(columns={'file_id':'site_id'})

points_gdf = gpd.GeoDataFrame(
    points, geometry=gpd.points_from_xy(points.centroid_X, points.centroid_Y)
)

points_clustered = clustered.merge(points_gdf, on="site_id")

gpd.GeoDataFrame(points_clustered).to_file(points_velcat, driver="GPKG")