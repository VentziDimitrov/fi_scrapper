import os
import json
from openai import OpenAI
from tiktoken import encoding_for_model

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VectorDBManager:
    def __init__(self, model="text-embedding-3-small", tokenizer_model="gpt-4"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.tokenizer = encoding_for_model(tokenizer_model)
        
    def check_chunk_size(self, items: str, max_tokens=500):
        """
        Check if item text exceeds max_tokens and mark it.
        Adds property: 'exceed_chunk_size': bool
        """
        parsed_items = json.loads(items)
        for item in parsed_items:
            text_to_embed = f"Title: {item['title']}\nDescription: {item['description']}\nURL: {item['url']}"
            token_count = len(self.tokenizer.encode(text_to_embed))

            # mark whether this item exceeds chunk size
            item["exceed_chunk_size"] = token_count > max_tokens  
        return parsed_items     

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
