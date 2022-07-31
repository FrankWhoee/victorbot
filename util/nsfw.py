import os

import requests as requests

from nsfw_model.nsfw_detector import predict
model = predict.load_model('./nsfw_mobilenet2.224x224.h5')

# predict nsfw from image url
def predict_nsfw_from_url(url):
    img_data = requests.get(url).content
    with open('eval.jpg', 'wb') as handler:
        handler.write(img_data)
    pred = predict.classify(model,'eval.jpg')
    os.remove('eval.jpg')
    return pred