import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.twitter_db
collection = db.tweets
following_collection = db.following
pseudofeed_collection = db.pseudofeed
