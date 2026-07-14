import joblib
import numpy as np

model = joblib.load("floods.save")
scaler = joblib.load("transform.save")


def predict_flood(data):

    data = np.array(data).reshape(1,-1)

    data = scaler.transform(data)

    prediction = model.predict(data)

    probability = model.predict_proba(data)

    flood_probability = probability[0][1]*100

    return prediction[0],round(flood_probability,2)