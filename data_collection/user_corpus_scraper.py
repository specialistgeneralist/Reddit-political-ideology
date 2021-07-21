#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 14:20:19 2021

@author: michaelkitchener
"""

import pandas as pd 
from pmaw import PushshiftAPI

user_flair = pd.read_csv('~/Desktop/WORK/Monash/Thesis/Data Collection/Complete Data/user_flair.csv')
user_flair.index = user_flair['user']

api = PushshiftAPI()

def UserData(user):
    
    comments = api.search_comments(author= user, limit=100, subreddit = '!PoliticalCompassMemes')
    comments_df = pd.DataFrame(comments)[['author','body','subreddit']]
    comments_df['flair'] = user_flair.loc[user,'flair']
    
    user_corpus = pd.DataFrame(comments_df,  columns=['author','body','subreddit','flair'])
    user_corpus.to_csv('user_corpus.csv', mode='a', index=False, header=False)
 
counter=1
for user in user_flair['user'][1:15]:
    try: 
        UserData(user)
        print(counter)
        counter += 1   
    except KeyError:
        pass


# comments = api.search_comments(author= [user for user in user_flair['user'][1:30]], 
                               limit=100, subreddit = '!PoliticalCompassMemes')
















