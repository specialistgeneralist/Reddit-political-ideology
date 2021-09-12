################################################################################
# Preparing data
################################################################################

# Load the necessary packages
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, roc_auc_score, make_scorer
from sklearn.dummy import DummyClassifier
from sklearn.compose import ColumnTransformer
from zeugma.embeddings import EmbeddingTransformer

################################################################################
################################################################################
# Modelling 
################################################################################
################################################################################

# Set up dictionaries to store results 
accuracy_log = {}
auc_log = {}
model_log = {}

# Set up scorer for weighted OVR AUC-ROC
scorer = make_scorer(roc_auc_score, needs_proba = True, multi_class='ovr', average ='weighted')

# Set up ZeroR classifier 
zero_r = DummyClassifier(strategy = "most_frequent")

# Set up object for truncated SVD 
svd = TruncatedSVD(random_state = 0, n_components=500)


# Set up OVR Linear SVM to use in all models 
linear_svc = LinearSVC(loss = 'hinge',
                       multi_class = 'ovr',
                       random_state = 0
                       )


# Set up custom train/validate splot
custom_cv = StratifiedShuffleSplit(test_size = 0.2, n_splits = 1, random_state = 0)


################################################################################
################################################################################
# TF-IDF models
################################################################################
################################################################################

clean_data = pd.read_csv('/Volumes/Elements/Text/nlp_cleaned_data.csv')

# clean_data = clean_data[clean_data['user.flair'] != ':CENTG: - Centrist']
# clean_data = clean_data[clean_data['user.flair'] != ':centrist: - Centrist']
# clean_data = clean_data[clean_data['user.flair'] != ':centrist: - Grand Inquisitor']
# clean_data = clean_data[clean_data['user.flair'] != ':auth: - AuthCenter']
# clean_data = clean_data[clean_data['user.flair'] != ':lib: - LibCenter']

# Recode flair labels to avoid doubling up on flairs 
clean_data.replace(':CENTG: - Centrist','centrist', inplace=True)
clean_data.replace(':centrist: - Centrist','centrist', inplace=True)
clean_data.replace(':centrist: - Grand Inquisitor','centrist', inplace=True)
clean_data.replace(':left: - Left', 'left', inplace=True)
clean_data.replace(':libright: - LibRight', 'libright', inplace=True)
clean_data.replace(':libright2: - LibRight', 'libright', inplace=True)
clean_data.replace(':right: - Right',  'right', inplace=True)
clean_data.replace(':libleft: - LibLeft', 'libleft', inplace=True)
clean_data.replace(':lib: - LibCenter', 'libcenter', inplace=True)
clean_data.replace(':auth: - AuthCenter','authcenter', inplace=True)
clean_data.replace(':authleft: - AuthLeft','authleft', inplace=True)
clean_data.replace(':authright: - AuthRight','authright', inplace=True)

# Recode to economic flair onlclean_data
clean_data.replace('centrist', 'center', inplace=True)
clean_data.replace('left', 'left', inplace=True)
clean_data.replace('libright', 'right', inplace=True)
clean_data.replace('right','right', inplace=True)
clean_data.replace('libleft', 'left', inplace=True)
clean_data.replace('libcenter', 'center', inplace=True)
clean_data.replace('authcenter', 'center', inplace=True)
clean_data.replace('authleft', 'left', inplace=True)
clean_data.replace('authright','right', inplace=True)    


# Assign features and response appropriately (for TF-IDF we use the cleaned comments)
X = clean_data['comment']
y = clean_data['user.flair']

# Ensure data is a string
X = X.apply(lambda x: np.str_(x))

# Split data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Set up TF-IDF object to create vocab, count and transform data to TF-IDF features
tf_idf_vec = TfidfVectorizer(smooth_idf = True, use_idf = True)

###################### ZeroR #########################
# Fit the model
zero_r.fit(X_train, y_train)

# Record best model results 
zero_r_predict = zero_r.predict(X_test)
accuracy_log['zero_r'] = accuracy_score(y_test, zero_r_predict)

###################### Linear SVC #########################

# Set up pipeline
tf_idf_svc_pipeline = Pipeline(steps = [
  ('tf_idf_vec', tf_idf_vec),   
  ('svd', svd),
  ('linear_svc', linear_svc)
])

# Set up grid for hyperparameter optimization 
tf_idf_svc_param_grid = {
  'svd': ['passthrough', svd],
  'tf_idf_vec__min_df': [0.01, 0.05],  
  'tf_idf_vec__max_df': [0.9, 0.95],  
  'tf_idf_vec__max_features': [10000, 100000],  
  'linear_svc__C': [10, 1]
}


tf_idf_svc_search = GridSearchCV(tf_idf_svc_pipeline,
                                    tf_idf_svc_param_grid,
                                    n_jobs =-1,
                                    scoring = 'accuracy',
                                    cv = custom_cv)

tf_idf_svc_search.fit(X_train, y_train)

# Record best model results 
tf_idf_svc_predict = tf_idf_svc_search.predict(X_test)
accuracy_log['tf_idf_svc'] = accuracy_score(y_test, tf_idf_svc_predict)


model_log['tf_idf_svc'] = str(tf_idf_svc_search.best_estimator_)

################################################################################
################################################################################
# EMBEDDING
################################################################################
################################################################################

# https://github.com/RaRe-Technologies/gensim-data
# import gensim.downloader
# print(list(gensim.downloader.info()['models'].keys()))
# glove_vectors = gensim.downloader.load('glove-twitter-200')
# gensim.downloader.load('word2vec-google-news-300')

data = pd.read_csv('/Volumes/Elements/Text/nlp_concat_data.csv')

