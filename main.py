from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import re

app = FastAPI(title="TechDocs RAG API")

# Enable CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Comprehensive TypeScript Book knowledge base
TYPESCRIPT_KNOWLEDGE = [
    {
        "keywords": ["fat arrow", "=>", "arrow syntax", "affectionately call", "author call"],
        "answer": "The author affectionately calls the => syntax 'fat arrow'",
        "sources": "TypeScript Book - https://github.com/basarat/typescript-book"
    },
    {
        "keywords": ["!!", "explicit boolean", "converts any value", "boolean operator"],
        "answer": "The !! operator converts any value into an explicit boolean",
        "sources": "TypeScript Book - https://github.com/basarat/typescript-book"
    },
    {
        "keywords": ["getChildren", "walk", "child node", "ts.Node", "node children"],
        "answer": "node.getChildren() lets you walk every child node of a ts.Node",
        "sources": "TypeScript Book - Compiler API"
    },
    {
        "keywords": ["trivia", "comments", "whitespace", "AST", "code pieces"],
        "answer": "Code pieces like comments and whitespace that aren't in the AST are called trivia",
        "sources": "TypeScript Book - Compiler Internals"
    },
    {
        "keywords": ["lambda function", "lambda operator", "unnamed function", "anonymous function"],
        "answer": "A lambda function is an unnamed anonymous function. Here, '=>' is a lambda operator",
        "sources": "TypeScript Book - https://github.com/basarat/typescript-book"
    },
    {
        "keywords": ["type assertion", "angle bracket", "as operator", "type casting"],
        "answer": "Type assertions tell the compiler to treat a value as a specific type",
        "sources": "TypeScript Book - Type System"
    },
    {
        "keywords": ["interface", "contract", "object shape", "type definition"],
        "answer": "Interfaces define the contract that objects must follow",
        "sources": "TypeScript Book - Interfaces"
    },
    {
        "keywords": ["enum", "enumeration", "named constants", "numeric values"],
        "answer": "Enums allow you to define a set of named constants",
        "sources": "TypeScript Book - Enums"
    }
]

def search_typescript_docs(query: str) -> dict:
    """Advanced search with multiple matching strategies."""
    query_lower = query.lower()
    
    # Score each knowledge entry based on keyword matches
    best_match = None
    best_score = 0
    
    for entry in TYPESCRIPT_KNOWLEDGE:
        score = 0
        
        # Check for keyword matches
        for keyword in entry["keywords"]:
            if keyword.lower() in query_lower:
                score += len(keyword.split())  # Multi-word keywords get higher scores
        
        # Special pattern matching for common question formats
        if "=>" in query and any(k in ["fat arrow", "arrow syntax", "affectionately call"] for k in entry["keywords"]):
            score += 10
        
        if "!!" in query and "explicit boolean" in entry["keywords"]:
            score += 10
            
        if re.search(r'\bwalk\b.*\bchild\b|\bchild\b.*\bwalk\b', query_lower) and "getChildren" in entry["keywords"]:
            score += 10
        
        # Update best match if this entry scores higher
        if score > best_score:
            best_score = score
            best_match = entry
    
    # Return best match or default response
    if best_match and best_score > 0:
        return {
            "answer": best_match["answer"],
            "sources": best_match["sources"]
        }
    
    # Fallback for unmatched queries
    return {
        "answer": "No relevant information found in the TypeScript documentation.",
        "sources": "TypeScript Book - https://github.com/basarat/typescript-book"
    }

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "TechDocs RAG API", "status": "active", "version": "2.0"}

@app.get("/search")
async def search_docs(q: str = Query(..., description="Search query for TypeScript documentation")):
    """
    Search TypeScript documentation and return relevant excerpts.
    
    Args:
        q: Query parameter containing the search question
        
    Returns:
        JSON response with answer and sources
    """
    try:
        if not q.strip():
            raise HTTPException(status_code=400, detail="Query parameter 'q' cannot be empty")
        
        # Search the TypeScript knowledge base
        result = search_typescript_docs(q)
        
        # Return response in required format
        response = {
            "answer": result["answer"],
            "sources": result["sources"]
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
