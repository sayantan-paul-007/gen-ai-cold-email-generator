import pandas as pd
import chromadb
from chromadb.config import Settings
import uuid
import os

class Portfolio:
    def __init__(self, file_path="resources/portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Make sure vectorstore folder exists
        persist_dir = "vectorstore"
        os.makedirs(persist_dir, exist_ok=True)

        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir
        ))
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
