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
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# Load data
data = pd.read_parquet('/Users/pkitc/Desktop/Michael/Thesis/data/user-interaction.parquet')

# Remove explicitly political columns

#  [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#  [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#  [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]

# Remove columns with insufficient interaction 

#  [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#  [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#  [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]

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

y.reset_index(drop = True, inplace=True)


# Split data into train andtest sets
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.2, 
                                                    stratify = y,
                                                    random_state = 0)
y_train.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)

# Data is now ready for modelling 

################################################################################
################################################################################
# Modelling 
################################################################################
################################################################################

# Set up dictionary to store results 
accuracy_log = {}

# Set up object for truncated SVD
svd = TruncatedSVD(n_components = 1000, random_state = 0)

# Set up custom train/validate split
custom_cv = StratifiedShuffleSplit(test_size = 0.2, n_splits = 1, random_state = 0)

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
                                n_jobs = -1)

# Set up Pipeline 
ovr_logreg_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('ovr_logreg', ovr_logreg)
])

# Fit the model
ovr_logreg_pipeline.fit(X_train, y_train)

# Record best model results 
ovr_logreg_predict = ovr_logreg_pipeline.predict(X_test)
accuracy_log['ovr_logreg'] = accuracy_score(y_test, ovr_logreg_predict)

################################################################################
# OVR Logistic regression - Lasso penalty
################################################################################

# Set up OVR logistic regression object
ovr_logreg_l1 = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'l1',
                                multi_class = 'ovr',
                                n_jobs = -1)

# Set up Pipeline 
ovr_logreg_l1_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('ovr_logreg_l1', ovr_logreg_l1)
])

# Set up grid for hyperparameter optimization
ovr_logreg_l1_param_grid = {
    'ovr_logreg_l1__C': [0.001, 0.01, 0.1]
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

################################################################################
# Multinomial Logistic regression - no penalty
################################################################################

# Set up multinomial logistic regression object
multinomial = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'none',
                                multi_class = 'multinomial',
                                n_jobs = -1)

# Set up Pipeline 
multinomial_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('multinomial', multinomial)
])

# Fit the model
multinomial_pipeline.fit(X_train, y_train)

# Record the best model results 
multinomial_predict = multinomial_pipeline.predict(X_test)
accuracy_log['multinomial'] = accuracy_score(y_test, multinomial_predict)

################################################################################
# Multinomial Logistic regression - Lasso penalty
################################################################################

# Set up multinomial logistic regression object
multinomial_l1 = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'l1',
                                multi_class = 'multinomial',
                                n_jobs = -1)

# Set up Pipeline
multinomial_l1_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('multinomial_l1', multinomial_l1)
])

# Set up grid for hyperparameter optimization
multinomial_l1_param_grid = {
  'multinomial_l1__C': [0.001, 0.01, 0.1]
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
  ('svd', svd),
  ('rf', rf)
])

# Set up grid for hyperparameter optimization
rf_param_grid = {
  'rf__min_samples_split': [5, 10, 20],
  'rf__min_samples_leaf': [5, 10, 20]
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
  ('svd', svd),
  ('ovr_rf', ovr_rf)
])

# Set up grid for hyperparameter optimization
ovr_rf_param_grid = {
  'ovr_rf__min_samples_split': [5, 10, 20],
  'ovr_rf__min_samples_leaf ': [5, 10, 20]
}

ovr_rf_search = GridSearchCV(rf_pipeline,
                         ovr_rf_param_grid,
                         n_jobs =-1,
                         scoring = 'accuracy',
                         cv = custom_cv)

ovr_rf_search.fit(X_train, y_train)

# Record best model results
ovr_rf_predict = ovr_rf_search.predict(X_test)
accuracy_log['ovr_rf'] = accuracy_score(y_test, ovr_rf_predict)

################################################################################
# ADA Boost 
################################################################################

adaboost = AdaBoostClassifier(
    n_estimators = 500,
    random_state = 0,
    algorithm= 'SAMME')

# Set up Pipeline
adaboost_pipeline = Pipeline(steps =[
  ('svd', svd),
  ('adaboost', adaboost)
])

# Set up grid for hyperparameter optimization
adaboost_param_grid = {
  'adaboost__learning_rate': [0.001, 0.01, 0.1,1]
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


################################################################################
# OVR ADA Boost 
################################################################################

ovr_adaboost = OneVsRestClassifier(AdaBoostClassifier(
  n_estimators = 500,
  random_state = 0,
  algorithim = 'SAMME'))

# Set up Pipeline
ovr_adaboost_pipeline = Pipeline(steps =[
  ('svd', svd),
  ('ovr_adaboost', ovr_adaboost)
])

# Set up grid for hyperparameter optimization
ovr_adaboost_param_grid = {
  'ovr_adaboost__learning_rate': [0.001, 0.01, 0.1,1]
}

ovr_adaboost_search = GridSearchCV(ovr_adaboost_pipeline,
                               ovr_adaboost_param_grid,
                               n_jobs =-1,
                               scoring = 'accuracy',
                               cv = custom_cv)

ovr_adaboost_search.fit(X_train, y_train)

# Record best model results
ovr_adaboost_predict = ovr_adaboost_search.predict(X_test)
accuracy_log['ovr_adaboost'] = accuracy_score(y_test, ovr_adaboost_predict)

################################################################################
# OVR Linear SVC
################################################################################

# Set up SVM object
svc = LinearSVC(penalty = 'l2',
                loss = 'hinge',
                multi_class = 'ovr',
                class_weight = 'balanced',
                random_state = 0)

# Set up pipeline
svc_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('svc', svc)
])

# Set up grid for hyperparameter optimization
svc_param_grid = {
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



