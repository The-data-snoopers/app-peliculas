from joblib import load

class Model_prediction:

    def __init__(self):
        self.model = load("./api-rest/assets/pipeline_peliculas.joblib")

    def make_predictions(self, data):
        result = self.model.predict(data)
        return result
