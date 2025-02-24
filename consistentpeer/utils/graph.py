from consistentpeer.models.graph import MetaReview
from consistentpeer.constants.graph import ASPECT_NODE, REVIEW_NODE, RATING_NODE, CONFIDENCE_NODE, RATING_SCORE_NODE, CONFIDENCE_SCORE_NODE
from consistentpeer.constants.consistentpeer import driver
from consistentpeer.utils.conviction import get_conviction_score
from consistentpeer.utils.hedge import get_hedge
from consistentpeer.utils.certainty import get_certainity
import re

VALID_ASPECTS = {
    'soundness',
    'meaningful_comparison', 
    'motivation',
    'originality',
    'clarity',
    'substance',
    'replicability'
}


def clean_text(text: str) -> str:
    """Remove all special characters from the text."""
    return re.sub(r'[^A-Za-z0-9 ]', '', text)

def extract_first_number(text: str) -> int:
    """Extract the first numeric value from the given text."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

def validate_aspect(aspect_name: str) -> str:
    """
    Validates and cleans aspect name by removing _positive/_negative suffixes.
    Returns cleaned name if valid, raises ValueError if invalid.
    """
    base_name = aspect_name.replace('_positive', '').replace('_negative', '')
    
    if base_name not in VALID_ASPECTS:
        raise ValueError(f"Invalid aspect name: {aspect_name}. Valid aspects are: {', '.join(VALID_ASPECTS)}")
    
    return base_name

def add_reviews(meta_review_request: MetaReview):
    with driver.session() as session:
        for review_data in meta_review_request.reviews:
            cleaned_review = clean_text(review_data.review)
            cleaned_rating = clean_text(review_data.rating)
            cleaned_confidence = clean_text(review_data.confidence)

            rating_score = extract_first_number(review_data.rating)
            confidence_score = extract_first_number(review_data.confidence)

            certainty_score = get_certainity(cleaned_review)
            hedge_score = get_hedge(cleaned_review)
            conviction_score = get_conviction_score(cleaned_review)
            
            review_query = f"""
            CREATE (review: {REVIEW_NODE} {{review: '{cleaned_review}', certainty: {certainty_score}, hedge: {hedge_score}, conviction: {conviction_score}}})
            CREATE (rating: {RATING_NODE} {{rating: '{cleaned_rating}'}})
            CREATE (confidence: {CONFIDENCE_NODE} {{confidence: '{cleaned_confidence}'}})
            MERGE (rating_score: {RATING_SCORE_NODE} {{value: {rating_score}}})
            MERGE (confidence_score: {CONFIDENCE_SCORE_NODE} {{value: {confidence_score}}})
            CREATE (review)-[:HAS_RATING]->(rating)
            CREATE (review)-[:HAS_CONFIDENCE]->(confidence)
            MERGE (rating)-[:HAS_RATING_SCORE]->(rating_score)  
            MERGE (confidence)-[:HAS_CONFIDENCE_SCORE]->(confidence_score)
            """
            
            result = session.run(review_query)
            
            valid_aspects = []
            for aspect_name in meta_review_request.aspect:
                try:
                    if aspect_name != 'summary':
                        cleaned_aspect = validate_aspect(aspect_name)
                        valid_aspects.append(cleaned_aspect)
                except ValueError as e:
                    print(f"Skipping invalid aspect: {str(e)}")
                    continue
            
            for aspect_name in valid_aspects:
                aspect_query = f"""
                MATCH (review:{REVIEW_NODE})
                WHERE review.review = '{cleaned_review}'
                MERGE (aspect:{ASPECT_NODE} {{name: '{aspect_name}'}})
                CREATE (review)-[:HAS_ASPECT]->(aspect)
                """
                session.run(aspect_query)

        return {"reviews_count": len(meta_review_request.reviews)}