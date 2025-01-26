from fastapi import APIRouter, UploadFile, HTTPException
import numpy as np
import json
from app.db_config import get_redis_client
from app.utils import generate_embedding, embedding_model

# Initialize FastAPI app
doc_router = APIRouter(prefix="/api/documents")

# Initialize Redis client
redis_client = get_redis_client()


@doc_router.post("/upload")
async def upload_document(file: UploadFile):
    """
    Uploads a document, generates its vector embedding, and stores it in Redis.
    """
    try:
        # Read and process the file content
        content = await file.read()
        text = content.decode('utf-8')

        # Generate embedding for the document
        embedding = generate_embedding(text)

        # Create a unique document ID and store it in Redis
        doc_id = f"doc:{file.filename}"
        redis_client.hset(doc_id, mapping={
            "content": text,
            "embedding": json.dumps(embedding)
        })
        redis_client.sadd("documents", doc_id)

        return {"message": "Document uploaded successfully", "doc_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@doc_router.post("/search")
async def search_documents(query: str):
    """
    Searches for documents similar to the query using cosine similarity.
    """
    try:
        # Generate query embedding
        query_embedding = embedding_model.encode(query)
        results = []

        # Iterate over stored documents and calculate similarity
        for doc_id in redis_client.smembers("documents"):
            doc = redis_client.hgetall(doc_id)
            doc_embedding = np.array(json.loads(doc["embedding"]))

            # Compute cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )

            results.append({
                "doc_id": doc_id,
                "similarity": similarity,
                "content": doc["content"]
            })

        # Sort results by similarity in descending order
        results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")