

################################################################################
# Preparing data
################################################################################

# Load the necessary packages
import pandas as pd 
import scipy.sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

# Load data
data = pd.read_parquet('/Users/pkitc/Desktop/Michael/Thesis/data/user-interaction.parquet')

# Remove columns with insufficient interaction 



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

# Data is now ready for modelling 

################################################################################
################################################################################
# Modelling
################################################################################
################################################################################

# Set up object for truncated SVD
svd = TruncatedSVD(n_components = 1000,
                   random_state = 0)

################################################################################
# ZeroR -- baseline
################################################################################
# Set up ZeroR classifier 
ZeroR = DummyClassifier(strategy = "most_frequent")

# Compute 5-fold CV metrics
ZeroR_CV = cross_validate(
  ZeroR,
  X,
  y,
  cv = 5,
  scoring = ('accuracy')
)

# Report 5-fold CV
print('baseline accuracy:')
print(ZeroR_CV ['test_accuracy'].mean())


################################################################################
# OVR Logistic regression - no penalty
################################################################################

# Set up OVR logistic regression object
ovr_logreg = LogisticRegression(solver = 'lbfgs',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'none',
                                multi_class = 'ovr')

# Set up Pipeline 
ovr_logreg_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('ovr_logreg', ovr_logreg)
])

# Compute 5-fold CV metrics
ovr_logreg_CV = cross_validate(
  ovr_logreg_pipeline,
  X,
  y,
  cv = 5,
  scoring = ('accuracy','roc_auc_ovr', 'roc_auc_ovr_weighted'),
  n_jobs = -1
)

# Report 5-fold CV
print('accuracy:')
print(ovr_logreg_CV['test_accuracy'].mean())
print('ROC-AUC:')
print(ovr_logreg_CV['test_roc_auc_ovr'].mean())
print('ROC-AUC:')
print(ovr_logreg_CV['test_roc_auc_ovr_weighted'].mean())

################################################################################
# OVR Logistic regression - Lasso penalty
################################################################################

# Set up OVR logistic regression object
ovr_logreg_l1 = LogisticRegression(solver = 'lbfgs',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'l1',
                                C = 0.01,
                                multi_class = 'ovr')

# Set up Pipeline 
ovr_logreg_l1_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('ovr_logreg_l1', ovr_logreg_l1)
])

# Compute 5-fold CV metrics
ovr_logreg_l1_CV = cross_validate(
  ovr_logreg_l1_pipeline,
  X,
  y,
  cv = 5,
  scoring = ('accuracy','roc_auc_ovr', 'roc_auc_ovr_weighted'),
  n_jobs = -1
)

# Report 5-fold CV
print('accuracy:')
print(ovr_logreg_l1_CV['test_accuracy'].mean())
print('ROC-AUC:')
print(ovr_logreg_l1_CV['test_roc_auc_ovr'].mean())
print('ROC-AUC:')
print(ovr_logreg_CV['test_roc_auc_ovr_weighted'].mean())

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

# Compute 5-fold CV metrics 
rf_CV = cross_validate(
  rf_pipeline,
  X,
  y,
  cv = 5,
  scoring = ('accuracy','roc_auc_ovr', 'roc_auc_ovr_weighted'),
  n_jobs = -1
)

# Report 5-fold CV
print('accuracy:')
print(rf_CV['test_accuracy'].mean())
print('ROC-AUC:')
print(rf_CV['test_roc_auc_ovr'].mean())
print('ROC-AUC:')
print(rf_CV['test_roc_auc_ovr_weighted'].mean())

################################################################################
# OVR Linear SVC
################################################################################

# Set up SVM object
svc = LinearSVC(penalty = 'l2',
                loss = 'hinge',
                C = 1,
                multi_class = 'ovr',
                class_weight = 'balanced',
                random_state = 0)

# Set up pipeline
svc_pipeline = Pipeline(steps = [
  ('svd', svd),
  ('svc', svc)
])

# Compute 5-fold CV
svc_CV = cross_validate(
  svc_pipeline,
  X,
  y,
  cv = 5,
  scoring = ('accuracy','roc_auc_ovr', 'roc_auc_ovr_weighted'),
  n_jobs = -1
)

# Report 5-fold CV
print('accuracy:')
print(svc_CV['test_accuracy'].mean())
print('ROC-AUC:')
print(svc_CV['test_roc_auc_ovr'].mean())
print('ROC-AUC:')
print(svc_CV['test_roc_auc_ovr_weighted'].mean())


# TODO/IDEAS:
# Stratify data - done automatically by cross_validate 
# put in random seed to ensure replicability 
# Save outputs 
# Delete rows
# see how much variance is explained by PCA

# OVR with lasso
# Multinomial
# Multinomial with lasso

# RF (multinomial)
# RF (OVR)

# SVM (svc) - OVR

# XGBoost 
# XGboost (OVR)


# Figure out how multi-class ROC-AUC
# Is there a need to do OVR RF - wil lit be different/better than normal?
# Best C for logistic reg L1
# Best C for multiclass reg L1
# Best C for linear SVM reg L2
# How does the SVM work
   









