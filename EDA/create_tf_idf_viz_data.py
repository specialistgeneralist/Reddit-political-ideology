################################################################################
# Get TF-IDF matrix
################################################################################

# Load the necessary packages
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

clean_data = pd.read_csv('nlp_cleaned_data.csv')

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


# Assign features and response appropriately (for TF-IDF we use the cleaned comments)
X = clean_data['comment']
y = clean_data['user.flair']

# Ensure data is a string
X = X.apply(lambda x: np.str_(x))

# Split data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Set up TF-IDF object to create vocab, count and transform data to TF-IDF features
tf_idf_vec = TfidfVectorizer(smooth_idf = True, use_idf = True,  max_df = 0.9, min_df = 0.01, max_features = 10000)

tf_idf_vec.fit(X_train)

matrix = tf_idf_vec.transform(X)
df = pd.DataFrame(matrix.toarray(), columns = tf_idf_vec.get_feature_names())

df = pd.concat([y, df], axis=1)
df.to_csv('tf_idf_matrix.csv')
