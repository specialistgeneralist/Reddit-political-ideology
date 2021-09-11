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
accuracy_log['zero_r_tfidf'] = accuracy_score(y_test, zero_r_predict)

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
# FAST TEXT
################################################################################
################################################################################

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

# Ens data uis a string
X = X.apply(lambda x: np.str_(x))
X = X.apply(lambda x: x.lower())

# Split data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


# https://zeugma.readthedocs.io/en/stable/readme.html#training-embeddings
# from zeugma.embeddings import EmbeddingTransformer
glove = EmbeddingTransformer('glove')

X_train = glove.transform(X_train)
X_test = glove.transform(X_test)

###################### ZeroR #########################
# Fit the model
zero_r.fit(X_train, y_train)

# Record best model results 
zero_r_predict = zero_r.predict(X_test)
accuracy_log['zero_r_glove'] = accuracy_score(y_test, zero_r_predict)

###################### Linear SVC #########################

# Set up pipeline
glove_svc_pipeline = Pipeline(steps = [
  ('linear_svc', linear_svc)
])

# Set up grid for hyperparameter optimization 
glove_svc_param_grid = {
  'linear_svc__C': [10, 1]
}


glove_svc_search = GridSearchCV(glove_svc_pipeline,
                                 glove_svc_param_grid,
                                 n_jobs =-1,
                                 scoring = 'accuracy',
                                 cv = custom_cv)

glove_svc_search.fit(X_train, y_train)

# Record best model results 
glove_svc_predict = glove_svc_search.predict(X_test)
accuracy_log['glove_svc'] = accuracy_score(y_test, glove_svc_predict)

model_log['glove_svc'] = str(glove_svc_search.best_estimator_)

