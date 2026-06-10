from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
load_dotenv()

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(
        os.getenv("ES_USER"),
        os.getenv("ES_PASSWORD")
    ),
    verify_certs=False
)

print("Connected:", es.ping())
print(es.info())
app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "Backend is running!"
@app.route("/reset")
def reset():
    es.indices.delete(
        index="search_engine",
        ignore_unavailable=True
    )
    return "Index deleted"
@app.route("/check")
def check():

    result = es.search(
        index="search_engine",
        query={
            "match_all": {}
        }
    )

    return jsonify(result.body)
@app.route("/count")
def count():
    return jsonify(es.count(index="search_engine").body)
@app.route("/autocomplete")
def autocomplete():

    query = request.args.get("q")

    response = es.search(
        index="search_engine",
        size=10,
        query={
            "match_phrase_prefix": {
                "title": {
                    "query": query
                }
            }
        }
    )

    suggestions = []

    for hit in response.body["hits"]["hits"]:
        suggestions.append(
            hit["_source"]["title"]
        )

    return jsonify(suggestions)
@app.route("/search")
def search():

    query = request.args.get("q")

    response = es.search(
    index="search_engine",
    size=20,
    query={
        "bool": {
            "should": [
                {
                    "match": {
                        "title": {
                            "query": query,
                            "boost": 10
                        }
                    }
                },
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "title^5",
                            "author^2",
                            "genre",
                            "description"
                        ],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                }
            ]
        }
    }
)

    results = []

    for hit in response.body["hits"]["hits"]:

        doc = hit["_source"]
        doc["score"] = round(hit["_score"], 2)

        results.append(doc)

    return jsonify(results)
if __name__ == "__main__":
    app.run(debug=True)