#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 22:56:42 2021

@author: pkitc
"""

# Import the necessary packages
import pandas as pd 
import matplotlib.pyplot as plt

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
#   Full classification 
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

# Get a quick barchart of the rowsie data for a specific subreddit
grouped_data_row['stupidpol'].plot.bar()


# Do some cool graphs

ax = grouped_data_row[['OCD','Anxiety','depression','schizophrenia','bipolar']].plot(kind='bar', 
                                                           title = 'Comments in mental health subreddits', 
                                                           figsize=(16, 10),
                                                           legend = True, 
                                                           fontsize = 12)

ax = grouped_data_row[['lgbt','transgender','BlackLivesMatter']].plot(kind='bar', 
                                                           title = 'Comments in identity based subreddits', 
                                                           figsize=(16, 10),
                                                           legend = True, 
                                                           fontsize = 12)

ax = grouped_data_row[['Bitcoin', 'philosophy', 'MachineLearning']].plot(kind='bar', 
                                                           title = 'Comments in mental health subreddits', 
                                                           figsize=(16, 10),
                                                           legend = True, 
                                                           fontsize = 12)

ax = grouped_data_row[grouped_data_row.columns[1:10]].plot(kind='bar', 
                                                           title = 'Comments in mental health subreddits', 
                                                           figsize=(16, 10),
                                                           legend = True, 
                                                           fontsize = 12)

ax = grouped_data_row[grouped_data_row.columns[100:110]].plot(kind='bar', 
                                                           title = 'Comments in mental health subreddits', 
                                                           figsize=(16, 10),
                                                           legend = True, 
                                                           fontsize = 12)

ax = grouped_data_row[grouped_data_row.columns[200:210]].plot(kind='bar', 
                                                           title = 'Comments in mental health subreddits', 
                                                           figsize=(16, 10),
                                                           legend = True, 
                                                           fontsize = 12)

ax = grouped_data_row[grouped_data_row.columns[1000:1010]].plot(kind='bar', 
                                                           title = 'Comments in mental health subreddits', 
                                                           figsize=(16, 10),
                                                           legend = True, 
                                                           fontsize = 12)



for flair in grouped_data_row.index:
  df = grouped_data_row.loc[flair].sort_values(ascending = False)[0:25]
  print('****'*10)
  print(flair.upper())
  print(df)
  
for flair in grouped_data_row.index:
  df = grouped_data_row.loc[flair].sort_values(ascending = False)[100:125]
  print('****'*10)
  print(flair.upper())
  print(df)

################################################################################
#   Economic classification
################################################################################
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

# Recode to economic flair only
data.replace('centrist', 'center', inplace=True)
data.replace('left', 'left', inplace=True)
data.replace('libright', 'right', inplace=True)
data.replace('right','right', inplace=True)
data.replace('libleft', 'left', inplace=True)
data.replace('libcenter', 'center', inplace=True)
data.replace('authcenter', 'center', inplace=True)
data.replace('authleft', 'left', inplace=True)
data.replace('authright','right', inplace=True)
        
grouped_data = data.groupby('user.flair').sum()
sum_grouped_data = grouped_data.sum().sort_values(ascending = False)
grouped_data = grouped_data[sum_grouped_data.index[1:]] 

# Divide by rowwise sum (cell represents the proportion of all comments from ideology i in subreddit j)
grouped_data_row = grouped_data.div(grouped_data.sum(axis=1), axis=0)

# Reindex in a logical order
grouped_data_row = grouped_data_row.reindex(['left','center','right'])

# Analysis 
# [][][][][][][][][][][][][][][][][][]
# [][][][][][][][][][][][][][][][][][]
# [][][][][][][][][][][][][][][][][][]

################################################################################
#   Social classification
################################################################################
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

# Recode to social flair only
data.replace('centrist', 'center', inplace=True)
data.replace('left', 'center', inplace=True)
data.replace('libright', 'lib', inplace=True)
data.replace('right','center', inplace=True)
data.replace('libleft', 'lib', inplace=True)
data.replace('libcenter', 'lib', inplace=True)
data.replace('authcenter', 'auth', inplace=True)
data.replace('authleft', 'auth', inplace=True)
data.replace('authright','auth', inplace=True)
        
grouped_data = data.groupby('user.flair').sum()
sum_grouped_data = grouped_data.sum().sort_values(ascending = False)
grouped_data = grouped_data[sum_grouped_data.index[1:]] 

# Divide by rowwise sum (cell represents the proportion of all comments from ideology i in subreddit j)
grouped_data_row = grouped_data.div(grouped_data.sum(axis=1), axis=0)

# Reindex in a logical order
grouped_data_row = grouped_data_row.reindex(['auth','center','lib'])

# Analysis 
# [][][][][][][][][][][][][][][][][][]
# [][][][][][][][][][][][][][][][][][]
# [][][][][][][][][][][][][][][][][][]












