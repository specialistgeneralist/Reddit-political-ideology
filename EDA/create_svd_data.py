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


y.reset_index(drop = True, inplace=True)


# Split data into train andtest sets
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.2, 
                                                    stratify = y,
                                                    random_state = 0)
y_train.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)

# Binarize
binarizer = Binarizer()
binarizer.fit(X_train)
X_train = binarizer.transform(X_train)

# Compute the first 500 SVD components 
svd = TruncatedSVD(n_components = 500, random_state = 0)
svd.fit(X_train)
X_train = svd.transform(X_train)

data = pd.concat([y_train, pd.DataFrame(X_train)], axis=1)
data.to_csv('/Users/pkitc/Desktop/Michael/Thesis/data/results/svd_data.csv')


