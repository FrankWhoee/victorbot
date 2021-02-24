from google.cloud import language_v1
import os

## Load glorious sentiment analysis
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "victorbot-49929982e4a1.json"
client = language_v1.LanguageServiceClient()

def get_sentiment(message):
    document = language_v1.Document(content=message.content, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment

def get_sentiment_raw(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment