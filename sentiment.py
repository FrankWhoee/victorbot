from google.cloud import language_v1
import os
import requests
from secrets import secrets

## Load glorious sentiment analysis
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "victorbot-49929982e4a1.json"
client = language_v1.LanguageServiceClient()

class sen:
    score = 0
    magnitude = 0

def get_sentiment(message):
    # r = requests.post(
    #     "https://api.deepai.org/api/sentiment-analysis",
    #     data={
    #         'text': message.content,
    #     },
    #     headers={'api-key': secrets["deep-ai-key"]}
    # )
    # print(r.json())
    return sen



def get_sentiment_raw(text):
    # r = requests.post(
    #     "https://api.deepai.org/api/sentiment-analysis",
    #     data={
    #         'text': text,
    #     },
    #     headers={'api-key': secrets["deep-ai-key"]}
    # )
    # print(r.json())
    return sen

# get_sentiment_raw("i hate blueberries")