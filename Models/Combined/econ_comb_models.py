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
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, roc_auc_score, make_scorer
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import Binarizer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MaxAbsScaler
from sklearn.compose import make_column_selector as selector

# Load TF-IDF data 
clean_data = pd.read_csv('/Volumes/Elements/Text/nlp_cleaned_data.csv')
clean_data.drop(['Unnamed: 0'], axis=1, inplace=True)

# Load user interaction data 
int_data = pd.read_parquet('/Volumes/Elements/First_scrape/user-interaction.parquet')
political_subs = ['Libertarian', 'Anarchism', 'socialism', 'progressive', 'Conservative', 'democrats',
                  'Liberal', 'Republican', 'Liberty', 'Labour', 'Marxism', 'Capitalism', 'Anarchist',
                  'republicans', 'conservatives']
int_data.drop(columns = political_subs, inplace = True)

# Remove columns with insufficient interaction 
# This loop will remove subreddits with less than 50 comments and users with less than 50 comments until no row
# or column violates this condition
while True:
  print('in: '+str(int_data.shape))
  size = int_data.size 
  col_sum = int_data.sum(axis = 0, numeric_only = True)
  row_sum = int_data.sum(axis = 1, numeric_only = True)
  bad_cols = col_sum[col_sum <= 50].index
  bad_rows = row_sum[row_sum <= 50].index
  int_data.drop(index = bad_rows, columns = bad_cols, inplace = True)
  print('out: ' + str(int_data.shape))
  if int_data.size == size:
      break


# Merge datasets 
data = pd.merge(clean_data, int_data, on='user')
data.drop(['user.flair_y'],axis=1, inplace = True)
data.rename(columns={'user.flair_x': 'user.flair'}, inplace = True)

data['comment'] = data['comment'].apply(lambda x: np.str_(x))

y = data['user.flair']    

features = data.columns[2:]
X = data[features]

# Recode flair labels to avoid 
y.replace(':CENTG: - Centrist','centrist', inplace=True)
y.replace(':centrist: - Centrist','centrist', inplace=True)
y.replace(':centrist: - Grand Inquisitor','centrist', inplace=True)
y.replace(':left: - Left', 'left', inplace=True)
y.replace(':libright: - LibRight', 'libright', inplace=True)
y.replace(':libright2: - LibRight', 'libright', inplace=True)
y.replace(':right: - Right',  'right', inplace=True)
y.replace(':libleft: - LibLeft', 'libleft', inplace=True)
y.replace(':lib: - LibCenter', 'libcenter', inplace=True)
y.replace(':auth: - AuthCenter','authcenter', inplace=True)
y.replace(':authleft: - AuthLeft','authleft', inplace=True)
y.replace(':authright: - AuthRight','authright', inplace=True)

# Recode to economic flair only
y.replace('centrist', 'center', inplace=True)
y.replace('left', 'left', inplace=True)
y.replace('libright', 'right', inplace=True)
y.replace('right','right', inplace=True)
y.replace('libleft', 'left', inplace=True)
y.replace('libcenter', 'center', inplace=True)
y.replace('authcenter', 'center', inplace=True)
y.replace('authleft', 'left', inplace=True)
y.replace('authright','right', inplace=True)                    

# Split data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

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

# Set up binarizer
binarizer = Binarizer()

# Set up scaler 
scaler = MaxAbsScaler()

# Set up object for truncated SVD 
svd = TruncatedSVD(random_state = 0, n_components = 500)

# Set up TF-IDF object to create vocab, count and transform data to TF-IDF features
tf_idf_vec = TfidfVectorizer(smooth_idf = True, use_idf = True)

# Set up custom train/validate splot
custom_cv = StratifiedShuffleSplit(test_size = 0.2, n_splits = 1, random_state = 0)

################################################################################
# Create general preprocessing pipeline
################################################################################

# Create pipeline of preprocessing steps from user-interaction data
int_features = data.columns[3:]
int_transformer = Pipeline(steps = [
  ('binarizer', binarizer)
])

