################################################################################
# Preparing data
################################################################################

# Load the necessary packages
import pandas as pd
import scipy.sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedShuffleSplit
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, make_scorer
from sklearn.preprocessing import Binarizer

# Load data
data = pd.read_parquet('user-interaction.parquet')

# Remove explicitly political columns
political_subs = ['Libertarian', 'Anarchism', 'socialism', 'progressive', 'Conservative', 'democrats',
                  'Liberal', 'Republican', 'Liberty', 'Labour', 'Marxism', 'Capitalism', 'Anarchist',
                  'republicans', 'conservatives']
data.drop(columns = political_subs, inplace = True)


# Remove columns with insufficient interaction 
# This loop will remove subreddits with less than 50 comments and users with less than 50 comments until no row
# or column violates this condition
while True:
  print('in: '+str(data.shape))
  size = data.size 
  col_sum = data.sum(axis = 0, numeric_only = True)
  row_sum = data.sum(axis = 1, numeric_only = True)
  bad_cols = col_sum[col_sum <= 50].index
  bad_rows = row_sum[row_sum <= 50].index
  data.drop(index = bad_rows, columns = bad_cols, inplace = True)
  print('out: ' + str(data.shape))
  if data.size == size:
      break

# Seperate data into target/features and make features sparse
features = list(data.columns)
features.remove('user.flair')
y = data['user.flair'].copy(deep=True)
X = scipy.sparse.csr_matrix(data[features].values)

# Delete data to free up memory
del data

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

# Recode to social flair only
y.replace('centrist', 'center', inplace=True)
y.replace('left', 'center', inplace=True)
y.replace('libright', 'lib', inplace=True)
y.replace('right','center', inplace=True)
y.replace('libleft', 'lib', inplace=True)
y.replace('libcenter', 'lib', inplace=True)
y.replace('authcenter', 'auth', inplace=True)
y.replace('authleft', 'auth', inplace=True)
y.replace('authright','auth', inplace=True)

y.reset_index(drop = True, inplace=True)


# Split data into train andtest sets
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.2, 
                                                    stratify = y,
                                                    random_state = 0)
y_train.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)

# Set up custom train/validate split
custom_cv = StratifiedShuffleSplit(test_size = 0.2, n_splits = 1, random_state = 0)

# Data is now ready for modelling 

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
svd = TruncatedSVD(n_components = 500, random_state = 0)

# Set up binarizer
binarizer = Binarizer()


################################################################################
# ZeroR -- baseline
################################################################################

# Set up ZeroR classifier 
zero_r = DummyClassifier(strategy = "most_frequent")

# Fit the model
zero_r.fit(X_train, y_train)

# Record best model results 
zero_r_predict = zero_r.predict(X_test)
accuracy_log['zero_r'] = accuracy_score(y_test, zero_r_predict)

################################################################################
# OVR Logistic regression - no penalty
################################################################################

# Set up OVR logistic regression object
ovr_logreg = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'none',
                                multi_class = 'ovr',
                                n_jobs = -1,
                                random_state = 0)

# Set up Pipeline 
ovr_logreg_pipeline = Pipeline(steps = [
  ('binarizer', binarizer),   
  ('svd', svd),
  ('ovr_logreg', ovr_logreg)
])


# Set up grid for hyperparameter optimization 
ovr_logreg_param_grid = {
    'binarizer': ['passthrough', binarizer],
    'ovr_logreg__class_weight': ['balanced', None]
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
# OVR Logistic regression - Lasso penalty
################################################################################

# Set up OVR logistic regression object
ovr_logreg_l1 = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'l1',
                                multi_class = 'ovr',
                                n_jobs = -1,
                                random_state = 0)

# Set up Pipeline 
ovr_logreg_l1_pipeline = Pipeline(steps = [
  ('binarizer', binarizer),   
  ('svd', svd),
  ('ovr_logreg_l1', ovr_logreg_l1)
])

# Set up grid for hyperparameter optimization 
ovr_logreg_l1_param_grid = {
    'binarizer': ['passthrough', binarizer],
    'ovr_logreg_l1__C': [0.001, 0.01, 0.1, 1, 10, 100],
    'ovr_logreg_l1__class_weight': ['balanced', None]
    }

