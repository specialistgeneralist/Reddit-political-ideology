################################################################################
# Preparing data
################################################################################

# Load the necessary packages
import pandas as pd
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
import re
from bs4 import BeautifulSoup
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import accuracy_score, roc_auc_score, make_scorer

# nltk.download('stopwords')

# Load data
data = pd.read_csv('/Users/pkitc/Desktop/Michael/Thesis/test/TEMP_user_corpus.csv')
data.columns = ['user', 'comment', 'subreddit', 'user.flair']

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

# Ensure all comments are strings and remove any rows that have no comment recorded
data['comment'] = data['comment'].astype(str)
data = data[pd.notnull(data['comment'])]

# Group data by user so each row corresponds to a user and all of their comments are concated 
data_grouped = data.groupby(['user', 'user.flair'])['comment'].apply(' '.join).reset_index()

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

# Create a seperate column of cleaned text to be used in TF-IDF models
data_grouped['clean_comment'] = data_grouped['comment'].apply(CleanText)

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

# Set up object for truncated SVD 
svd = TruncatedSVD(random_state = 0)

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

# Assign features and response appropriately (for TF-IDF we use the cleaned comments)
X = data_grouped['clean_comment']
y = data_grouped['user.flair']

# Split data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Set up TF-IDF object to create vocab, count and transform data to TF-IDF features
tf_idf_vec = TfidfVectorizer(smooth_idf = True, use_idf = True)

###################### Linear SVC #########################

# Set up pipeline
tf_idf_svc_pipeline = Pipeline(steps = [
  ('tf_idf_vec', tf_idf_vec ),   
  ('svd', svd),
  ('linear_svc', linear_svc)
])

# Set up grid for hyperparameter optimization 
tf_idf_svc_param_grid = {
  'tf_idf_vec__min_df': [0.01, 0.05, 0.1],  
  'tf_idf_vec__max_df': [0.95, 0.9, 0.8],  
  'tf_idf_vec__max_features': [10000, 1000],  
  'svd__n_components': [50, 100, 500],
  'linear_svc__C': [10, 100],
  'linear_svc__class_weight': [None, 'balanced']
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

tf_idf_svc_predict_prob = tf_idf_svc_search.predict_proba(X_test)
auc_log['tf_idf_svc'] = roc_auc_score(y_test, tf_idf_svc_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['tf_idf_svc'] = str(tf_idf_svc_search .best_estimator_)
