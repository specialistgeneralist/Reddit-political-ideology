################################################################################
# Preparing data
################################################################################

# Load the necessary packages
import pandas as pd
from statistics import mean
from readability import Readability
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
import re
from bs4 import BeautifulSoup

# nltk.download('stopwords')

# Load data
data = pd.read_csv('user_corpus.csv')
data.columns = ['user', 'comment', 'subreddit', 'user.flair']

# Ensure all comments are strings and remove any rows that have no comment recorded
data['comment'] = data['comment'].astype(str)
data = data[pd.notnull(data['comment'])]

################################################################################
# Preparing Metadata 
################################################################################

# Create a function to get the length of each comment (in terms of words)
def GetLen(comment): return len(comment.split())
# Create a new column for column length
data['len'] = data['comment'].apply(GetLen)

# Create dataset containing the max, min and average length of comments for each user
meta_data_df1 = data.groupby(['user', 'user.flair'])['len'].agg(['max', 'min', 'mean']).reset_index()

# Create functions that take a concat of comments as arguments and output SMOG and Flesch Kincaid readaibility scores
def TrySmog(comment):
  try:
    smog = int(Readability(comment).smog().grade_level)
  except Exception:
    smog = 'NA'
  return(smog)

def TryFK(comment):
  try:
    FK = int(Readability(comment).flesch_kincaid().grade_level)
  except Exception:
    FK = 'NA'
  return(FK)

# Create dataset containing the number of unique words, SMOG readaibility and Flesch Kinaid readaibility of the concat of a user's comments
meta_data_df2 = data.groupby(['user', 'user.flair'])['comment'].apply(' '.join).reset_index().assign(
  unique_words = lambda df: df['comment'].map(lambda comment: len(set(comment.split())))).assign(
    smog_grade = lambda df: df['comment'].map(lambda comment: TrySmog(comment))).assign(
    fk_grade = lambda df: df['comment'].map(lambda comment: TryFK(comment)))

# We must now merge our two data frames to gain a final dataframe with meta data on comments for all users
meta_data_df1.set_index('user')
meta_data_df2.set_index('user')
metadata = pd.concat([meta_data_df1, meta_data_df2], axis=1, join='inner')

# Export cleaned meta data to csv to use in modelling
metadata.to_csv('nlp_metadata.csv')

del meta_data_df1, meta_data_df2, metadata

################################################################################
# Preparing cleaned and stemmedd data
################################################################################

# Create a function to clean and stem text to be used in TF-IDF models
stop_words = stopwords.words('english')
porter = PorterStemmer()

def CleanText(text):
  text = BeautifulSoup(text, "lxml").text
  text = re.sub(r'\|\|\|', r' ', text) 
  text = re.sub(r'http\S+', r'<URL>', text)
  text = text.encode('ascii', 'ignore').decode('ascii')

  text = text.lower()
  text = word_tokenize(text)
  text = [word for word in text if word.isalpha()]    
  text = [word for word in text if word not in stop_words]
  text = [porter.stem(word) for word in text]   
  text = " ".join(text)

  return text

# Group data by user so each row corresponds to a user and all of their comments are concated 
data_grouped = data.groupby(['user', 'user.flair'])['comment'].apply(' '.join).reset_index()

# Create a column of cleaned text to be used in TF-IDF models
data_grouped['comment'] = data_grouped['comment'].apply(CleanText)

# Export cleaned data to a csv to use in models
data_grouped.to_csv('nlp_cleaned_data.csv')

del data_grouped

################################################################################
# Preparing raw text concat
################################################################################

# Group data by user so each row corresponds to a user and all of their comments are concated 
data_grouped = data.groupby(['user', 'user.flair'])['comment'].apply(' '.join).reset_index()

# Export cleaned data to a csv to use in models
data_grouped.to_csv('nlp_concat_data.csv')