ovr_logreg_l1_search = GridSearchCV(ovr_logreg_l1_pipeline,
                      ovr_logreg_l1_param_grid,
                      n_jobs =-1,
                      scoring = 'accuracy',
                      cv = custom_cv)

ovr_logreg_l1_search.fit(X_train, y_train)

# Record best model results 
ovr_logreg_l1_predict = ovr_logreg_l1_search.predict(X_test)
accuracy_log['ovr_logreg_l1'] = accuracy_score(y_test, ovr_logreg_l1_predict)

ovr_logreg_l1_predict_prob = ovr_logreg_l1_search.predict_proba(X_test)
auc_log['ovr_logreg_l1'] = roc_auc_score(y_test, ovr_logreg_l1_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['ovr_logreg_l1'] = str(ovr_logreg_l1_search.best_estimator_)

################################################################################
# Multinomial Logistic regression - no penalty
################################################################################

# Set up multinomial logistic regression object
multinomial = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'none',
                                multi_class = 'multinomial',
                                n_jobs = -1,
                                random_state = 0)

# Set up Pipeline 
multinomial_pipeline = Pipeline(steps = [
  ('binarizer', binarizer), 
  ('svd', svd),
  ('multinomial', multinomial)
])

# Set up grid for hyperparameter optimization 
multinomial_param_grid = {
    'binarizer': ['passthrough', binarizer],
    'multinomial__class_weight': ['balanced', None]
    }

multinomial_search = GridSearchCV(multinomial_pipeline,
                      multinomial_param_grid,
                      n_jobs =-1,
                      scoring = 'accuracy',
                      cv = custom_cv)

multinomial_search.fit(X_train, y_train)


# Record the best model results 
multinomial_predict = multinomial_search.predict(X_test)
accuracy_log['multinomial'] = accuracy_score(y_test, multinomial_predict)


multinomial_predict_prob = multinomial_search.predict_proba(X_test)
auc_log['multinomial'] = roc_auc_score(y_test, multinomial_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['multinomial'] = str(multinomial_search.best_estimator_)


################################################################################
# Multinomial Logistic regression - Lasso penalty
################################################################################

# Set up multinomial logistic regression object
multinomial_l1 = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'l1',
                                multi_class = 'multinomial',
                                n_jobs = -1,
                                random_state = 0)

# Set up Pipeline
multinomial_l1_pipeline = Pipeline(steps = [
  ('binarizer', binarizer),     
  ('svd', svd),
  ('multinomial_l1', multinomial_l1)
])

# Set up grid for hyperparameter optimization
multinomial_l1_param_grid = {
  'binarizer': ['passthrough', binarizer],
  'multinomial_l1__C': [0.001, 0.01, 0.1, 1, 10, 100]
}

multinomial_l1_search = GridSearchCV(multinomial_l1_pipeline,
                                    multinomial_l1_param_grid,
                                    n_jobs =-1,
                                    scoring = 'accuracy',
                                    cv = custom_cv)

multinomial_l1_search.fit(X_train, y_train)

# Record best model results
multinomial_l1_predict = multinomial_l1_search.predict(X_test)
accuracy_log['multinomial_l1'] = accuracy_score(y_test, multinomial_l1_predict)

