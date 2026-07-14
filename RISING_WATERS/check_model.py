import joblib
import numpy as np

model = joblib.load("floods.save")
scaler = joblib.load("transform.save")

sample = [[24,95,90,3500,180,500,2200,620,450,12]]

sample = scaler.transform(sample)

prediction = model.predict(sample)

print("Prediction:", prediction)

print("Probability:", model.predict_proba(sample))

print(model.get_depth())
print(model.get_n_leaves())