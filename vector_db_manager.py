import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VectorDBManager:
    def __init__(self, model="text-embedding-3-small"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def create_embedding(self, text: str):
        """Generate an embedding for a single text string."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_items(self, items: list):
        """Embed a list of JSON items """
        results = []
        for item in items:
            text_to_embed = f"Title: {item['title']}\nDescription: {item['description']}\nURL: {item['url']}"
            embedding = self.create_embedding(text_to_embed)
            
            results.append({
                "embedding": embedding,
                "metadata": {
                    "url": item["url"],
                    "title": item["title"],
                    "description": item["description"]
                }
            })
        return results
