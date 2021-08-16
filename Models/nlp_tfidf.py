import pandas as pd
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
import re
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# nltk.download('stopwords')

data = pd.read_csv('/Users/pkitc/Desktop/Michael/Thesis/test/TEMP_user_corpus.csv')
data.columns = ['User', 'Comment', 'Subreddit', 'user.flair']

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


data['Comment'] = data['Comment'].astype(str)
data = data[pd.notnull(data['Comment'])]

data = data.groupby(['User', 'user.flair'])['Comment'].apply(' '.join).reset_index()

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

X = data['Comment'].apply(CleanText)
y = data['user.flair']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

vocab_docs = X_train.tolist()
cv = CountVectorizer(max_features = 5000) # HYPERPARAMS TBD max_df, min_df, max_features
word_count = cv.fit_transform(vocab_docs)

transformer = TfidfTransformer(smooth_idf = True, use_idf = True)
transformer.fit(word_count)

feature_names = cv.get_feature_names()

X_train = transformer.transform(cv.transform(X_train.tolist()))
X_test = transformer.transform(cv.transform(X_test.tolist()))


ovr_logreg = LogisticRegression(solver = 'saga',
                                max_iter = 1000,
                                class_weight = 'balanced',
                                penalty = 'l1',
                                C = 10,
                                multi_class = 'ovr',
                                n_jobs = -1)

ovr_logreg.fit(X_train, y_train)
accuracy_score(y_test, ovr_logreg.predict(X_test))



# pd.DataFrame(train.toarray(),columns = feature_names)
# pd.DataFrame(test.toarray(),columns = feature_names)



docs = data['Comment'][0:500].apply(CleanText).to_list()



cv = CountVectorizer(max_df = 0.95, max_features = 1000)
word_count = cv.fit_transform(docs)

transformer = TfidfTransformer(smooth_idf = True, use_idf = True)
transformer.fit(word_count)

feature_names = cv.get_feature_names()

tf_idf_vector = transformer.transform(cv.transform(data['Comment'][0:10].tolist()))




TEST  = pd.DataFrame(transformer.transform(cv.transform(data['Comment'][0:1000].tolist())).toarray())




list(cv.vocabulary_.keys())[:30]
list(cv.vocabulary_.values())[:30]


cv = CountVectorizer(max_df = 0.95, max_features = 1000)



CleanText(data['Comment'][1])


" ".join(CleanText(data['Comment'][1]))



data['Comment'] = data['Comment'].apply(CleanText)


docs = data['Comment'][0:500].apply(CleanText).to_list()

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

cv = CountVectorizer()
word_count = cv.fit_transform(docs)

transformer = TfidfTransformer(smooth_idf = True, use_idf = True)
transformer.fit(word_count)

feature_names = cv.get_feature_names()

tf_idf_vector = transformer.transform(cv.transform(data['Comment'][0:10].tolist()))




TEST  = pd.DataFrame(transformer.transform(cv.transform(data['Comment'][0:1000].tolist())).toarray())
