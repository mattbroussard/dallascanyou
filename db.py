
import os
import pymongo
import urlparse

# don't show frontend clients the _id
def removeId(obj):
    if "_id" in obj:
        del obj["_id"]
    return obj

class DB:
    
    client = None
    db = None
    posts = None

    def __init__(self):
        pass

    def __enter__(self):
        url = os.environ.get("MONGOLAB_URI", "")
        dbName = url.split("/")[-1]
        
        self.client = pymongo.MongoClient(url)
        self.db = self.client[dbName]
        self.posts = self.db["posts"]

        return self

    def get(self):
        query = self.posts.find().limit(50).sort("_id" , pymongo.DESCENDING)
        
        return map(removeId, query)

    def put(self, record):
        self.posts.insert(record)
        removeId(record)

    def nuke(self):
        self.db.drop_collection("posts")
        self.posts = self.db["posts"]

    def __exit__(self, exitType, value, traceback):
        self.client.close()
