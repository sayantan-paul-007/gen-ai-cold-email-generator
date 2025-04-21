import chromadb
import json
client = chromadb.Client()
collection = client.create_collection(name = 'new_collection')
collection.add(
    documents = [
        "This is India",
        "This is USA"
    ],
    ids = ['id1', 'id2']
)
all_docs = collection.get()
results = collection.delete(ids=all_docs["ids"])
get = collection.get()
print(get)