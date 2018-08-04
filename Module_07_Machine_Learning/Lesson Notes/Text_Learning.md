
Bag of Words
- Counts the frequency of words
- Word order does not matter
- Long phrases gives different input vectors
- Cannot handle complex phrases


```python
from sklearn.feature_extraction.text import CountVectorizer



# create a list of strings
string1 = "blahblahblah"
string2 = "this is a test test test test"
string3 = "bags of words test test"
stringlist = [string1, string2, string3]

# vectorize the list
vectorizer = CountVectorizer()
bag_of_words = vectorizer.fit(stringlist)
bag_of_words = vectorizer.transform(stringlist)

print bag_of_words

# find out how many times a word is used
vectorizer.vocabulary_.get('test')
```

stopwords = low information words (and, the, in, for, you, will, have, be, etc...) that will be removed before processing.

NLTK = National Language Toolkit


```python
# find number of stopwords
from nltk.corpus import stopwords
sw = stopwords.words("english")
len(sw)
```




    153




```python
#Stemmer -> wraps up a group of words to the same root

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
print stemmer.stem("responsiveness")
print stemmer.stem("responsive")
print stemmer.stem("unresponsive")

# You want to run a stemmer before running bag of words.
```

    respons
    respons
    unrespons
    

TfIdf - Term Frequency Inverse Document Frequency

Tf = like a bag of words: frequency of a word
Idf = words are weighted based on how often the word occurs. The less frequent the words are used, the higher they are weighted.


