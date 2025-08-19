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
    client_id='XXXX', 
    client_secret='YYYY',
    user_agent='scrape dawg'
    )

# store  the subreddit class object for the political compass memes subreddit
pcm = reddit.subreddit('PoliticalCompassMemes') 

# create some empty lists which will be used to store users and their flairs
user_flair = pd.DataFrame(columns=['user','flair']).to_csv('user_flair.csv', index=False)
users = []
flairs = []
users_unique = []

# variable to count how many posts we have gone through
post_count = 1


# loop through top posts on the political compass memes subreddit
for post in pcm.top('all', limit=None):
    
    # print the post title and the number 
    print('We are now looking at post number #: ' + str(post_count))
    print('This post is titled ' + post.title)
    
    # load up all the (first level) comments in the post 
    post.comments.replace_more(limit=None)
    comment_queue = post.comments[:]  

    # loop through all the comments in the post 
    while comment_queue:
        comment = comment_queue.pop(0)
        
        # check if 1) the author is flaired, 2) not already recorded and 3) not private
        if (
             comment.author_flair_text not in [None, ''] and   
             str(comment.author) not in users_unique and   
             comment.author != None   
            ):
            
                # if so, save their user name to the users list and flair to the flairs list
                redditor = str(comment.author)
                flair = comment.author_flair_text
                flairs.append(flair)
                users.append(redditor)
                users_unique.append(redditor)

        # this adds the comments replies to the list of comments so we go through all
        comment_queue.extend(comment.replies)  

        # if the current number of users is in the list is multiple of specified number then:
        if len(users) == 100:
            
            # convert the user and flair lists to pandas series so we can merge them into a dataframe 
            user_series = pd.Series(users)
            flair_series = pd.Series(flairs)
            # merge the series to create a dataframe where each row list a username and the flaired ideology 
            user_flair = pd.concat([user_series,flair_series], axis=1)
            
            # update the data frame with the current set of users and flairs
            user_flair.to_csv('user_flair.csv', mode='a', index=False, header=False)
            
            # empty the lists 
            users = []
            flairs = []
                       
            # report the current number of unique users whos username and flair we have recorded 
            print(len(users_unique))
           

# How many comments does it get from each post? Limit of 1000 too?
# How can I get it to get new daily posts

# Changes made:
    # nowloop through top posts of all time (more comments)
    # provides an update every 1000posts
    # got rid of the loopbreaker - it was uncecessary
    # there are going to be diminishingreturns when looking at user/flaurs through posts
    # so, collection will get slower and slower 
