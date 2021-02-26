from flask import Flask, render_template, request, Response
import json
import csv
import os

import sys

from flask import Flask, request, render_template
from suggestion import image_search

# sys.path.append('TF-IDF')
import tf_idf

app = Flask(__name__, static_url_path='/static')
likesMap = {}


@app.route('/')
def get_root_dir():
    return 'hello world'


@app.route('/page')
def page():
    listing_info = '''
    {
  "MlsNumber": "X5095381",
  "PublicRemarks": "Location Location Location !!! Bright Well Maintained One Of Detached Home Back To Trail !!! Newly Wood Floor Throughout, Lots Of Windows, New Paint, Quiet Neighbourhood, Mins To Local Restaurants, Mall, Supermarkets, Schools &Shops. Walk Distense To University Of Waterloo, Used To Be Licensed Student Rental.And Own Use. Buy To Invest Or Own Use. Recent Improvements!!! Can't Miss This.**** EXTRAS **** Stove, Dishwasher, Washer, Dryer, All Elf's, All Window Coverings And Cac. (27853962)",
  "Bathrooms": 3,
  "Bedrooms": "4 + 1",
  "InteriorSize": "",
  "Type": "House",
  "Ammenities": "",
  "Address": "74 KAREN WALK|Waterloo, Ontario N2L6K7",
  "Longitude": -80.5463426,
  "Latitude": 43.4591645,
  "PostalCode": "N2L6K7",
  "NeighbourHood": "",
  "Price": "$550,000",
  "PropertyType": "Single Family",
  "ParkingSpace": 3,
  "OwnershipType": "Freehold",
  "Appliances": "",
  "FlooringType": "",
  "BasementType": "N/A (Finished)",
  "HeatingType": "Forced air (Natural gas)",
  "LandSize": "39.37 x 124.12 FT",
  "AmmenitiesNearBy": "",
  "PropertyTax": "$3,547.12",
  "ZoningDescription": "",
  "LowResPhoto": ""
}

    '''
    return render_template("public/listing.html", data=json.loads(listing_info))


@app.route('/page/<MlsNumber>')
def page_id(MlsNumber):
    places = {}
    with open('./data/results.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')

        for row in data:
            if row[0] == MlsNumber:
                places = {
                    "MlsNumber": row[0],
                    "PublicRemarks": row[1],
                    "Bathrooms": row[2],
                    "Bedrooms": row[3],
                    "InteriorSize": row[4],
                    "Ammenities": row[6],

                    "Address": row[7],
                    "Longitude": row[8],
                    "Latitude": row[9],
                    "Price": row[12],

                    "LowResPhoto": row[23]
                }
    return render_template("public/listing.html", data=places)


@app.route('/search')
def search():
    places = []
    with open('./data/results.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True

        for row in data:
            if not first_line:
                places.append({
                    "MlsNumber": row[0],
                    "Price": row[12],
                    "Address": row[7],
                    "Bathrooms": row[2],
                    "Bedrooms": row[3],
                    "InteriorSize": row[4],
                    "LowResPhoto": row[23]
                })
            else:
                first_line = False
    return render_template("public/results.html", data=places)


@app.route('/like', methods=['GET'])
def likes():
    return json.dumps(likesMap)


@app.route('/like/<mls_number>', methods=['POST'])
def addLike(mls_number):
    ip_addr = request.remote_addr
    if ip_addr not in likesMap:
        likesMap[ip_addr] = []

    # For now let's make this endpoint like a toggle button
    if (mls_number not in likesMap[request.remote_addr]):
        likesMap[request.remote_addr].append(mls_number)
    else:
        likesMap[request.remote_addr].remove(mls_number)
    print(likesMap)
    return "success"


@app.route('/admin')
def admin():
    return render_template("public/admin.html", data=str(likesMap), render=True)


@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    # print(likesMap)
    listOfLikes = likesMap[request.json['ipAddress']]
    # print(listOfLikes)
    #get list of all tfidf scores
    text_rec = tf_idf.recommend(listOfLikes, 5)
    print('tf-idf scores:', text_rec)

    # Put recommendation code here
    # Use listOfLikes to get what the user likes
    scores = image_search(listOfLikes)

    print(scores)

    #pair mls number with scores
    # results=scores[0],[os.path.basename(score) for score in scores[1]]
    print('image-rec scores:', results)

    return render_template('public/admin.html',
                           render_images=True,
                           query_path=image_path,
                           scores=scores,
                           render=False)


if __name__ == '__main__':
    app.run()
