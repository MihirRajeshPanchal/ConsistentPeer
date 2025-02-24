from fastapi import APIRouter, HTTPException
from consistentpeer.models.graph import MetaReviewRequest
from consistentpeer.utils.graph import add_reviews
import os
import json

router = APIRouter()


@router.post("/create_graph")
def add_meta_review(request: MetaReviewRequest):
    try:
        result = add_reviews(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

DATASET_FOLDER = "dataset"

@router.post("/bulk_create_graph")
def process_dataset_files():
    try:     
        if not os.path.exists(DATASET_FOLDER):
            raise HTTPException(status_code=404, detail="Dataset folder not found.")
        
        json_files = [f for f in os.listdir(DATASET_FOLDER) if f.endswith('.json')]

        if not json_files:
            return {"status": "failure", "message": "No JSON files found in the dataset folder."}
        
        success_rate = 0
        failure_rate = 0
        
        for file_name in json_files:
            file_path = os.path.join(DATASET_FOLDER, file_name)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                
                request = MetaReviewRequest(**data)
                result = add_reviews(request)
                
                print(f"File {file_name} processed successfully.")
                success_rate += 1
            except Exception as e:
                print(f"Error processing file {file_name}. Error: {str(e)}")
                failure_rate += 1
        
        total_files = success_rate + failure_rate
        success_rate_percentage = (success_rate / total_files) * 100 if total_files > 0 else 0
        failure_rate_percentage = (failure_rate / total_files) * 100 if total_files > 0 else 0
        
        return {
            "status": "completed",
            "success_rate": success_rate_percentage,
            "failure_rate": failure_rate_percentage
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))