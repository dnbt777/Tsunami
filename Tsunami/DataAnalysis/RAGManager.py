import os
import pickle
from Tsunami.DataAnalysis.RAGCreationJob import RAGCreationJob
from Tsunami.ProjectConfig import ProjectConfig
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class RAGManager:
    def __init__(self, project_config: ProjectConfig):
        self.project_config = project_config

    def execute_job(self, rag_job: RAGCreationJob):
        workspace_path = self.project_config.rag_directory
        os.makedirs(workspace_path, exist_ok=True)
        # Load and preprocess data
        documents = self.load_data(self.project_config.data_download_directory)
        vectorizer, tfidf_matrix = self.preprocess_data(documents)
        # Save the vectorizer and tfidf_matrix
        self.save_rag_db(vectorizer, tfidf_matrix, documents, workspace_path)
        print("saved")
        # Load generative model
        tokenizer, model = self.load_model(rag_job.model_name)
        print("loaded")
        # Example query for demonstration
        query = "Chess"
        response = self.retrieve_relevant_chunks(query, vectorizer, tfidf_matrix, documents, model, tokenizer, rag_job.top_k, rag_job.chunk_size)
        # Save the response
        response_path = os.path.join(workspace_path, "response.txt")
        with open(response_path, 'w') as file:
            file.write(response)
        print(f"RAG job executed. Response saved to {response_path}")

    def load_data(self, data_folder, chunk_size=1000):
        documents = []
        for filename in os.listdir(data_folder):
            if filename.endswith('.txt'):
                with open(os.path.join(data_folder, filename), 'r') as file:
                    text = file.read()
                    # Split the text into chunks
                    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                    documents.extend(chunks)
        return documents

    def preprocess_data(self, documents):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        return vectorizer, tfidf_matrix

    def load_model(self, model_name):
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        return tokenizer, model

    def retrieve(self, query, vectorizer, tfidf_matrix, documents, top_k):
        query_vec = vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        related_docs_indices = cosine_similarities.argsort()[-top_k:][::-1]
        return [documents[i] for i in related_docs_indices]

    def generate_response(self, context, model, tokenizer, max_new_tokens):
        inputs = tokenizer.encode(context, return_tensors='pt')
        # Truncate the input if it exceeds the model's maximum length
        max_input_length = model.config.n_positions
        if inputs.size(1) > max_input_length:
            inputs = inputs[:, -max_input_length:]  # Keep only the last max_input_length tokens
        outputs = model.generate(inputs, max_new_tokens=max_new_tokens, num_return_sequences=1)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def retrieve_relevant_chunks(self, query, vectorizer, tfidf_matrix, documents, model, tokenizer, top_k, max_new_tokens):
        retrieved_chunks = self.retrieve(query, vectorizer, tfidf_matrix, documents, top_k)
        context = "<RETRIEVED_CHUNK>" + "</RETRIEVED_CHUNK><RETRIEVED_CHUNK>".join(retrieved_chunks) + "</RETRIEVED_CHUNK>"
        #response = self.generate_response(context, model, tokenizer, max_new_tokens)
        #return response
        return context

    def save_rag_db(self, vectorizer, tfidf_matrix, documents, workspace_path):
        with open(os.path.join(workspace_path, 'vectorizer.pkl'), 'wb') as f:
            pickle.dump(vectorizer, f)
        with open(os.path.join(workspace_path, 'tfidf_matrix.pkl'), 'wb') as f:
            pickle.dump(tfidf_matrix, f)
        with open(os.path.join(workspace_path, 'documents.pkl'), 'wb') as f:
            pickle.dump(documents, f)
        print(f"RAG database saved to {workspace_path}")

    def load_rag_db(self, workspace_path):
        with open(os.path.join(workspace_path, 'vectorizer.pkl'), 'rb') as f:
            vectorizer = pickle.load(f)
        with open(os.path.join(workspace_path, 'tfidf_matrix.pkl'), 'rb') as f:
            tfidf_matrix = pickle.load(f)
        with open(os.path.join(workspace_path, 'documents.pkl'), 'rb') as f:
            documents = pickle.load(f)
        return vectorizer, tfidf_matrix, documents

    def query_rag_db(self, query, workspace_path, model_name, top_k, max_new_tokens):
        vectorizer, tfidf_matrix, documents = self.load_rag_db(workspace_path)
        tokenizer, model = self.load_model(model_name)
        relevant_chunks = self.retrieve_relevant_chunks(query, vectorizer, tfidf_matrix, documents, model, tokenizer, top_k, max_new_tokens)
        return relevant_chunks