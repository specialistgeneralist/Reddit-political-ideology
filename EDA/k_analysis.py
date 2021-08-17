################################################################################
# Preparing data
################################################################################

# Load the necessary packages
import pandas as pd
import scipy.sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import Binarizer
import matplotlib.pyplot as plt

# Load data
data = pd.read_parquet('/Users/pkitc/Desktop/Michael/Thesis/data/user-interaction.parquet')

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

y.reset_index(drop = True, inplace=True)


# Split data into train andtest sets
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.2, 
                                                    stratify = y,
                                                    random_state = 0)
y_train.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)

###############################################################################
# K-ANALYSIS
###############################################################################

# Set up dictionary to store accuracy and ROC-AUC for prediction on varying k SVD components

# Set up dictionary to store accuracy and ROC-AUC for prediction on varying k SVD components
accuracy_log = {}
auc_log = {}

# Set up ZeroR baseline classifier to create a baseline accuracy 
zero_r = DummyClassifier(strategy = "most_frequent").fit(X_train, y_train)
zero_r.fit(X_train, y_train)
baseline_accuracy = accuracy_score(y_test, zero_r.predict(X_test))

# Set up binarizer to transform data into binary form and transform train and test set 
binarizer = Binarizer()
binarizer.fit(X_train)
X_train = binarizer.transform(X_train)
X_test = binarizer.transform(X_test)

# Compute the first 2000 SVD components of predictors (from training set) and transform test and training data accordingly
svd = TruncatedSVD(n_components = 1000, random_state = 0)
svd.fit(X_train)
X_train = svd.transform(X_train)
X_test = svd.transform(X_test)

# Set up OVR logistic regression model to use in predictions
ovr_logreg = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'none',
                                multi_class = 'ovr',
                                n_jobs = -1)

# Loop through different k and train model on first k principles components recording accuracy and ROC-AUC
for k in range(1, 1001, 25):
  
  X_test_temp = X_test[:,0:k]
  
  ovr_logreg.fit(X_train[:,0:k], y_train)
  predict = ovr_logreg.predict(X_test[:,0:k])
  accuracy_log[k] = accuracy_score(y_test, predict)
  prob = ovr_logreg.predict_proba(X_test[:,0:k])
  auc_log[k] = roc_auc_score(y_test, prob, average = 'weighted', multi_class = 'ovr')
  
  print(accuracy_log[k])


k_components = list(accuracy_log.keys())          
accuracy = list(accuracy_log.values())   
auc = list(auc_log.values())
     
plt.plot(k_components, accuracy, color='red')
plt.title('No. SVD components and accuracy')
plt.xlabel('K components')
plt.ylabel('Accuracy')
plt.grid(True)
plt.savefig('/Users/pkitc/Desktop/Michael/Thesis/data/k_svd_acc.pdf', dpi=600)
plt.show()

plt.plot(k_components, auc, color='blue')
plt.title('No. SVD components and weighted AUC')
plt.xlabel('K components')
plt.ylabel('ROC-AUC')
plt.grid(True)
plt.savefig('/Users/pkitc/Desktop/Michael/Thesis/data/k_svd_auc.pdf', dpi=600)
plt.show()

###############################################################################
# COMP ANALYSIS
###############################################################################


svd_1 = pd.DataFrame(zip(features, svd.components_[0]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_2 = pd.DataFrame(zip(features, svd.components_[1]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_3 = pd.DataFrame(zip(features, svd.components_[2]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_4 = pd.DataFrame(zip(features, svd.components_[3]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_5 = pd.DataFrame(zip(features, svd.components_[4]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_6 = pd.DataFrame(zip(features, svd.components_[5]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_7 = pd.DataFrame(zip(features, svd.components_[6]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_8 = pd.DataFrame(zip(features, svd.components_[7]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_9 = pd.DataFrame(zip(features, svd.components_[8]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_10 = pd.DataFrame(zip(features, svd.components_[9]),
               columns =['Feature', 'Value']).sort_values(by=['Value'], ascending = False)

svd_k = pd.concat([
    pd.concat([svd_1.head(10), svd_1.tail(10)]).reset_index(drop=True),
    pd.concat([svd_2.head(10), svd_2.tail(10)]).reset_index(drop=True),
    pd.concat([svd_3.head(10), svd_3.tail(10)]).reset_index(drop=True),
    pd.concat([svd_4.head(10), svd_4.tail(10)]).reset_index(drop=True),
    pd.concat([svd_5.head(10), svd_5.tail(10)]).reset_index(drop=True),
    pd.concat([svd_6.head(10), svd_6.tail(10)]).reset_index(drop=True),
    pd.concat([svd_7.head(10), svd_7.tail(10)]).reset_index(drop=True),
    pd.concat([svd_8.head(10), svd_8.tail(10)]).reset_index(drop=True),
    pd.concat([svd_9.head(10), svd_9.tail(10)]).reset_index(drop=True),
    pd.concat([svd_10.head(10), svd_10.tail(10)]).reset_index(drop=True)], axis=1)


svd_k.to_csv('/Users/pkitc/Desktop/Michael/Thesis/data/results/svd_k.csv')

ovr_logreg.fit(X_train[:,0:10], y_train)
svd_coef = pd.DataFrame(ovr_logreg.coef_)
svd_coef.index = list(ovr_logreg.classes_)
svd_coef.columns = [("svd " + str(n)) for n in range(1,11)]
svd_coef


color = ['red' if flair == 'left' else 'blue' if flair == 'right' else 'grey' for flair in list(y_train)]

plt.scatter(x=X_train[:,0],
            y=X_train[:,1],
            c=color,
            marker='D',
            alpha = 0.1)
plt.xlabel('SVD component 1')
plt.ylabel('SVD component 2')


plt.scatter(x=X_train[:,2],
            y=X_train[:,3],
            c=color,
            marker='D',
            alpha = 0.1)
plt.xlabel('SVD component 3')
plt.ylabel('SVD component 4')

plt.scatter(x=X_train[:,4],
            y=X_train[:,5],
            c=color,
            marker='D',
            alpha = 0.1)
plt.xlabel('SVD component 5')
plt.ylabel('SVD component 6') 
plt.title('Leftwing (red), rightwing (blue) and centrist (grey) users')
plt.savefig('/Users/pkitc/Desktop/Michael/Thesis/data/svd_scatterplot', dpi=600)
plt.show()


