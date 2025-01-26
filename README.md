# doc_assist
- ADOC ASSIST PP Instructions
1. Redis Setup:
   - Ensure Redis is installed with vector search capabilities (e.g., RedisAI, RediSearch).
   - Start Redis server: redis-server

2. Project Setup:
   - Install dependencies: pip install fastapi uvicorn redis sentence-transformers
   - Start the FastAPI app: uvicorn main:app --reload

3. API Endpoints:
   - POST /api/documents/upload: Upload a document and store its vector embedding.
   - POST /api/documents/search: Search for documents similar to a query.

4. Key Design Decisions:
   - Used Redis for vector storage and efficient retrieval.
   - Leveraged Sentence Transformers for embedding generation.
   - Cosine similarity for document-query matching.