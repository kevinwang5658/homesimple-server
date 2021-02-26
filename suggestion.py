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


def image_search(listOfLikes):
    # Read image features
    fe = FeatureExtractor()
    features = []
    img_paths = []
    relative_img_paths = []
    mlsNumbers = []
    #/Users/PHOEN/PycharmProjects/homesimple-server/static/data/feature
    for feature_path in Path("./static/data/feature").glob("*.npy"):
        print(feature_path)
        features.append(np.load(feature_path))
        img_paths.append(
            Path("./static/data/images") / (feature_path.stem + ".jpg"))
        relative_img_paths.append('./static/data/images/' + (feature_path.stem + ".jpg"))
        mlsNumbers.append(feature_path.stem)

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
        return dict(zip(mlsNumbers, dists))
    '''
    return render_template('public/admin.html',
                               render_images=True,
                               query_path=img_path,
                               scores=scores,
                               render=False)
        else:
        return render_template('public/admin.html')
    '''


#image_search(listOfLikes)
