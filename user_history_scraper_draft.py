#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 19:04:06 2021

@author: michaelkitchener
"""

# import the required packages 
import praw 
import pandas as pd 

# authenticate 
reddit = praw.Reddit(
    client_id='UWy7KqSIIbRZFg', 
    client_secret='fk9U_vzAwJdp4J2qouixpR-97mI',
    user_agent='scrape dawg'
    )

# this function goes through as much of a users comment and post history as possible (how much??)
def UserData(user):

    global user_records
    # set up the PRAW redditor object for the user in question    
    redditor = reddit.redditor(user)
    
    # loop through as much of the users comment history as possible
    for comment in redditor.comments.new(limit=None):
        
        # for each comment, save the text, score, time of creation and subreddit it was made in
        body = comment.body 
        score = comment.score 
        time = comment.created_utc
        subreddit = comment.subreddit 
        
        # save this information in a liist
        row = [user, 'comment', None, body, score, time, subreddit]
        
        # add it to the record as an additional 'row'
        user_records.append(row)
        
    # loop through as much of the users post history as possible    
    for submission in redditor.submissions.new(limit=None):

        # for each post, save the title, text, score, time of creation and subreddit it was made in
        title = submission.title
        selftext = submission.selftext 
        score = submission.score 
        time = submission.created_utc 
        subreddit = submission.subreddit 

        # add it to the record as an additional 'row'        
        row = [user, 'post', title,  selftext, score, time, subreddit]
 
        # add it to the record as an additional 'row'
        user_records.append(row)
      
        
    # turn the list of post and comment info into a datagrame   
    user_records_data = pd.DataFrame(user_records, 
                                 columns = ['user','interaction_type','title',
                                            'body','score','time','subreddit']) 
    
    
    # update the .csv file with tthis users info      
    user_records_data.to_csv('user_records.csv', mode='a', index=False, header=False)
    
    # clear the list for the next user
    user_records = []


# create a blank list to store the rows describing a users comment or post 
# columns will be:
# user|interaction_type|title|body|score|time|subreddit
user_records = []
user_records_data = pd.DataFrame(columns=['user','interaction', 'title','body',
                                          'score','time','subreddit']).to_csv('user_records.csv', index=False)


# here we can run the UserData function with various flaired users as the input
