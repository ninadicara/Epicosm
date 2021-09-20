import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.twitter_db
collection = db.tweets
follows_collection = db.follows
pseudofeed_collection = db.pseudofeed
