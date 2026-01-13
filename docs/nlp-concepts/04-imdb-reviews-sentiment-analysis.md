# IMDB Reviews Sentiment Analysis Example

In this example, we will perform sentiment analysis on the IMDB movie reviews dataset using Python and popular NLP libraries. The goal is to classify movie reviews as positive or negative based on their content.

[Full Code Jupyter Notebook](nbs/nlp/04-imdb-reviews-project.ipynb)

## Step 1: Import Libraries

```python
import pandas as pd
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
```

## Step 2: Load the Dataset

```python
# Load the IMDB dataset
df = pd.read_csv('path/to/imdb-dataset.csv')
```

## Step 3: Split the Dataset

```python
from sklearn.model_selection import train_test_split

X = df['review']
y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

## Step 4: Preprocess the Text Data

```python
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = text.lower()
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

X_train = X_train.apply(preprocess_text)
X_test = X_test.apply(preprocess_text)
```

## Step 5: Feature Extraction

### Using Bag of Words

```python
vectorizer_bow = CountVectorizer(max_features=5000)
X_train_bow = vectorizer_bow.fit_transform(X_train).toarray()
X_test_bow = vectorizer_bow.transform(X_test).toarray()
```

### Using TF-IDF

```python
vectorizer_tfidf = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer_tfidf.fit_transform(X_train).toarray()
X_test_tfidf = vectorizer_tfidf.transform(X_test).toarray()
```

### Using Word2Vec

```python
def tokenize(text):
    return simple_preprocess(text)

X_train_tokens = X_train.apply(tokenize)
X_test_tokens = X_test.apply(tokenize)

w2v_model = Word2Vec(sentences=X_train_tokens, vector_size=100, window=5, min_count=1, workers=4)

def get_w2v_features(tokens, model, vector_size):
    features = []
    for token_list in tokens:
        vector = sum([model.wv[word] for word in token_list if word in model.wv]) / len(token_list)
        features.append(vector)
    return np.array(features)

X_train_w2v = get_w2v_features(X_train_tokens, w2v_model, 100)
X_test_w2v = get_w2v_features(X_test_tokens, w2v_model, 100)
```

## Step 6: Train the Model

```python
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train_w2v, y_train)
```

## Step 7: Evaluate the Model

```python
y_pred = classifier.predict(X_test_w2v)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

This example demonstrates how to preprocess text data, extract features using different techniques, and train a machine learning model for sentiment analysis on the IMDB reviews dataset. You can experiment with different models and feature extraction methods to improve performance.

[Back to NLP Concepts](index.md) | [Back to Home](../index.md)
