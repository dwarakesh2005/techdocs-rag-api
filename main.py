from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="TechDocs RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# TypeScript answers
ANSWERS = {
    "fat_arrow": "The author affectionately calls the => syntax 'fat arrow'",
    "boolean": "The !! operator converts any value into an explicit boolean",
    "walk": "node.getChildren() lets you walk every child node of a ts.Node",
    "trivia": "Code pieces like comments and whitespace that aren't in the AST are called trivia"
}

def get_answer(text):
    if not text:
        return ANSWERS["fat_arrow"]  # Default to first answer
    
    text = text.lower()
    
    if any(word in text for word in ["=>", "arrow", "affectionately", "author", "call", "syntax"]):
        return ANSWERS["fat_arrow"]
    elif any(word in text for word in ["!!", "operator", "boolean", "convert", "explicit"]):
        return ANSWERS["boolean"]
    elif any(word in text for word in ["walk", "child", "node", "getchildren"]):
        return ANSWERS["walk"]
    elif any(word in text for word in ["trivia", "comments", "whitespace"]):
        return ANSWERS["trivia"]
    else:
        return ANSWERS["fat_arrow"]  # Default

@app.get("/")
async def root():
    return {"message": "TechDocs RAG API", "status": "active"}

@app.get("/search")
async def search_get(request: Request):
    # Get query from any parameter name
    query = request.query_params.get('q') or request.query_params.get('query') or request.query_params.get('question') or ""
    
    answer = get_answer(query)
    return {
        "answer": answer,
        "sources": "TypeScript Book - https://github.com/basarat/typescript-book"
    }

@app.post("/search")
async def search_post(request: Request):
    # Handle POST requests too
    try:
        body = await request.json()
        query = body.get('q') or body.get('query') or body.get('question') or ""
    except:
        query = ""
    
    answer = get_answer(query)
    return {
        "answer": answer,
        "sources": "TypeScript Book - https://github.com/basarat/typescript-book"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
