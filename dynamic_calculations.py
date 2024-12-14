from dash import dcc, html, Input, Output, callback
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import plotly.express as px
import json


uv_data_path = 'C:/Users/Siva/Desktop/sivapro/todaysdata.csv'
geojson_path = 'C:/Users/Siva/Desktop/sivapro/us-states.json'

data = pd.read_csv(uv_data_path)
with open(geojson_path) as f:
    geojson = json.load(f)


data['Year'] = data['Year'].astype(int)
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day


layout = html.Div([
    html.H1("Dynamic Calculations and Machine Learning", style={"text-align": "center"}),

    html.Div([
        html.Label("Select Your State:"),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in data['NAME'].unique()],
            value=data['NAME'].unique()[0],
            clearable=False,
            style={"width": "400px", "margin": "10px auto"}
        )
    ], style={"text-align": "center"}),

    html.Div([
        html.Label("Select Analysis Type:"),
        dcc.Dropdown(
            id='analysis-type-dropdown',
            options=[
                {'label': 'Predict Cloudy Sky UVI', 'value': 'regression'},
                {'label': 'Cluster States', 'value': 'clustering'}
            ],
            value='regression',
            clearable=False,
            style={"width": "400px", "margin": "10px auto"}
        )
    ], style={"text-align": "center"}),

    html.Div([
        html.Label("Select Factors:"),
        dcc.Dropdown(
            id='factors-dropdown',
            options=[
                {'label': 'Clear Sky UVI', 'value': 'Clear Sky UVI'},
                {'label': 'Cloud Transmission', 'value': 'Cloud Transmission'},
                {'label': 'Solar Zenith Angle', 'value': 'Solar Zenith Angle'},
                {'label': 'Aerosol Transmission', 'value': 'Aerosol Transmission'},
                {'label': 'Total Column Ozone', 'value': 'Total Column Ozone'}
            ],
            multi=True,
            value=['Clear Sky UVI'],
            style={"width": "400px", "margin": "10px auto"}
        )
    ], style={"text-align": "center"}),

    html.Div([
        html.Label("Select Date:"),
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=data['Date'].min().date(),
            max_date_allowed=data['Date'].max().date(),
            initial_visible_month=data['Date'].min().date(),
            date=data['Date'].min().date(),
            style={"margin": "10px auto"}
        )
    ], style={"text-align": "center"}),

    html.Div([
        html.Label("Adjust Parameters (if applicable):"),
        dcc.Input(
            id='num-clusters-input',
            type='number',
            value=3,
            placeholder="Number of Clusters",
            style={"width": "200px", "margin": "10px"}
        )
    ], style={"text-align": "center", "display": "none"}, id="clustering-parameters"),

    html.Div([
        dcc.Graph(id="ml-output-graph", style={"height": "500px", "border": "2px solid black", "margin": "auto"})
    ], style={"text-align": "center"}),

    html.Div([
        html.Label("Actual and Predicted Values:"),
        html.Div(id="actual-predicted-values", style={"text-align": "center", "margin": "10px"})
    ])
])

@callback(
    Output("clustering-parameters", "style"),
    Input("analysis-type-dropdown", "value")
)
def toggle_clustering_parameters(analysis_type):
    if analysis_type == "clustering":
        return {"text-align": "center"}
    return {"text-align": "center", "display": "none"}

@callback(
    [Output("ml-output-graph", "figure"),
     Output("actual-predicted-values", "children")],
    [Input("state-dropdown", "value"),
     Input("analysis-type-dropdown", "value"),
     Input("factors-dropdown", "value"),
     Input("date-picker", "date")],
)
def perform_regression(selected_state, analysis_type, selected_factors, selected_date):
    if analysis_type != "regression":
        return px.scatter(title="Select 'Predict Cloudy Sky UVI' for regression."), ""

    if not selected_factors or "Cloudy Sky UVI" in selected_factors:
        return px.scatter(title="Please select valid factors (excluding Cloudy Sky UVI)."), ""

    state_data = data[data['NAME'] == selected_state]

    filtered_data = state_data.dropna(subset=selected_factors + ["Cloudy Sky UVI"])
    if filtered_data.empty:
        return px.scatter(title="No data available for the selected state and factors."), "No data available for the selected date."

    X = filtered_data[selected_factors]
    y = filtered_data["Cloudy Sky UVI"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    results_df = pd.DataFrame({
        "Actual": y_test,
        "Predicted": y_pred
    }).reset_index()

    fig = px.scatter(results_df, x="Actual", y="Predicted",
                     title=f"Regression Results for {selected_state}: Predicted vs Actual",
                     labels={"Actual": "Actual Cloudy Sky UVI", "Predicted": "Predicted Cloudy Sky UVI"},
                     trendline="ols")

    date_data = filtered_data[filtered_data['Date'] == pd.to_datetime(selected_date)]
    if not date_data.empty:
        actual_value = date_data["Cloudy Sky UVI"].iloc[0]
        predicted_value = model.predict(date_data[selected_factors])[0]
        actual_predicted_text = f"Actual: {actual_value:.2f}, Predicted: {predicted_value:.2f}"
    else:
        actual_predicted_text = "No data available for the selected date."

    return fig, actual_predicted_text
