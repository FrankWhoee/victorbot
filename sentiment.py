# from google.cloud import language_v1
# import os
import requests
from secrets import secrets
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
import nltk
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re, string, random
import pickle


nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

f = open('MaoClassifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()
## Load glorious sentiment analysis
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "victorbot-49929982e4a1.json"
# client = language_v1.LanguageServiceClient()

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

class neu:
    score = 0
    magnitude = 0

class neg:
    score = -1
    magnitude = 1

class pos:
    score = 1
    magnitude = 1

def get_sentiment(message):
    # r = requests.post(
    #     "https://api.deepai.org/api/sentiment-analysis",
    #     data={
    #         'text': message.content,
    #     },
    #     headers={'api-key': secrets["deep-ai-key"]}
    # )
    # print(r.json())
    custom_tokens = remove_noise(word_tokenize(message.content))
    answer = classifier.classify(dict([token, True] for token in custom_tokens))
    if answer == "Negative":
        return neg
    elif answer == "Neutral":
        return neu
    else:
        return pos



def get_sentiment_raw(text):
    # r = requests.post(
    #     "https://api.deepai.org/api/sentiment-analysis",
    #     data={
    #         'text': text,
    #     },
    #     headers={'api-key': secrets["deep-ai-key"]}
    # )
    # print(r.json())
    custom_tokens = remove_noise(word_tokenize(text))
    answer = classifier.classify(dict([token, True] for token in custom_tokens))
    if answer == "Negative":
        return neg
    elif answer == "Neutral":
        return neu
    else:
        return pos

# print(get_sentiment_raw("i hate blueberries"))