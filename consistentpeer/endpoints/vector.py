from fastapi import APIRouter, HTTPException
from consistentpeer.utils.vector import add_vector_indexes

router = APIRouter()

@router.post("/vector_index")
def create_vector_indexes():
    try:
        result = add_vector_indexes()
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))