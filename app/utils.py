from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the embedding model (Not using gpt-4o as it was paid one...)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    return embedding_model.encode(text).tolist()

def calculate_similarity(vector1, vector2):
    vector1, vector2 = np.array(vector1), np.array(vector2)
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))