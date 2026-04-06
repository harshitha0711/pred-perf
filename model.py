import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data.csv")


X = df[['hours', 'sleep']]
y = df['marks']


model = LinearRegression()
model.fit(X, y)


def predict_marks(hours, sleep):
    return model.predict([[hours, sleep]])[0]