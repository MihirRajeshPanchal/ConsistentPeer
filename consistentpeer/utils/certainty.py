from consistentpeer.constants.consistentpeer import estimator

def get_certainity(text):
    return estimator.predict(text)[0]