# Text Preprocessing Techniques in NLP

Text preprocessing is a crucial step in Natural Language Processing (NLP) that involves cleaning and transforming raw text data into a format suitable for analysis and modeling. Here are some common text preprocessing techniques:

1. **Removing unwanted characters**: Eliminate unwanted characters such as punctuation marks from the text as they often do not contribute to the meaning in many NLP tasks.

   ```python
    import re
    text = re.sub(r'[^\w\s]', '', text)
   ```

   You can adjust the regex pattern based on your specific requirements for cleaning the text. For example:
   - To remove all characters except words and spaces, use `r'[^\w\s]'`.
   - To remove digits as well, you can use `r'[^a-zA-Z\s]'`.
2. **Lowercasing**: Convert all text to lowercase to ensure uniformity. This helps in reducing the vocabulary size by treating "Word" and "word" as the same token.

   ```python
   text = text.lower()
   ```
3. **Tokenization**: Split the text into individual words or tokens. This can be done using libraries like NLTK or SpaCy.

   ```python
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(text)
   ```
4. **Removing Stop Words**: Remove common words (like "and", "the", "is") that do not carry significant meaning in text analysis.

   ```python
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
   ```
5. **Stemming and Lemmatization**: Reduce words to their base or root form. Stemming cuts off word endings, while lemmatization considers the context and converts words to their meaningful base form.

   ```python
    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
   
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
   ```

To see these techniques in action, check out the [Text Preprocessing Notebook](https://github.com/peeush-agarwal/peeush-agarwal.github.io/blob/3149e6d33aedfbeff599425e57b4b9a814e00514/nbs/nlp/02-text-preprocessing.ipynb).

---

[<< Getting Started](01-getting-started.md) | [>> Feature Extraction](03-feature-extraction.md)

[Back to NLP Concepts](index.md) | [Back to Home](../index.md)
