import pandas as pd
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Word Cloud
# name_wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white', height = 2000, width = 4000).generate(desc_corpus)
# plt.figure(figsize = (16,8))
# plt.imshow(name_wordcloud)
# plt.axis('off')
# plt.show()

listings = pd.read_csv('./data/natalie.csv', usecols=['MlsNumber', 'PublicRemarks', 'Type', 'Ammenities'])

def item(listings, id):
    name = listings.loc[listings['MlsNumber'] == id]['content'].tolist()[0].split(' // ')[0]
    desc = ' \nDescription: ' + listings.loc[listings['MlsNumber'] == id]['content'].tolist()[0].split(' // ')[1][
                                0:165] + '...'
    prediction = name + desc
    return prediction


def recommend(list_of_likes, num):
    # todo refactor csv read so it only has to be done once
    # listings = listings.head(10)
    # print(listings)
    # print(list_of_likes)

    listings['PublicRemarks'] = listings['PublicRemarks'].astype('str')
    listings['Type'] = listings['Type'].astype('str')
    listings['Ammenities'] = listings['Ammenities'].astype('str')
    listings['Combined'] = listings['Ammenities'] + ' ' + listings['PublicRemarks']
    listings['Combined'].fillna('Null', inplace=True)

    # print(listings.tail(10))

    # Get all listings within list of likes from the data frame
    liked_listings = listings.loc[listings['MlsNumber'].isin(list_of_likes)]

    # Combine all liked listings together to create an ideal listing
    ideal_listing = liked_listings['Combined'].str.cat(sep=' ')

    # Drop unused columns Type, Ammenities and Public Remarks
    listings.drop(['PublicRemarks', 'Type', 'Ammenities'], axis=1)

    # Drop liked listings from dataframe
    for mlsNumber in list_of_likes:
        print(mlsNumber)
        listings.drop(index=listings[listings['MlsNumber'] == mlsNumber].index, inplace=True)

    print(listings.columns)

    # Add ideal listing back in
    listings.append(['ideal', ideal_listing])


    # TF-IDF for description
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(listings['Combined'])
    cosine_similarities = linear_kernel(tfidf_matrix[-1], tfidf_matrix)[0]


    # Generate dictionary with scores
    mls_numbers = listings['MlsNumber'].tolist()
    result = {mls_numbers[i]: cosine_similarities[i] for i in range(len(mls_numbers))}

    # Return the top N values
    # return dict(sorted(result.items())[:num])
    return dict(sorted(result.items()))



# recommend(item_id='X5095381',num=5)
