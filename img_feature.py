from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np

def image_feature():
    # Read image features
    fe = FeatureExtractor()
    features = []
    img_paths = []
    for feature_path in Path("../data/feature").glob("*.npy"):
        print(feature_path)
        features.append(np.load(feature_path))
        img_paths.append(Path("../data/images") / (feature_path.stem + ".jpg"))
    features = np.array(features)
    print(features)
    print(img_paths)

    return features, img_paths

image_feature()