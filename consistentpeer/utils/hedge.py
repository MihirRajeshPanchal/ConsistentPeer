from consistentpeer.constants.consistentpeer import hedge_model

def get_hedge(text): 

    predictions, _ = hedge_model.predict([text])

    token_predictions = predictions[0]

    uncertainty_labels = {"D", "E", "I", "N"} 

    uncertainty_count = sum(1 for token_dict in token_predictions if list(token_dict.values())[0] in uncertainty_labels)

    total_tokens = len(token_predictions)
    hedge_score = uncertainty_count / total_tokens if total_tokens > 0 else 0

    return hedge_score