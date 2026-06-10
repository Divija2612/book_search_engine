import pandas as pd
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "hello2612"),
    verify_certs=False
)

print("Connected:", es.ping())

df = pd.read_csv("Books.csv")

for _, row in df.iterrows():

    doc = {
    "title": str(row["title"]),
    "author": str(row["author"]),
    "genre": str(row["genre"]),
    "description": str(row["description"]),
    "publisher": str(row["publisher"]),
    "language": str(row["language"]),
    "rating": row["average_rating"],
    "thumbnail": str(row["thumbnail"])
}

    es.index(
        index="search_engine",
        document=doc
    )

print("Books Indexed Successfully!")