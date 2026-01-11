# Feature Extraction Methods in NLP

Feature extraction is a crucial step in Natural Language Processing (NLP) that involves transforming text data into numerical representations that machine learning models can understand. Here are some common feature extraction methods:

1. **Bag of Words (BoW)**: This method represents text as a collection of word counts, disregarding grammar and word order. Each unique word in the corpus becomes a feature, and the value is the frequency of that word in the document.

   ```python
    from sklearn.feature_extraction.text import CountVectorizer
    corpus = ["This is a sample document.", "This document is another example."]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    print(X.toarray())
    print(vectorizer.get_feature_names_out())
   ```

   - Pros:
     - Simple and easy to implement.
     - Effective for small to medium-sized datasets.
   - Cons:
     - Ignores word order and context.
     - Can lead to high-dimensional feature spaces with sparse data.
2. **TF-IDF (Term Frequency-Inverse Document Frequency)**: This method weighs the importance of words based on their frequency in a document relative to their frequency across all documents. It helps to highlight words that are more relevant to a specific document.

   ```python
    from sklearn.feature_extraction.text import TfidfVectorizer
    corpus = ["This is a sample document.", "This document is another example."]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    print(X.toarray())
    print(vectorizer.get_feature_names_out())
   ```

   - Pros:
     - Reduces the impact of frequently occurring words that may not be informative.
     - Captures the importance of words in context.
   - Cons:
     - Still ignores word order.
     - Can be computationally intensive for large datasets.
3. **Word Embeddings**: Techniques like Word2Vec, GloVe, and FastText represent words as dense vectors in a continuous vector space. These embeddings capture semantic relationships between words based on their context in large corpora.

   ```python
    from gensim.models import Word2Vec
    sentences = [["this", "is", "a", "sample"], ["this", "is", "another", "example"]]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    vector = model.wv['sample']
    print(vector)
   ```

   - Pros:
     - Captures semantic meaning and relationships between words.
     - Can handle synonyms and analogies effectively.
   - Cons:
     - Requires large datasets for training.
     - More complex to implement and interpret.

To see these feature extraction methods in action, check out the [Feature Extraction Notebook](../../nbs/nlp/03-feature-extraction.ipynb).

[Back to NLP Concepts](index.md) | [Back to Home](../index.md)
