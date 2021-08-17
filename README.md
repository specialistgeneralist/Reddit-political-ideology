# RedditIdeology-Honours2021
Files for scraping and modeling reddit users' ideologies 

## Data Collection

1. *user_flair_scraper_draft.py* this script goes through the Political Compass Memes subreddit and records the flair and usernames of flaired users who have commented in the top 1000 most popular posts, it gives us our list of username and associated ideolog.
2. *user_history_scraper_draft.py* this script loops through each username in the list of usernames and ideologies produced by user_flair_scraper_draft.py and logs the ammount of times each user has posted or commented in a specific subreddit.
3. *data_manipulator_complete.py* this script pivots the data file produced by user_history_scraper_draft.py so that each row represents a user, each column a subreddit and each cell how much the relevant user comments/posts in the relevant subreddit, we merge this with our list of users and flairs so that we have a complete data set that can be use for prediction.
4. *user_corpus_scraper.py* this script goes loops through each username in the list of usernames and ideologies produced by user_flair_scraper_draft.py and records the textual content of (a maximum of) 100 comments from each user (with the additional criterion that the comments not be made in the Political Compass Memes subreddit). We process this data to gain features to use in the NLP based models.

## Models

1. *all_class_int_models.py* this script trains, optimizes and validates models designed to predict the ideology of users based on the user-interaction matrix produced by data_manipulator_complete.py (see the Data Collection folder)and produces a csv file that records the exact specification of each model and its accuracy and AUC on a testing set.
2. *econ_int_models.py* does the same but with the task of predicting the economic element of the user's ideology from the user-interaction matrix.
3. *social_int_models.py* does the same but with the task of predicting the social element of the user's ideology from the user-interaction matrix.

## Results

1. *all_int_results.csv* contains a record of each model developed in all_class_int_models.py, its accuracy and auc on training set.
2. *econ_int_results.csv* contains a record of each model developed in econ_class_int_models.py, its accuracy and auc on training set.
3. *social_int_results.csv* contains a record of each model developed in social_class_int_models.py, its accuracy and auc on training set.
4. *svd_k.csv* contains the original variables that contribute most to the first 10 SVD components, it is produced by k_analysis.py.

## EDA

1. *create_eda_data.py* this script produces 1) a version of the user-interaction matrix produced by data_manipulator_complete.py with most columns removed so that it can be easily loaded into memory and used to create some visual analyses of the relationship between ideology and subreddit interaction 2) a grouped and summarised version of the user-interaction matrix for the same purpose.
2. *interactions_eda.R* this script uses the data file produced by create_eda_data.py to create visual analyses of the relationshup between ideology and subreddit interaction.
3. *k_analysis.py* this script uses the user-interaction matrix to 1) produce a graphic of the accuracy of predictions using a varying number of SVD components and 2) produce svd_k.csv.
4. *result_int_viz.R* this script takes the all_int_results.csv, econ_int_results.csv, and social_int_results.csv files and produces graphics illustrating the predictive performance of all the models developed in all_class_int_models.py, econ_class_int_models.py and social_class_int_models.py.

## Write up

This folder contains notes to myself that represent intermediate progress on the final write up and is not relevant to the final thesis.

## Proposal

This folder contains some files used in the project proposal and project presentation in semester 1 and are not relevant to the final thesis.



