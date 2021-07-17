##############################################################################
#                           DATA MANIPULATOR SCRIPT
##############################################################################
# The purpose of this script is to take the raw user_records data and transform
# it into 'user interaction matrix' form and merge it with the user flair data 
# so that we have a data frame where each row refers to a user, lists their 
# ideology and the amount of times they have commented/posted into different
# subreddits 

# import packages
import pandas as pd 
import numpy as np

# load user-history data 
user_records = pd.read_csv("/Users/pkitc/Desktop/Michael Honours Stuff/user_records_complete.csv")
# create frequency column
user_records['freq'] = 1
# summarise data
user_records = user_records.groupby(['user','subreddit'])['freq'].sum().reset_index(name='freq')

# split data into chunks and create a data frame in which we can recursively take the union of chunks with the data frame
chunker = np.array_split(user_records, 1000)
chunker_pivoted = []

# loop through chunks and concat them with the existing union of chunks 
counter=0
for chunk in chunker:
    
    chunk_to_add = chunk.pivot(index="user", columns="subreddit", values ="freq")
    chunker_pivoted.append(chunk_to_add)
    print(counter)
    counter += 1

union = pd.concat(chunker_pivoted)

del chunk, chunk_to_add, chunker, chunker_pivoted, counter, user_records


# check that this has worked as intended 
union.sum(axis=0,skipna=True)
# we expect this to be false as one users post/comment history may be split over chunks
union.index.is_unique
# we group by the index (username) and combine records for duplicate entries of the same user 
union = union.groupby(union.index).sum()
# we now expect this to be true 
union.index.is_unique

# we now load the user_flair and modify it so that it uses usernames as its index
user_flair = pd.read_csv("/Users/pkitc/Desktop/Michael Honours Stuff/user_flair.csv")
user_flair.index = user_flair['user']
user_flair.drop('user', inplace=True,axis=1)

# merge ideology labels data with the digital footprint data 
data = user_flair.join(union, how="inner")

##############################################################################
#                           END OF SCRIPT
##############################################################################



union.groupby(union.index).sum()
