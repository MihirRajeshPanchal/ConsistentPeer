from typing import List
from pydantic import BaseModel

class Review(BaseModel):
    review: str  
    rating: str  
    confidence: str 
    
class SimilarReviews(BaseModel):
    reviews: List[Review]