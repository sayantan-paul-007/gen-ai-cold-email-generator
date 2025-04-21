import pandas as pd
import chromadb
import uuid
import os
from chromadb.config import Settings

class Portfolio:
    def __init__(self, file_path=None):
        base_path = os.path.dirname(__file__)
        if file_path is None:
            file_path = os.path.join(base_path, "resources", "portfolio.csv")
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

        persist_dir = os.path.join(base_path, "..", "vectorstore")
        os.makedirs(persist_dir, exist_ok=True)

        if "STREAMLIT_SHARING" in os.environ:
            self.chroma_client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                anonymized_telemetry=False
            ))
        else:
            # Your original implementation for local development
            self.chroma_client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=persist_dir
            ))

        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
