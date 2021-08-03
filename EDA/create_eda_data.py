# Import the necessary packages
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.preprocessing import Binarizer 


# Load data
data = pd.read_parquet('/Users/pkitc/Desktop/Michael/Thesis/data/user-interaction.parquet')

# Recode flairs
data.replace(':CENTG: - Centrist','centrist', inplace=True)
data.replace(':centrist: - Centrist','centrist', inplace=True)
data.replace(':centrist: - Grand Inquisitor','centrist', inplace=True)
data.replace(':left: - Left', 'left', inplace=True)
data.replace(':libright: - LibRight', 'libright', inplace=True)
data.replace(':libright2: - LibRight', 'libright', inplace=True)
data.replace(':right: - Right',  'right', inplace=True)
data.replace(':libleft: - LibLeft', 'libleft', inplace=True)
data.replace(':lib: - LibCenter', 'libcenter', inplace=True)
data.replace(':auth: - AuthCenter','authcenter', inplace=True)
data.replace(':authleft: - AuthLeft','authleft', inplace=True)
data.replace(':authright: - AuthRight','authright', inplace=True)

################################################################################
################################################################################
#   Analyzing proportion of total comments
################################################################################
################################################################################

################################################################################
#   Proportion of comments per ideology
################################################################################

# Group data by flair to get the sum of all posts/comments in each subreddit by user flair
grouped_data = data.groupby('user.flair').sum()
sum_grouped_data = grouped_data.sum().sort_values(ascending = False)
grouped_data = grouped_data[sum_grouped_data.index[1:]]

# Can sum columns and divide each cell by sum to get proportion of total comments in subreddit X by people of each ideology
# Can also sum rows and divide each cell by this to get proportion of total comments from that ideology in that subreddit

# Divide by rowwise sum (cell represents the proportion of all comments from ideology i in subreddit j)
grouped_data_row = grouped_data.div(grouped_data.sum(axis=1), axis=0)

# Reindex in a logical order
grouped_data_row = grouped_data_row.reindex(['authleft', 'left', 'libleft', 'libcenter', 'centrist', 'authcenter', 'libright', 'right', 'authright'])

# Export to parquet
grouped_data_row.to_parquet('/Users/pkitc/Desktop/Michael/Thesis/data/eda_prop.parquet')

################################################################################
#   Distribution of comments per ideology
################################################################################
# Load data
data = pd.read_parquet('/Users/pkitc/Desktop/Michael/Thesis/data/user-interaction.parquet')

# Create list of relevant subreddits
subreddits = ['user.flair','depression','Anxiety','OCD','bipolar','Bitcoin','wallstreetbets','conspiracy',
  'lgbt', 'AgainstHateSubreddits','TwoXChromosomes', 'MensRights', 'FemaleDatingStrategy',
  'MGTOW2','anime','MMA','Minecraft','movies','gaming','sports']

# Select only relevant columns
data = data[subreddits]

# Export to parquet 
data.to_parquet('/Users/pkitc/Desktop/Michael/Thesis/data/eda_dist.parquet')
