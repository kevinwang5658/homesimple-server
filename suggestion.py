import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from flask import Flask, request, render_template
from pathlib import Path
import os

'''
ipAddress = '192.168.0.1'
likesMap = {"ipAddress": ["21001023"]}

listOfLikes = likesMap['ipAddress']
print(listOfLikes)

for number in listOfLikes:
    print(number)

'''

#Function helps determien the best house to represent listoflikes
def average_image(listOfLikes):
    # Read image features
    fe = FeatureExtractor()
    features = []
    relative_img_paths = []
    mlsNumbers = []
    lowest_dist = []

    # Limit features, mlsNumbers and relative img path to just list of likes
    for mls_number in listOfLikes:
        feature_path = Path("./static/data/feature/" + mls_number + "_1" + ".npy")
        print(feature_path)
        features.append(np.load(feature_path))
        relative_img_paths.append('./static/data/images/' + (feature_path.stem + ".jpg"))
        mlsNumbers.append(feature_path.stem[:-(len('_1'))])

    features = np.array(features)
    scriptDir = os.path.dirname(__file__)
    print(scriptDir)

    for mls_number in listOfLikes:
        # img_path = Path(("./data/images/" + mls_number + '_1' + '.jpg'))
        img_path = os.path.join(scriptDir, './static/data/images/' + mls_number + '_1' + '.jpg')
        print(img_path)  # e.g., ./data/images/xxx.jpg

        # feature = fe.extract(img=Image.open(img_path))  # extracts features from that image path
        # feature_path = Path("./data/feature") / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
        # feature_path = os.path.join(scriptDir, './data/feature')
        # np.save(feature_path, feature)

        query = fe.extract(img=Image.open(img_path))
        dists = np.linalg.norm(features - query, axis=1)  # L2 distances to features
        id_wishlist = np.argsort(dists)[1:2]  # Top result from witihin listoflikes, exclusing itself
        print(id_wishlist)
        wishlist = [(dists[id]) for id in id_wishlist]
        lowest_dist += wishlist

    print(lowest_dist)
    avg_dist_vector = np.argsort(lowest_dist)[:1]
    print(avg_dist_vector)
    wishlist_final = [(lowest_dist[id], relative_img_paths[id]) for id in avg_dist_vector]
    print(wishlist_final)
    # return dict(zip(mlsNumbers, avg_dist_vector))
    # returns a single best representative house
    return wishlist_final


def image_search(listOfLikes):
    #run image rec normally on best average house
    ideal_image = average_image(listOfLikes)
    img_path = ideal_image[0][1]

    # Read image features
    fe = FeatureExtractor()
    features = []
    img_paths = []
    relative_img_paths = []
    mlsNumbers = []
    # /Users/PHOEN/PycharmProjects/homesimple-server/static/data/feature
    for feature_path in Path("./static/data/feature").glob("*.npy"):
        # print(feature_path)
        features.append(np.load(feature_path))
        img_paths.append(
            Path("./static/data/images") / (feature_path.stem + ".jpg"))
        relative_img_paths.append('./static/data/images/' + (feature_path.stem + ".jpg"))
        mlsNumbers.append(feature_path.stem[:-(len('_1'))])

    features = np.array(features)
    query = fe.extract(img=Image.open(img_path))
    dists = np.linalg.norm(features - query, axis=1)  # L2 distances to features
    print('we did it')
    print(dists)
    print(mlsNumbers)
    return dict(zip(mlsNumbers, dists))


#image_search(listOfLikes)
