import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from itertools import combinations

uv_data_path = 'C:/Users/Siva/Desktop/sivapro/todaysdata.csv'
geojson_path = 'C:/Users/Siva/Desktop/sivapro/us-states.json'

data = pd.read_csv(uv_data_path)
with open(geojson_path) as f:
    geojson = json.load(f)

data['Year'] = data['Year'].astype(int)
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

def forward_selection(data, target, factors):
    best_r2 = 0
    best_combination = None

    for i in range(1, len(factors) + 1):
        for combo in combinations(factors, i):
            X = data[list(combo)]
            y = data[target]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = LinearRegression()
            model.fit(X_train, y_train)
            r2 = model.score(X_test, y_test)

            if r2 > best_r2:
                best_r2 = r2
                best_combination = combo

    return best_combination, best_r2


factors = ['Clear Sky UVI', 'Cloud Transmission', 'Solar Zenith Angle', 'Aerosol Transmission', 'Total Column Ozone']
target = 'Cloudy Sky UVI'
best_factors, best_r2 = forward_selection(data, target, factors)
print(f"Best Combination: {best_factors}, R^2: {best_r2}")
