import os
import json

class RAGCreationJob:
    def __init__(self, rag_job_json):
        self.top_k = rag_job_json.get("top_k", 5)
        self.chunk_size = rag_job_json.get("chunk_size", 1000)
        self.max_length = self.chunk_size
        self.model_name = rag_job_json.get("model_name", 'gpt2')

    def __str__(self):
        return (f"RAGJob configured with:\n"
                f"Top K: {self.top_k}\n"
                f"Max Length: {self.max_length}\n"
                f"Chunk Size: {self.chunk_size}\n"
                f"Model Name: {self.model_name}")