# Create pipeline for feature extraction from comments
text_transformer = Pipeline(steps = [
  ('tf_idf_vec', tf_idf_vec )
])

# Create preprocessor 
processor = ColumnTransformer(
  transformers=[
    ('int', int_transformer, int_features),
    ('text', text_transformer, 'comment')])

################################################################################
# ZeroR -- baseline
################################################################################

# Fit the model
zero_r.fit(X_train, y_train)

# Record best model results 
zero_r_predict = zero_r.predict(X_test)
accuracy_log['zero_r'] = accuracy_score(y_test, zero_r_predict)

################################################################################
# OVR Logistic regression 
################################################################################

# Set up OVR logistic regression object
ovr_logreg = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                penalty = 'l1',
                                multi_class = 'ovr',
                                n_jobs = -1,
                                random_state = 0)


# OVR logistic regresssion pipeline
ovr_logreg_pipeline = Pipeline(steps=[('processor', processor),
                               ('scaler', scaler),       
                               ('svd', svd),
                               ('ovr_logreg', ovr_logreg)])


ovr_logreg_param_grid = {
  'processor__text__tf_idf_vec__min_df': [0.01],  
  'processor__text__tf_idf_vec__max_df': [0.9],  
  'processor__text__tf_idf_vec__max_features': [10000, 100000],  
  'ovr_logreg__C': [0.001, 0.01, 0.1, 1, 10, 100, 'none']
}


ovr_logreg_search = GridSearchCV(ovr_logreg_pipeline,
                                 ovr_logreg_param_grid,
                                 n_jobs =-1,
                                 scoring = 'accuracy',
                                 cv = custom_cv)

ovr_logreg_search.fit(X_train, y_train)

# Record best model results 
ovr_logreg_predict = ovr_logreg_search.predict(X_test)
accuracy_log['ovr_logreg'] = accuracy_score(y_test, ovr_logreg_predict)

ovr_logreg_predict_prob = ovr_logreg_search.predict_proba(X_test)
auc_log['ovr_logreg'] = roc_auc_score(y_test, ovr_logreg_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['ovr_logreg'] = str(ovr_logreg_search.best_estimator_)

################################################################################
# Linear SVC
################################################################################

# Set up linear SVC object
svc = LinearSVC(loss = 'hinge',
                       multi_class = 'ovr',
                       random_state = 0
                       )



# OVR logistic regresssion pipeline
svc_pipeline = Pipeline(steps=[('processor', processor),
                               ('scaler', scaler),       
                               ('svd', svd),
                               ('svc', svc)])


svc_param_grid = {
  'svd': ['passthrough', svd],  
  'processor__text__tf_idf_vec__min_df': [0.01],  
  'processor__text__tf_idf_vec__max_df': [0.9],  
  'processor__text__tf_idf_vec__max_features': [10000],  
  'svc__C': [0.001, 0.01, 0.1, 1, 10, 100]
  }


svc_search = GridSearchCV(svc_pipeline,
                                 svc_param_grid,
                                 n_jobs =-1,
                                 scoring = 'accuracy',
                                 cv = custom_cv)

svc_search.fit(X_train, y_train)

# Record best model results 
svc_predict = svc_search.predict(X_test)
accuracy_log['svc'] = accuracy_score(y_test, svc_predict)


model_log['svc'] = str(svc_search.best_estimator_)


################################################################################
# Save results into a csv for the write-up
################################################################################

# Turn result dictionaries into a dataframe
model_df = pd.DataFrame(model_log, index = ['model'])
acc_df = pd.DataFrame(accuracy_log, index=['accuracy'])
auc_df = pd.DataFrame(accuracy_log, index=['auc'])

# Join these rowwise
results = pd.concat([acc_df, auc_df, model_df])
results.sort_values('accuracy', axis = 1, ascending = True, inplace = True)

# Export this dataframe (which contains each optimized models exact specification, accuracy and auc on the test set) to a .csv
results.to_csv('/Users/pkitc/Desktop/Michael/Thesis/data/results/econ_comb_results.csv')





