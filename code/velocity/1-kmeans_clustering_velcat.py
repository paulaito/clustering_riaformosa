# Clustering data_velocity

# K-means clustering
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq, whiten
import seaborn as sns

# Input
velcat_analysis = "./data_velocity/data/velocity_analysis/table_velcat_analysis.csv"

# Output
out_clustered = "./clustering_riaformosa/data/velocity_analysis/cluster/velcat_clustered.csv"
hist_clusters_img = "./clustering_riaformosa/data/velocity_analysis/cluster/img/velcat_clusters.png"

# Read CSV (obs. columns with sd == 0 have already been removed!)
table_velcat = pd.read_csv(velcat_analysis)

# Create list with site_ids, then set it as index
site_id = pd.DataFrame(table_velcat['site_id'])
table_velcat = table_velcat.set_index('site_id')
vel_intervals = table_velcat.columns.tolist()

# Create pandas DataFrame with normalized data (whiten())
velcat_df = pd.DataFrame(whiten(table_velcat))
scaled_intervals = velcat_df.columns

# Add site_id column and set it as idex
velcat_df['site_id'] = site_id
velcat_df = velcat_df.set_index('site_id')

## Plotting Elbow plot
#distortions = []
#num_clusters = range(2,7)
#
#for i in num_clusters:
#    centroids, distortion = kmeans(velcat_df, i, seed = 1)
#    distortions.append(distortion)
#
#elbow_plot_data = pd.DataFrame({'num_clusters': num_clusters, 'distortions': distortions})
#sns.lineplot('num_clusters', 'distortions', data = elbow_plot_data)
#plt.show()

# Create cluster centers and labels
cluster_centers,_ = kmeans(velcat_df, 3, iter=300, seed = 2)
velcat_df['velcat_raw'],_ = vq(velcat_df, cluster_centers)

# Analyze plots and understand created clusters
# - analyze which has more higher speed counts
velcat_df.groupby('velcat_raw')[scaled_intervals].min().plot(xlabel = 'cluster (raw)', kind='bar')
plt.show()

# Define velocity labels (1 to 3) according to plot 
vel_cats = {0: 1, # lowest  speed
            1: 3, # highest speed
            2: 2, # medium speed
}

# Readjust cluster labels
velcat_df['vel_cat'] = velcat_df['velcat_raw'].replace(vel_cats)

velcat_df.groupby('vel_cat')[scaled_intervals].mean().plot(xlabel = 'cluster (adjusted)', kind='bar')
plt.legend(vel_intervals, ncol=len(vel_intervals)/2, loc="upper left", mode='expand')
plt.show()
#plt.savefig(hist_clusters_img)

velcat_df = velcat_df.drop('velcat_raw', axis=1)

# Write csv
velcat_df.to_csv(out_clustered)


