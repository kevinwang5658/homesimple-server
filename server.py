from flask import Flask, render_template, request, Response
import json
import csv
import os

import sys

from flask import Flask, request, render_template
from suggestion import image_search

# sys.path.append('TF-IDF')
import tf_idf

import requests

app = Flask(__name__, static_url_path='/static')
likesMap = {}
ipToNameMap = {}
resultsMap = {}

@app.route('/')
def get_root_dir():
    return login()


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

                    "LowResPhoto": row[24]
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
                    "LowResPhoto": row[24]
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


@app.route('/recommendation', methods=['POST'])
def recommendation():
    # print(likesMap)
    listOfLikes = likesMap[request.json['ipAddress']]
    # print(listOfLikes)
    #get list of all tfidf scores
    text_rec = tf_idf.recommend(listOfLikes, 5)
    print('tf-idf scores:', text_rec)

    # Put recommendation code here
    # Use listOfLikes to get what the user likes
    img_rec = image_search(listOfLikes)
    #combine both dicts by mlsnumber
    combined = {k: text_rec.get(k, 0) + 0.75 * img_rec.get(k, 0) for k in set(text_rec) | set(img_rec)}
    #sort ascending
    sorted_rec = [[k, combined[k]] for k in sorted(combined, key=combined.get, reverse=False)]
    print(sorted_rec)
    # return render_template('public/admin.html',
    #                        render_images=True,
    #                        query_path=image_path,
    #                        scores=scores,
    #                        render=False)
    rec_listings=[]
    #only show first 10 items
    with open('./data/results.csv') as csv_file:
        data = list(csv.reader(csv_file, delimiter=','))
        for recommendation in sorted_rec[:10]:
            for row in data:
                if row[0] == recommendation[0]:
                    rec_listings.append({
                        "MlsNumber": row[0],
                        "Price": row[12],
                        "Address": row[7],
                        "Bathrooms": row[2],
                        "Bedrooms": row[3],
                        "InteriorSize": row[4],
                        "LowResPhoto": row[24],
                        "Score": recommendation[1]
                    })

    if (request.json['ipAddress'] in ipToNameMap):
        name = ipToNameMap[request.json['ipAddress']]
        if (name not in resultsMap):
            resultsMap[name] = {}

        resultsMap[name]['realtorD'] = list(map(lambda x: x['MlsNumber'], rec_listings))

        print()

    return render_template("public/results.html", data=rec_listings)

@app.route('/name', methods=['POST'])
def setName():
    ip_addr = request.remote_addr
    ipToNameMap[ip_addr] = request.json['name']

    return "success"

@app.route('/name', methods=['GET'])
def getName():
    ip_addr = request.remote_addr
    return ipToNameMap[ip_addr]

@app.route('/result/<name>/<realtor>', methods=['POST'])
def setResults(name, realtor):
    if (name not in resultsMap):
        resultsMap[name] = {}

    resultsMap[name][realtor] = request.json['data']

    return "success"

@app.route('/result/<name>', methods=['GET'])
def getResults(name):
    return resultsMap

@app.route('/result/<name>', methods=['DELETE'])
def deleteResults(name):
    del resultsMap[name]

    return "success"


@app.route('/login')
def login():
    return render_template("public/login.html")

@app.route('/results/<name>')
def results(name):
    #get recommendation listings from 3 sources
    response = requests.get('http://'+request.headers.get('Host')+'/result/'+name)
    response = response.json()
    print(response)
    #get recommendation values
    with open('./data/results.csv') as csv_file:
        data = list(csv.reader(csv_file, delimiter=','))
        results={'realtorA': [], 'realtorB': [], 'realtorC': [], 'realtorD': [], 'realtorE': []}
        sources=['realtorA','realtorB','realtorC','realtorD','realtorE']
        for source in sources:
            if source in response[name]:
                for liked_mls in response[name][source]:
                    for listing in data:
                        if listing[0] == liked_mls:
                            results[source].append({
                                        "MlsNumber": listing[0],
                                        "Price": listing[12],
                                        "Address": listing[7],
                                        "Bathrooms": listing[2],
                                        "Bedrooms": listing[3],
                                        "InteriorSize": listing[4],
                                        "LowResPhoto": listing[24]
                            })
            else:
                print(source,' recommendation not found!')
    return render_template("public/recommendations.html", data=results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
