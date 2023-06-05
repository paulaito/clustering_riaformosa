import geopandas as gpd
import pandas as pd

# Inputs
sg_habitats_gpkg = "./clustering_riaformosa/data/habitats/seagrass_carmen.gpkg"
sm_habitats_gpkg = "./clustering_riaformosa/data/habitats/saltmarsh_carmen.gpkg"

# Outputs
#habitats_gpkg = "./clustering_riaformosa/output/habitats/all_habitats.gpkg"

sg_habitats_out = "./clustering_riaformosa/output/habitats/sg_habitats.gpkg"
sg_intertidal_out = "./clustering_riaformosa/output/habitats/sg_intertidal_habitats.gpkg"
sm_habitats_out = "./clustering_riaformosa/output/habitats/sm_habitats.gpkg"
sm_low_out = "./clustering_riaformosa/output/habitats/sm_low_habitats.gpkg"

# Read
sg_habitats = gpd.read_file(sg_habitats_gpkg)
sm_habitats = gpd.GeoDataFrame(gpd.read_file(sm_habitats_gpkg))

sm_habitats = sm_habitats.to_crs(sg_habitats.crs)

# Arrange 'habitat_class' in saltmarsh ds
sm_habitats_dict = {1: 'saltmarsh_low',
               2: 'saltmarsh_middle',
               3: 'saltmarsh_high'
               }

## Readjust cluster labels
sm_habitats['habitat_class'] = gpd.GeoDataFrame(sm_habitats['Community']).replace(sm_habitats_dict)
sm_habitats.to_crs(sg_habitats.crs)

# Arrange 'habitat_class' in saltmarsh ds
sg_habitats_dict = {'seagrass_intertidal': 'seagrass_intertidal',
                'seagras_intertidal': 'seagrass_intertidal',
                'seagrass_subtidal': 'seagrass_subtidal',
                'seg': 'seagrass_intertidal'
}

sg_habitats['habitat_class'] = gpd.GeoDataFrame(sg_habitats['habitat_class']).replace(sg_habitats_dict)
sg_habitats['habitat_class'] = sg_habitats['habitat_class'].fillna('seagrass_unknown')

# Create object with 'habitat_class' columns
sm_habitats_habitat_class = sm_habitats['habitat_class']
sg_habitats_habitat_class = sg_habitats['habitat_class']

# Buffer vector with 0. 
## This step is important to remove "self-intersection" in features, which raise a problem later on in case it is not solved.
sg_habitats = gpd.GeoDataFrame(sg_habitats.buffer(0))
sm_habitats = gpd.GeoDataFrame(sm_habitats.buffer(0))

## The buffering process ends up removing all columns, so we must add 'habitat_class' column back,
### and rename the geometry column as it was before (i.e. as it must be)
sg_habitats['habitat_class'] = sg_habitats_habitat_class
sm_habitats['habitat_class'] = sm_habitats_habitat_class

sg_habitats = sg_habitats.rename(columns={0:'geometry'})
sm_habitats = sm_habitats.rename(columns={0:'geometry'})

sg_habitats = gpd.GeoDataFrame(sg_habitats)
sm_habitats = gpd.GeoDataFrame(sm_habitats)

sg_habitats_intertidal = sg_habitats.loc[sg_habitats['habitat_class'] == 'seagrass_intertidal']
sm_low_habitats = sm_habitats.loc[sm_habitats['habitat_class'] == 'saltmarsh_low']

sm_low_habitats.to_file(sm_low_out)
sg_habitats_intertidal.to_file(sg_intertidal_out)
sg_habitats.to_file(sg_habitats_out)
sm_habitats.to_file(sm_habitats_out)
