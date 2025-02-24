from fastapi import APIRouter, HTTPException
from consistentpeer.constants.consistentpeer import rag
from consistentpeer.models.counterfactual import Review
from consistentpeer.utils.certainty import get_certainity
from consistentpeer.utils.conviction import get_conviction_score
from consistentpeer.utils.counterfactual import calculate_averages, compute_consistency, convert_to_dict, extract_score
from consistentpeer.utils.hedge import get_hedge

router = APIRouter()

@router.post("/consistentpeer/counterfactual")
async def nlp(request: Review):
    try:
        query_string = "Analyze the similar reviews and their confidence and rating score and give counterfactual reasoning for given review " + request.review + "with confidence score " + request.confidence + "and rating score " + request.rating

        conviction_score = get_conviction_score(request.review)
        certainity_score = get_certainity(request.review)
        hedge_score = get_hedge(request.review)
        
        retriever_result = rag.search(query_text=query_string, return_context=True, retriever_config={"top_k": 5})
        before_consistency = compute_consistency(
            conviction_score,
            certainity_score,
            extract_score(request.rating),
            extract_score(request.confidence),
            hedge_score
        )
        result = convert_to_dict({"result": retriever_result})
        res_averages = calculate_averages(result)

        after_consistency = compute_consistency(
            conviction_score,
            certainity_score,
            res_averages["rating"],
            res_averages["confidence"],
            hedge_score
        )
        return {
            "counterfactual_reasoning": result["result"]["answer"],
            "context": result["result"]["retriever_result"],
            "conviction_score": float(conviction_score),  
            "certainty_score": float(certainity_score),  
            "hedge_score": float(hedge_score),
            "before_consistency": float(before_consistency),
            "self_annotated_rating": float(extract_score(request.rating)),
            "self_annotated_confidence": float(extract_score(request.confidence)),
            "counterfactual_rating": float(res_averages["rating"]),
            "counterfactual_confidence": float(res_averages["confidence"]),
            "after_consistency": float(after_consistency)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    