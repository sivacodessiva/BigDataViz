from dash import dcc, html, Input, Output, State, callback, dash_table
from prophet import Prophet
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

uv_data_path = 'todaysdata.csv'
data = pd.read_csv(uv_data_path)

data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day


layout = html.Div(
    style={"backgroundColor": "#f7f9fc", "padding": "20px", "fontFamily": "Arial"},
    children=[
        html.H1(
            "Forecast Cloudy Sky UVI Using Prophet",
            style={"textAlign": "center", "color": "#2c3e50", "fontWeight": "bold", "marginBottom": "20px"}
        ),

        # Arrange boxes side by side in one row
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    width=3,
                    children=dbc.Card(
                        style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #2980b9", "borderRadius": "10px"},
                        children=[
                            html.Label("Select Your State:", style={"fontWeight": "bold", "color": "#34495e"}),
                            dcc.Dropdown(
                                id='state-dropdown',
                                options=[{'label': state, 'value': state} for state in data['NAME'].unique()],
                                value=data['NAME'].unique()[0],
                                clearable=False,
                                style={"width": "100%", "margin": "auto"}
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    width=3,
                    children=dbc.Card(
                        style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #27ae60", "borderRadius": "10px"},
                        children=[
                            html.Label("Select Features (Optional):", style={"fontWeight": "bold", "color": "#34495e"}),
                            dcc.Checklist(
                                id='regressor-checklist',
                                options=[
                                    {'label': 'Clear Sky UVI', 'value': 'Clear Sky UVI'},
                                    {'label': 'Total Column Ozone', 'value': 'Total Column Ozone'}
                                ],
                                value=[],
                                style={"padding": "10px", "color": "#34495e"}
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    width=3,
                    children=dbc.Card(
                        style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #e67e22", "borderRadius": "10px"},
                        children=[
                            html.Label("Forecast for Future Dates:", style={"fontWeight": "bold", "color": "#34495e"}),
                            dcc.Input(
                                id='forecast-days-input',
                                type='number',
                                value=30,
                                placeholder="Enter number of days to forecast",
                                style={"width": "100%", "margin": "10px auto", "display": "block"}
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    width=3,
                    children=dbc.Card(
                        style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #8e44ad", "borderRadius": "10px"},
                        children=[
                            html.Label("Select a Specific Future Date:", style={"fontWeight": "bold", "color": "#34495e"}),
                            dcc.DatePickerSingle(
                                id='future-date-picker',
                                min_date_allowed=data['Date'].max().date(),
                                max_date_allowed=pd.to_datetime("2025-12-31").date(),
                                initial_visible_month=data['Date'].max().date(),
                                placeholder="Select a future date",
                                style={"margin": "10px auto", "display": "block"}
                            )
                        ]
                    ),
                ),
            ],
        ),


        # Forecast Graph
        dbc.Card(
            style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #16a085", "borderRadius": "10px"},
            children=[
                dcc.Graph(id="forecast-graph", style={"height": "500px", "borderRadius": "10px"})
            ]
        ),

        # Forecast Value Display (narrow and centered)
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    width=6,  # Narrow the box by limiting the column width
                    children=dbc.Card(
                        style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #c0392b", "borderRadius": "10px"},
                        children=[
                            html.Label("Forecasted UVI for Selected Date:", style={"fontWeight": "bold", "color": "#34495e"}),
                            html.Div(
                                id="forecast-value",
                                style={"textAlign": "center", "margin": "10px", "color": "#34495e"}
                            )
                        ]
                    ),
                )
            ],
        ),


        # Interactive Insights Section
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                html.H3("Interactive Insights", style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "10px"}),
                dbc.Button("Show/Hide Insights", id="toggle-insights-btn", color="primary", style={"margin": "10px auto", "display": "block"}),
                dbc.Collapse(
                    id="insights-collapse",
                    is_open=False,
                    children=[
                        dbc.Card(
                            style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #1abc9c", "borderRadius": "10px"},
                            children=[
                                dcc.Graph(id="future-factors-analysis", style={"height": "500px", "borderRadius": "10px"})
                            ]
                        ),
                        dbc.Row(
                            justify="center",
                            children=[
                                dbc.Col(
                                    width=10,  # Adjust the width to control the space it takes
                                    children=dbc.Card(
                                        style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #f39c12", "borderRadius": "10px"},
                                        children=[
                                            dcc.Graph(id="seasonal-trends", style={"height": "400px", "width": "100%"}),
                                            dcc.Graph(id="distribution-plot", style={"height": "300px", "width": "100%"})
                                        ]
                                    ),
                                )
                            ],
                        )
                    ]
                )
            ]
        ),

        # Skin Damage Risk Analysis Section
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                html.H3("Skin Damage Risk Analysis", style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "10px"}),
                dbc.Button("Show/Hide Skin Damage Risk Analysis", id="toggle-skin-risk-btn", color="warning", style={"margin": "10px auto", "display": "block"}),
                dbc.Collapse(
                    id="skin-risk-collapse",
                    is_open=False,
                    children=[
                        dbc.Card(
                            style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #e74c3c", "borderRadius": "10px"},
                            children=[
                                html.Label("Select a Specific Date:", style={"fontWeight": "bold", "color": "#34495e"}),
                                dcc.DatePickerSingle(
                                    id='skin-risk-date-picker',
                                    min_date_allowed=data['Date'].min().date(),
                                    max_date_allowed=(data['Date'].max() + pd.Timedelta(days=365)).date(),
                                    initial_visible_month=data['Date'].max().date(),
                                    placeholder="Select a date",
                                    style={"margin": "10px auto", "display": "block"}
                                ),
                                html.Label("Select Location:", style={"fontWeight": "bold", "color": "#34495e"}),
                                dcc.Dropdown(
                                    id='skin-risk-location',
                                    options=[{'label': state, 'value': state} for state in data['NAME'].unique()],
                                    value=data['NAME'].unique()[0],
                                    clearable=False,
                                    style={"width": "400px", "margin": "10px auto"}
                                )
                            ]
                        ),
                        dcc.Graph(id="skin-risk-gauge", style={"height": "400px", "borderRadius": "10px"}),
                        dbc.Card(
                            style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #34495e", "borderRadius": "10px"},
                            children=[
                                html.Label("Recommendations:", style={"fontWeight": "bold", "color": "#34495e"}),
                                html.Div(id="skin-risk-recommendations", style={"textAlign": "center", "margin": "10px", "color": "#34495e"})
                            ]
                        )
                    ]
                )
            ]
        ),

        # Minimal Erythemal Dose Section
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                html.H3("Minimal Erythemal Dose (MED) Analysis", style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "10px"}),
                dbc.Button("Show/Hide MED Analysis", id="toggle-med-btn", color="danger", style={"margin": "10px auto", "display": "block"}),
                dbc.Collapse(
                    id="med-collapse",
                    is_open=False,
                    children=[
                        dbc.Card(
                            style={"padding": "20px", "marginBottom": "20px", "border": "2px solid #8e44ad", "borderRadius": "10px"},
                            children=[
                                html.Label("Select State:", style={"fontWeight": "bold", "color": "#34495e"}),
                                dcc.Dropdown(
                                    id='med-state-dropdown',
                                    options=[{'label': state, 'value': state} for state in data['NAME'].unique()],
                                    value=data['NAME'].unique()[0],
                                    clearable=False,
                                    style={"width": "400px", "margin": "10px auto"}
                                ),
                                html.Label("Select Skin Type:", style={"fontWeight": "bold", "color": "#34495e"}),
                                dcc.Dropdown(
                                    id='skin-type-dropdown',
                                    options=[
                                        {'label': 'Type I - Very Fair', 'value': 200},
                                        {'label': 'Type II - Fair', 'value': 300},
                                        {'label': 'Type III - Medium', 'value': 400},
                                        {'label': 'Type IV - Olive', 'value': 600},
                                        {'label': 'Type V - Brown', 'value': 800},
                                        {'label': 'Type VI - Dark Brown/Black', 'value': 1000}
                                    ],
                                    value=200,
                                    clearable=False,
                                    style={"width": "400px", "margin": "10px auto"}
                                ),
                                html.Label("Select Date for MED Calculation:", style={"fontWeight": "bold", "color": "#34495e"}),
                                dcc.DatePickerSingle(
                                    id='med-date-picker',
                                    min_date_allowed=data['Date'].min().date(),
                                    max_date_allowed=(data['Date'].max() + pd.Timedelta(days=365)).date(),
                                    initial_visible_month=data['Date'].max().date(),
                                    placeholder="Select a date",
                                    style={"margin": "10px auto"}
                                )
                            ]
                        ),
                        html.Div(
                            style={"padding": "20px"},
                            children=[
                                html.Label("Time to Erythema (minutes):", style={"fontWeight": "bold", "color": "#34495e"}),
                                html.Div(id="med-result", style={"textAlign": "center", "margin": "10px", "color": "#34495e"})
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)



@callback(
    [Output("forecast-graph", "figure"),
     Output("forecast-value", "children")],
    [Input("state-dropdown", "value"),
     Input("regressor-checklist", "value"),
     Input("forecast-days-input", "value"),
     Input("future-date-picker", "date")]
)
def forecast_uv_index(selected_state, selected_regressors, forecast_days, future_date):
    state_data = data[data['NAME'] == selected_state]

    prophet_data = state_data[['Date', 'Cloudy Sky UVI']].rename(columns={'Date': 'ds', 'Cloudy Sky UVI': 'y'})
    prophet_model = Prophet()

    for regressor in selected_regressors:
        prophet_data[regressor] = state_data[regressor]
        prophet_model.add_regressor(regressor)

    prophet_model.fit(prophet_data)

    future = prophet_model.make_future_dataframe(periods=forecast_days)
    for regressor in selected_regressors:
        future[regressor] = state_data[regressor].mean()


    forecast = prophet_model.predict(future)

    fig = px.line(
        forecast, x='ds', y='yhat',
        title=f"Forecast for {selected_state}",
        labels={'ds': 'Date', 'yhat': 'Cloudy Sky UVI'},
        line_shape='linear',
    )
    fig.add_scatter(x=prophet_data['ds'], y=prophet_data['y'], mode='markers', name='Actual')
    fig.add_scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast', line=dict(color='blue'))
    fig.update_layout(title_font_size=20, legend_title_text='Legend')

    if future_date:
        future_date = pd.to_datetime(future_date)
        forecast_row = forecast[forecast['ds'] == future_date]
        if not forecast_row.empty:
            forecast_value = forecast_row['yhat'].iloc[0]
            forecast_text = f"Forecasted Cloudy Sky UVI for {future_date.date()}: {forecast_value:.2f}"
        else:
            forecast_text = "No forecast available for the selected date."
    else:
        forecast_text = "Please select a future date to see the forecast."

    return fig, forecast_text

@callback(
    Output("future-factors-analysis", "figure"),
    [Input("state-dropdown", "value"),
     Input("forecast-days-input", "value")]
)
def analyze_future_factors(selected_state, forecast_days):
    state_data = data[data['NAME'] == selected_state]
    prophet_data = state_data[['Date', 'Cloudy Sky UVI']].rename(columns={'Date': 'ds', 'Cloudy Sky UVI': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_data)

    future = prophet_model.make_future_dataframe(periods=forecast_days)
    forecast = prophet_model.predict(future)

    forecast['Day'] = forecast['ds'].dt.day
    analysis_fig = px.line(
        forecast, x='ds', y=['yhat', 'yhat_lower', 'yhat_upper'],
        title="Upper and Lower Bound variations of Forecast Cloudy Sky UVI for the selected State",
        labels={"value": "UVI", "variable": "Type", "ds": "Date"},
        line_group="variable",
    )
    analysis_fig.update_layout(title_font_size=20, legend_title_text='Type')
    return analysis_fig



@callback(
    Output("seasonal-trends", "figure"),
    [Input("state-dropdown", "value"),
     Input("forecast-days-input", "value")]
)
def plot_seasonal_trends(selected_state, forecast_days):
    state_data = data[data['NAME'] == selected_state]
    prophet_data = state_data[['Date', 'Cloudy Sky UVI']].rename(columns={'Date': 'ds', 'Cloudy Sky UVI': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_data)
    future = prophet_model.make_future_dataframe(periods=forecast_days)
    forecast = prophet_model.predict(future)

    forecast['Month'] = forecast['ds'].dt.month
    monthly_avg = forecast.groupby('Month')['yhat'].mean()

    fig = px.bar(
        x=monthly_avg.index,
        y=monthly_avg.values,
        title="Monthly Trends in Forecasted Cloudy Sky UVI",
        labels={'x': 'Month', 'y': 'Average UVI'},
        color=monthly_avg.index,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(title_font_size=20, xaxis_title="Month", yaxis_title="Average UVI", coloraxis_showscale=False)
    return fig

@callback(
    Output("distribution-plot", "figure"),
    [Input("state-dropdown", "value"),
     Input("forecast-days-input", "value")]
)
def plot_distribution(selected_state, forecast_days):
    state_data = data[data['NAME'] == selected_state]
    prophet_data = state_data[['Date', 'Cloudy Sky UVI']].rename(columns={'Date': 'ds', 'Cloudy Sky UVI': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_data)
    future = prophet_model.make_future_dataframe(periods=forecast_days)
    forecast = prophet_model.predict(future)

    fig = px.histogram(
        forecast, x='yhat',
        title="Forecast Distribution",
        labels={'yhat': 'Forecasted UVI'},
        nbins=20,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(title_font_size=20, xaxis_title="Forecasted UVI", yaxis_title="Frequency")
    return fig

@callback(
    [Output("skin-risk-gauge", "figure"),
     Output("skin-risk-recommendations", "children")],
    [Input("skin-risk-date-picker", "date"),
     Input("skin-risk-location", "value"),
     Input("forecast-days-input", "value")]
)
def calculate_skin_risk(selected_date, selected_location, forecast_days):
    if not selected_date or not selected_location:
        return go.Figure(), "Please select a valid date and location."

    selected_date = pd.to_datetime(selected_date)

    state_data = data[data['NAME'] == selected_location]
    if state_data.empty:
        return go.Figure(), "No data available for the selected location."

    prophet_data = state_data[['Date', 'Clear Sky UVI']].rename(columns={'Date': 'ds', 'Clear Sky UVI': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_data)

    future = prophet_model.make_future_dataframe(periods=forecast_days)
    forecast = prophet_model.predict(future)

    forecast_row = forecast[forecast['ds'] == selected_date]
    if forecast_row.empty:
        return go.Figure(), "No forecast available for the selected date."

    aerosol_transmission = state_data['Aerosol Transmission'].mean()
    adjusted_uv_index = forecast_row['yhat'].iloc[0] * (aerosol_transmission / 100)

    if adjusted_uv_index <= 2:
        risk_category = "Low"
    elif adjusted_uv_index <= 5:
        risk_category = "Moderate"
    elif adjusted_uv_index <= 7:
        risk_category = "High"
    elif adjusted_uv_index <= 10:
        risk_category = "Very High"
    else:
        risk_category = "Extreme"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=adjusted_uv_index,
        title={'text': "Adjusted UV Index"},
        gauge={
            'axis': {'range': [0, 11]},
            'bar': {'color': "red" if adjusted_uv_index > 7 else "yellow" if adjusted_uv_index > 3 else "green"},
            'steps': [
                {'range': [0, 2], 'color': "green"},
                {'range': [3, 5], 'color': "yellow"},
                {'range': [6, 7], 'color': "orange"},
                {'range': [8, 10], 'color': "red"},
                {'range': [11, 15], 'color': "purple"}
            ]
        }
    ))

    recommendations = f"Risk Level: {risk_category}. "
    if risk_category in ["High", "Very High", "Extreme"]:
        recommendations += "Use sunscreen SPF 30+, wear a hat and sunglasses, avoid prolonged exposure."
    elif risk_category == "Moderate":
        recommendations += "Use sunscreen SPF 15+, and limit time outdoors."
    else:
        recommendations += "Minimal protection required. Enjoy your day!"

    return fig, recommendations


@callback(
    Output("med-result", "children"),
    [Input("med-state-dropdown", "value"),
     Input("skin-type-dropdown", "value"),
     Input("med-date-picker", "date"),
     Input("forecast-days-input", "value")]
)
def calculate_med(selected_state, skin_type_med, med_date, forecast_days):
    if not med_date or not selected_state:
        return "Please select a state and a date for MED calculation."

    med_date = pd.to_datetime(med_date)

    state_data = data[data['NAME'] == selected_state]
    if state_data.empty:
        return "No data available for the selected state."

    prophet_data = state_data[['Date', 'Clear Sky UVI']].rename(columns={'Date': 'ds', 'Clear Sky UVI': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_data)

    future = prophet_model.make_future_dataframe(periods=forecast_days)
    forecast = prophet_model.predict(future)

    forecast_row = forecast[forecast['ds'] == med_date]
    if forecast_row.empty:
        return "No forecast available for the selected date."

    uv_index = forecast_row['yhat'].iloc[0]
    time_to_erythema = skin_type_med / (uv_index * 25) if uv_index > 0 else "N/A"

    return f"Time to Erythema: {time_to_erythema:.2f} minutes" if isinstance(time_to_erythema, float) else "UV Index is too low for erythema risk."


@callback(
    Output("insights-collapse", "is_open"),
    [Input("toggle-insights-btn", "n_clicks")],
    [State("insights-collapse", "is_open")]
)
def toggle_insights(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("skin-risk-collapse", "is_open"),
    [Input("toggle-skin-risk-btn", "n_clicks")],
    [State("skin-risk-collapse", "is_open")]
)
def toggle_skin_risk(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("med-collapse", "is_open"),
    [Input("toggle-med-btn", "n_clicks")],
    [State("med-collapse", "is_open")]
)
def toggle_med(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@callback(
    Output("ten-day-forecast-table", "data"),
    [Input("skin-risk-location", "value"),
     Input("forecast-days-input", "value"),
     Input("ten-day-forecast-start-date", "date")]
)
def generate_ten_day_forecast(location, forecast_days, start_date):
    if not location or not start_date:
        return [] 

    start_date = pd.to_datetime(start_date)

    state_data = data[data['NAME'] == location]
    if state_data.empty:
        return []

    prophet_data = state_data[['Date', 'Clear Sky UVI']].rename(columns={'Date': 'ds', 'Clear Sky UVI': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_data)

    future = prophet_model.make_future_dataframe(periods=forecast_days)
    future = future[future['ds'] >= start_date] 

    forecast = prophet_model.predict(future)

    next_10_days = forecast[forecast['ds'] >= start_date].head(10)

    table_data = []
    for _, row in next_10_days.iterrows():
        uv_index = row['yhat']
        if uv_index <= 2:
            risk = "Low"
            recommendations = "Minimal protection required."
        elif uv_index <= 5:
            risk = "Moderate"
            recommendations = "Use sunscreen SPF 15+, limit outdoor time."
        elif uv_index <= 7:
            risk = "High"
            recommendations = "Use sunscreen SPF 30+, wear sunglasses."
        elif uv_index <= 10:
            risk = "Very High"
            recommendations = "Avoid prolonged sun exposure, use SPF 50+."
        else:
            risk = "Extreme"
            recommendations = "Stay indoors, avoid sun exposure."

        table_data.append({
            "date": row['ds'].date().strftime('%Y-%m-%d'),
            "uv_index": f"{uv_index:.2f}",
            "risk": risk,
            "recommendations": recommendations
        })

    return table_data

############# END - venkata pidaparthi #######