multinomial_l1_predict_prob = multinomial_l1_search.predict_proba(X_test)
auc_log['multinomial_l1'] = roc_auc_score(y_test, multinomial_l1_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['multinomial_l1'] = str(multinomial_l1_search.best_estimator_)


################################################################################
# Random Forest
################################################################################

# Set up random forest model object
rf = RandomForestClassifier(n_estimators = 500,
                            criterion = 'gini',
                            min_samples_split = 5,
                            min_samples_leaf = 5,
                            max_features = 'sqrt',
                            n_jobs = -1,
                            random_state = 0,
                            class_weight = 'balanced_subsample'
                            )

# Set up Pipeline
rf_pipeline = Pipeline(steps =[
  ('binarizer', binarizer),      
  ('svd', svd),
  ('rf', rf)
])

# Set up grid for hyperparameter optimization
rf_param_grid = {
  'binarizer': ['passthrough', binarizer],
  'rf__min_samples_split': [5, 10, 20],
  'rf__min_samples_leaf': [5, 10, 20],
  'rf__class_weight': ['balanced_subsample', None]
}

rf_search = GridSearchCV(rf_pipeline,
                         rf_param_grid,
                         n_jobs =-1,
                         scoring = 'accuracy',
                         cv = custom_cv)

rf_search.fit(X_train, y_train)

# Record best model results
rf_predict = rf_search.predict(X_test)
accuracy_log['rf'] = accuracy_score(y_test, rf_predict)

rf_predict_prob = rf_search.predict_proba(X_test)
auc_log['rf'] = roc_auc_score(y_test, rf_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['rf'] = str(rf_search.best_estimator_)


################################################################################
# OVR Random Forest
################################################################################

ovr_rf = OneVsRestClassifier(
    RandomForestClassifier(
        n_estimators = 500,
        criterion = 'gini',
        min_samples_split = 5,
        min_samples_leaf = 5,
        max_features = 'sqrt',
        n_jobs = -1,
        random_state = 0,
        class_weight = 'balanced_subsample'
        )
    )


# Set up Pipeline
ovr_rf_pipeline = Pipeline(steps =[
  ('binarizer', binarizer),     
  ('svd', svd),
  ('ovr_rf', ovr_rf)
])

# Set up grid for hyperparameter optimization
ovr_rf_param_grid = {
  'binarizer': ['passthrough', binarizer],  
  'ovr_rf__estimator__min_samples_split': [5, 10, 20],
  'ovr_rf__estimator__min_samples_leaf': [5, 10, 20],
  'ovr_rf__estimator__class_weight': ['balanced_subsample', None]  
}

ovr_rf_search = GridSearchCV(ovr_rf_pipeline,
                         ovr_rf_param_grid,
                         n_jobs =-1,
                         scoring = 'accuracy',
                         cv = custom_cv)

ovr_rf_search.fit(X_train, y_train)

# Record best model results
ovr_rf_predict = ovr_rf_search.predict(X_test)
accuracy_log['ovr_rf'] = accuracy_score(y_test, ovr_rf_predict)

ovr_rf_predict_prob = ovr_rf_search.predict_proba(X_test)
auc_log['ovr_rf'] = roc_auc_score(y_test, ovr_rf_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['ovr_rf'] = str(ovr_rf_search.best_estimator_)

################################################################################
# ADA Boost 
################################################################################

adaboost = AdaBoostClassifier(
    n_estimators = 500,
    random_state = 0,
    algorithm= 'SAMME')

# Set up Pipeline
adaboost_pipeline = Pipeline(steps =[
  ('binarizer', binarizer),
  ('svd', svd),
  ('adaboost', adaboost)
])

# Set up grid for hyperparameter optimization
adaboost_param_grid = {
  'binarizer': ['passthrough', binarizer],    
  'adaboost__learning_rate': [0.001, 0.01, 0.1, 1]
}

adaboost_search = GridSearchCV(adaboost_pipeline,
                         adaboost_param_grid,
                         n_jobs = -1,
                         scoring = 'accuracy',
                         cv = custom_cv)

adaboost_search.fit(X_train, y_train)

# Record best model results
adaboost_predict = adaboost_search.predict(X_test)
accuracy_log['adaboost'] = accuracy_score(y_test, adaboost_predict)

adaboost_predict_prob = adaboost_search.predict_proba(X_test)
auc_log['adaboost'] = roc_auc_score(y_test, adaboost_predict_prob, average = 'weighted', multi_class = 'ovr')

model_log['adaboost'] = str(adaboost_search.best_estimator_)


################################################################################
# Save results into a csv for the write-up
################################################################################

# Turn result dictionaries into a dataframe
model_df = pd.DataFrame(model_log, index = ['model'])
acc_df = pd.DataFrame(accuracy_log, index=['accuracy'])
auc_df = pd.DataFrame(auc_log, index=['auc'])

# Join these rowwise
results = pd.concat([acc_df, auc_df, model_df])
results.sort_values('accuracy', axis = 1, ascending = True, inplace = True)

# Export this dataframe (which contains each optimized models exact specification, accuracy and auc on the test set) to a .csv
results.to_csv('social_int_results.csv')
