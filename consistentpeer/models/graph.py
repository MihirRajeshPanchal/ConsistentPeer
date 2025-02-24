from pydantic import BaseModel
from typing import List, Optional

class Review(BaseModel):
    review: str  
    rating: str  
    confidence: str 

class MetaReview(BaseModel):
    id: str
    reviews: List[Review]  
    aspect: List[str]

class Rating(BaseModel):
    rating: str  
    id: str  

class Confidence(BaseModel):
    confidence: str  
    id: str  

class MetaReviewRequest(BaseModel):
    id: str
    reviews: List[Review]  
    aspect: List[str]

class ReviewRequest(BaseModel):
    review: str  
    rating: str  
    confidence: str  
