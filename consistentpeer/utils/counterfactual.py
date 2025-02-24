import re


def compute_consistency(conviction, certainty, rating, confidence, hedge):
    """
    Compute the Consistency score based on given parameters.

    Parameters:
    conviction (float): Conviction (-1 to 1)
    certainty (float): Certainty (3.3165 to 4.9329)
    rating (float): Rating (6 to 9)
    confidence (float): Confidence (2 to 5)
    hedge (float): Hedge (0 to 0.0734)

    Returns:
    float: Consistency score (1 to 10)
    """
    conviction = max(-1, min(1, conviction))
    certainty = max(3.3165, min(4.9329, certainty))
    rating = max(6, min(9, rating))
    confidence = max(2, min(5, confidence))
    hedge = max(0, min(0.0734, hedge))

    consistency = 1 + 9 * (
        0.4 * ((certainty - 3.3165) / 1.6164) +
        (0.25 + 0.1 * ((rating - 6) / 3) + 0.1 * ((confidence - 2) / 3)) * ((conviction + 1) / 2) +
        0.15 * ((rating - 6) / 3) +
        0.1 * ((confidence - 2) / 3) -
        0.1 * (hedge / 0.0734)
    )

    return max(1, min(10, consistency))

def convert_to_dict(obj):
    """
    Recursively converts nested objects to dictionaries.
    Preserves str, int, and float values while converting everything else to dict.
    
    Args:
        obj: Any Python object
        
    Returns:
        Converted structure with only dict, list, str, int, float as types
    """
    if isinstance(obj, (str, int, float)):
        return obj

    if isinstance(obj, (list, tuple, set)):
        return [convert_to_dict(item) for item in obj]

    if isinstance(obj, dict):
        return {key: convert_to_dict(value) for key, value in obj.items()}
    if hasattr(obj, '__dict__'):
        return convert_to_dict(obj.__dict__)
    
    try:
        return {key: convert_to_dict(value) 
                for key, value in obj.__getattribute__.__self__.__dict__.items()
                if not key.startswith('_')}
    except:
        return str(obj)
    
def calculate_averages(result):
    items = result["result"]["retriever_result"]["items"]
    
    total_hedge = total_certainty = total_conviction = total_confidence = total_rating = 0
    count = len(items)
    
    for item in items:
        content = eval(item["content"])
        total_hedge += content["hedge"]
        total_certainty += content["certainty"]
        total_conviction += content["conviction"]
        total_confidence += content["confidence"]
        total_rating += content["rating"]
    
    if count == 0:
        return {
            "hedge": 0,
            "certainty": 0,
            "conviction": 0,
            "confidence": 0,
            "rating": 0
        }
    
    return {
        "hedge": total_hedge / count,
        "certainty": total_certainty / count,
        "conviction": total_conviction / count,
        "confidence": total_confidence / count,
        "rating": total_rating / count
    }
    
def extract_score(text):
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None