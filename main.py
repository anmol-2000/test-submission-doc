from fastapi import FastAPI
from app.router import doc_router

app = FastAPI()
app.include_router(doc_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)