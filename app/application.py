from flask import Flask, render_template, json, request
from datetime import datetime
from pymongo import MongoClient
import os
import tracemalloc
import time
from bson import json_util, ObjectId  # MongoDB's utility for JSON serialization
from trie import Trie

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json.JSONEncoder)

application = Flask(__name__)

application.json_encoder = MongoJsonEncoder
trie = Trie()

client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.0')
db = client['swiftsearch']
sites_collection = db['sites']
inverted_index_collection = db['inverted_indices']

# Default endpoint
@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@application.route('/linear-search', methods=['POST'])
def linear_search():
    tracemalloc.start()
    search_query = request.json.get('search_query')
    page = request.json.get('page')
    per_page = request.json.get('per_page')
    
    start_time = time.time()
    words = set(search_query.lower().split())
    results = []
    cursor = sites_collection.find({})

    for document in cursor:
        all_document_words = set(document['title'].lower().split()).union(set(document['description'].lower().split()))
        matched_words_count = len(words.intersection(all_document_words))

        if matched_words_count > 0:
            results.append((document, matched_words_count))

    results.sort(key=lambda x: x[1], reverse=True)

    sorted_documents = [doc[0] for doc in results]
    
    elapsed_time = time.time() - start_time
    total_results = len(sorted_documents)
    start = (page - 1) * per_page
    end = start + per_page

    current, peak = tracemalloc.get_traced_memory()

    return {
        'results': sorted_documents[start:end],
        'total_results': total_results,
        'elapsed_time': elapsed_time,
        'current_memory': current / 1024**2,
        'peak_memory': peak / 1024**2
    }

@application.route('/inverted-index-search', methods=['POST'])
def inverted_index_search():
    tracemalloc.start()
    search_query = request.json.get('search_query')
    page = request.json.get('page')
    per_page = request.json.get('per_page')

    words = search_query.lower().split()
    start_time = time.time()

    # Dictionary to count occurrences of document IDs across words
    doc_id_count = {}
    for word in words:
        result = inverted_index_collection.find_one({'word': word})
        if result:
            for doc_id in result['document_ids']:
                if doc_id in doc_id_count:
                    doc_id_count[doc_id] += 1
                else:
                    doc_id_count[doc_id] = 1

    # Sorting documents by the count of matched query words, descending
    sorted_doc_ids = sorted(doc_id_count, key=doc_id_count.get, reverse=True)
    
    if sorted_doc_ids:
        # Fetch documents in the order of relevance
        results = list(sites_collection.find({'_id': {'$in': sorted_doc_ids}}))
        results.sort(key=lambda x: sorted_doc_ids.index(x['_id']))
    else:
        results = []

    elapsed_time = time.time() - start_time
    total_results = len(results)
    start = (page - 1) * per_page
    end = start + per_page

    current, peak = tracemalloc.get_traced_memory()

    return {
        'results': results[start:end],
        'total_results': total_results,
        'elapsed_time': elapsed_time,
        'current_memory': current / 1024**2,
        'peak_memory': peak / 1024**2
    }

@application.route('/trie-search', methods=['POST'])
def trie_search():
    tracemalloc.start()
    search_query = request.json.get('search_query')
    page = request.json.get('page')
    per_page = request.json.get('per_page')

    words = search_query.lower().split()
    start_time = time.time()

    # Dictionary to count occurrences of document IDs across words
    doc_id_count = {}
    for word in words:
        result = trie.search(word)
        if result:
            for doc_id in result:
                if doc_id in doc_id_count:
                    doc_id_count[doc_id] += 1
                else:
                    doc_id_count[doc_id] = 1

    # Sorting documents by the count of matched query words, descending
    sorted_doc_ids = sorted(doc_id_count, key=doc_id_count.get, reverse=True)
    
    if sorted_doc_ids:
        # Fetch documents in the order of relevance
        results = list(sites_collection.find({'_id': {'$in': sorted_doc_ids}}))
        results.sort(key=lambda x: sorted_doc_ids.index(x['_id']))
    else:
        results = []

    elapsed_time = time.time() - start_time
    total_results = len(results)
    start = (page - 1) * per_page
    end = start + per_page

    current, peak = tracemalloc.get_traced_memory()

    return {
        'results': results[start:end],
        'total_results': total_results,
        'elapsed_time': elapsed_time,
        'current_memory': current / 1024**2,
        'peak_memory': peak / 1024**2
    }

def populate_trie():
    documents = sites_collection.find({})
    count = 0
    for document in documents:
        os.system('clear')
        count = count + 1
        print("Build tree for: ", count)
        words = document['title'].lower().split() + document['description'].lower().split()
        for word in set(words):
            trie.insert(word, document['_id'])

populate_trie()

if __name__ == "__main__":
    application.run(debug=True, port=10303, host='0.0.0.0', use_reloader=True)
