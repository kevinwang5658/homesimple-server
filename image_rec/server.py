import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/wishlist") / (feature_path.stem + ".jpg"))
features = np.array(features)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        #image1
        file1 = request.files['query_img1']

        # Save query image
        query_image1 = Image.open(file1.stream)  # PIL image
        uploaded_img_path1 = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file1.filename
        query_image1.save(uploaded_img_path1)

        # Run search
        wish = fe.extract(query_image1)
        dists1 = np.linalg.norm(features-wish, axis=1)  # L2 distances to features
        id_wishlist = np.argsort(dists1)[1:2]  # Top 30 results
        wishlist1 = [(dists1[id], img_paths[id]) for id in id_wishlist]

        #image2
        file2 = request.files['query_img2']

        # Save query image
        query_image2 = Image.open(file2.stream)  # PIL image
        uploaded_img_path2 = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file2.filename
        query_image2.save(uploaded_img_path2)

        # Run search
        wish = fe.extract(query_image2)
        dists2 = np.linalg.norm(features-wish, axis=1)  # L2 distances to features
        id_wishlist = np.argsort(dists2)[1:2]  # Top 30 results
        wishlist2 = [(dists2[id], img_paths[id]) for id in id_wishlist]


        #image3
        file3 = request.files['query_img3']

        # Save query image
        query_image3 = Image.open(file3.stream)  # PIL image
        uploaded_img_path3 = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file3.filename
        query_image3.save(uploaded_img_path3)

        # Run search
        wish = fe.extract(query_image3)
        dists3 = np.linalg.norm(features-wish, axis=1)  # L2 distances to features
        id_wishlist = np.argsort(dists3)[1:2]  # Top 30 results
        wishlist3 = [(dists3[id], img_paths[id]) for id in id_wishlist]


        #image4
        file4 = request.files['query_img4']

        # Save query image
        query_image4 = Image.open(file4.stream)  # PIL image
        uploaded_img_path4 = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file4.filename
        query_image4.save(uploaded_img_path4)

        # Run search
        wish = fe.extract(query_image4)
        dists4 = np.linalg.norm(features-wish, axis=1)  # L2 distances to features
        id_wishlist = np.argsort(dists4)[1:2]  # Top 30 results
        wishlist4 = [(dists4[id], img_paths[id]) for id in id_wishlist]


        lowest_dist = dists1 + dists2 + dists3 + dists4
        avg_dist_vector = np.argsort(lowest_dist)[:1]
        best_vector = [(lowest_dist[id], img_paths[id]) for id in avg_dist_vector]

        return render_template('index.html',
                               query_path1=uploaded_img_path1,
                               query_path2=uploaded_img_path2,
                               query_path3=uploaded_img_path3,
                               query_path4=uploaded_img_path4,
                               wishlist1=wishlist1,
                               wishlist2=wishlist2,
                               wishlist3=wishlist3,
                               wishlist4=wishlist4,
                               best_vector=best_vector)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()