# data = data[data['user.flair'] != ':CENTG: - Centrist']
# data = data[data['user.flair'] != ':centrist: - Centrist']
# data = data[data['user.flair'] != ':centrist: - Grand Inquisitor']
# data = data[data['user.flair'] != ':auth: - AuthCenter']
# data = data[data['user.flair'] != ':lib: - LibCenter']

# Recode flair labels to avoid doubling up on flairs 
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

# Assign features and response appropriately (for TF-IDF we use the cleaned comments)
X = data['comment']
y = data['user.flair']

# Ensure data is a string
X = X.apply(lambda x: np.str_(x))

# Split data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Create embeddings transformer
embed = EmbeddingTransformer('word2vec-google-news-300')

###################### Linear SVC #########################

# Set up pipeline
embed_svc_pipeline = Pipeline(steps = [
  ('embed', embed),
  ('linear_svc', linear_svc)
])

# Set up grid for hyperparameter optimization 
embed_svc_param_grid = {
  'linear_svc__C': [10, 1]
}


embed_svc_search = GridSearchCV(embed_svc_pipeline,
                                 embed_svc_param_grid,
                                 n_jobs =-1,
                                 scoring = 'accuracy',
                                 cv = custom_cv)

embed_svc_search.fit(X_train, y_train)

# Record best model results 
embed_svc_predict = embed_svc_search.predict(X_test)
accuracy_log['embed_svc'] = accuracy_score(y_test, embed_svc_predict)

model_log['embed_svc'] = str(embed_svc_search.best_estimator_)

################################################################################
################################################################################
# TF-IDF + EMBEDDING
################################################################################
################################################################################

comb_data = pd.merge(clean_data, data, on='user')
comb_data.drop(['user.flair_y', 'Unnamed: 0_x', 'Unnamed: 0_y'],axis=1, inplace = True)
comb_data.rename(columns={'user.flair_x': 'user.flair',
                          'comment_y': 'comment_embed',
                          'comment_x': 'comment_tfidf'}, inplace = True)


# comb_data = comb_data[comb_data['user.flair'] != ':CENTG: - Centrist']
# comb_data = comb_data[comb_data['user.flair'] != ':centrist: - Centrist']
# comb_data = comb_data[comb_data['user.flair'] != ':centrist: - Grand Inquisitor']
# comb_data = comb_data[comb_data['user.flair'] != ':auth: - AuthCenter']
# comb_data = comb_data[comb_data['user.flair'] != ':lib: - LibCenter']

# Recode flair labels to avoid doubling up on flairs 
comb_data.replace(':CENTG: - Centrist','centrist', inplace=True)
comb_data.replace(':centrist: - Centrist','centrist', inplace=True)
comb_data.replace(':centrist: - Grand Inquisitor','centrist', inplace=True)
comb_data.replace(':left: - Left', 'left', inplace=True)
comb_data.replace(':libright: - LibRight', 'libright', inplace=True)
comb_data.replace(':libright2: - LibRight', 'libright', inplace=True)
comb_data.replace(':right: - Right',  'right', inplace=True)
comb_data.replace(':libleft: - LibLeft', 'libleft', inplace=True)
comb_data.replace(':lib: - LibCenter', 'libcenter', inplace=True)
comb_data.replace(':auth: - AuthCenter','authcenter', inplace=True)
comb_data.replace(':authleft: - AuthLeft','authleft', inplace=True)
comb_data.replace(':authright: - AuthRight','authright', inplace=True)

# Recode to economic flair only
comb_data.replace('centrist', 'center', inplace=True)
comb_data.replace('left', 'left', inplace=True)
comb_data.replace('libright', 'right', inplace=True)
comb_data.replace('right','right', inplace=True)
comb_data.replace('libleft', 'left', inplace=True)
comb_data.replace('libcenter', 'center', inplace=True)
comb_data.replace('authcenter', 'center', inplace=True)
comb_data.replace('authleft', 'left', inplace=True)
comb_data.replace('authright','right', inplace=True)

# Assign features and response appropriately (for TF-IDF we use the cleaned comments)
X = comb_data[['comment_embed', 'comment_tfidf']]
y = data['user.flair']

# Ensure data is a string
X['comment_embed'] = X['comment_embed'].apply(lambda x: np.str_(x))
X['comment_tfidf'] = X['comment_tfidf'].apply(lambda x: np.str_(x))

# Create processor for both types of text data
processor = ColumnTransformer(
  transformers=[
    ('embed', embed, 'comment_embed'),
    ('tf_idf_vec', tf_idf_vec, 'comment_tfidf')])


###################### Linear SVC #########################

# Set up pipeline
comb_svc_pipeline = Pipeline(steps=[
    ('processor', processor),
    ('svd', svd),
    ('linear_svc', linear_svc)])

# Set up grid for hyperparameter optimization 
comb_svc_param_grid = {
  'svd': ['passthrough', svd],
  'processor__tf_idf_vec__min_df': [0.01, 0.05],  
  'processor__tf_idf_vec__max_df': [0.9, 0.95],  
  'processor__tf_idf_vec__max_features': [10000, 100000],  
  'linear_svc__C': [10, 1]
}


comb_svc_search = GridSearchCV(comb_svc_pipeline,
                                 comb_svc_param_grid,
                                 n_jobs =-1,
                                 scoring = 'accuracy',
                                 cv = custom_cv)

comb_svc_search.fit(X_train, y_train)

# Record best model results 
comb_svc_predict = comb_svc_search.predict(X_test)
accuracy_log['comb_svc'] = accuracy_score(y_test, comb_svc_predict)

model_log['comb_svc'] = str(comb_svc_search.best_estimator_)


# SGD classifier
# Choose good HPs for everything
# Proof read
# Autogenerate results 
















