import requests
import pathlib
import io
import os
import json
import numpy as np
from feature_extractor import FeatureExtractor
from PIL import Image

realtor_url = 'https://api37.realtor.ca/Listing.svc/PropertySearch_Post'
fs = FeatureExtractor()

def fetch(data, id):
    result = {}
    print("data ", data)
    response = requests.post(realtor_url, data=data)
    num_pages = json.loads(response.content)['Paging']['TotalPages']
    print(num_pages)

    for count in range(0, num_pages):
        sendListingRequest(count, data, id, result)



def sendListingRequest(number, data, id, result):
    data['CurrentPage'] = number
    response = requests.post(realtor_url, data=data)
    results = json.loads(response.content)['Results']

    for listing in results:
        result[listing['MlsNumber']] = listing
        generateFeature(listing['Property']['Photo'][0]['LowResPath'], listing['MlsNumber'], id)

def generateFeature(image_url, mls_number, id):
    r = requests.get(image_url)
    image = Image.open(io.BytesIO(r.content))

    feature_path = os.path.join(pathlib.Path().absolute(), 'static', 'data', 'feature', id, mls_number + '.npy')
    feature = fs.extract(image)

    os.makedirs(os.path.dirname(feature_path), exist_ok=True)
    np.save(feature_path, feature)
    print(feature)
