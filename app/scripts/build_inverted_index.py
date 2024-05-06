from pymongo import MongoClient
import os

client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.0')
db = client['swiftsearch']
docs = db['sites']  # Your main documents collection
index_collection = db['inverted_indices']  # The inverted index collection

def build_index():
    cursor = docs.find({})
    count = 0
    for doc in cursor:
        # Assuming the document has a field named 'text' you want to index
        os.system('clear')
        count = count +1
        print('Current: ', count)
        try:
            words = doc['title'].lower().split() + doc['description'].lower().split()
            unique_words = set(words)  # Remove duplicates in each document
            for word in unique_words:
                index_collection.update_one(
                    {'word': word},
                    {'$addToSet': {'document_ids': doc['_id']}},
                    upsert=True
                )
        except:
            continue

build_index()
