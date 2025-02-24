from fastapi import APIRouter, HTTPException
from consistentpeer.models.query import QueryRequest
from consistentpeer.constants.consistentpeer import rag

router = APIRouter()

@router.post("/query")
async def nlp(request: QueryRequest):
    try:
        response = rag.search(query_text=request.query, retriever_config={"top_k": 5})
        print(response.answer)
        return {"result": response.answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))