import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import numpy as np


uv_data_path = 'todaysdata.csv'
data = pd.read_csv(uv_data_path)

data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

layout = html.Div([
    html.H1("Derived Factor Calculations", style={"text-align": "center"}),


    html.Div([
        html.Label("Select Location:"),
        dcc.Dropdown(
            id='location-dropdown',
            options=[{'label': loc, 'value': loc} for loc in data['NAME'].unique()],
            value=data['NAME'].unique()[0],
            clearable=False,
            style={"width": "400px", "margin": "10px auto"}
        ),
        html.Label("Select Date Range:"),
        dcc.DatePickerRange(
            id='date-range-picker',
            start_date=data['Date'].min(),
            end_date=data['Date'].max(),
            display_format="YYYY-MM-DD",
            style={"margin": "10px auto"}
        ),
        html.Label("Select Derived Factors to Calculate:"),
        dcc.Checklist(
            id='factor-checklist',
            options=[
                {'label': 'Direct and Diffuse UV Components', 'value': 'direct_diffuse'},
                {'label': 'UV Attenuation Factor', 'value': 'uv_attenuation'},
                {'label': 'Cloud Impact Factor', 'value': 'cloud_impact'},
                {'label': 'Ozone Protection Factor', 'value': 'ozone_protection'},
                {'label': 'Transmission Efficiency', 'value': 'transmission_efficiency'},
                {'label': 'Solar Energy Potential Adjustment', 'value': 'solar_energy_potential'},
                {'label': 'Weighted UV Exposure', 'value': 'weighted_uv'}
            ],
            value=['direct_diffuse', 'uv_attenuation'],
            style={"width": "400px", "margin": "10px auto"}
        ),
        html.Button("Calculate", id="calculate-btn", n_clicks=0, style={"margin": "10px auto", "display": "block"})
    ], style={"text-align": "center", "border": "1px solid black", "padding": "10px", "margin": "10px"}),


    html.Div([
        html.H4("Derived Factor Visualizations", style={"text-align": "center"}),
        dcc.Graph(id="derived-factor-visualization", style={"height": "500px", "border": "2px solid black"})
    ], style={"border": "1px solid black", "padding": "10px", "margin": "10px"})
])


@callback(
    Output("derived-factor-visualization", "figure"),
    [Input("calculate-btn", "n_clicks")],
    [State("location-dropdown", "value"),
     State("date-range-picker", "start_date"),
     State("date-range-picker", "end_date"),
     State("factor-checklist", "value")]
)
def calculate_derived_factors(n_clicks, location, start_date, end_date, factors):
    if n_clicks == 0:
        return go.Figure()

    global data

    filtered_data = data[(data['NAME'] == location) & 
                         (data['Date'] >= pd.to_datetime(start_date)) & 
                         (data['Date'] <= pd.to_datetime(end_date))]


    results = filtered_data.copy()

    if 'direct_diffuse' in factors:
        results['Direct UV'] = results['Clear Sky UVI'] * (results['Aerosol Transmission'] / 100) * \
                               np.cos(np.radians(results['Solar Zenith Angle']))
        results['Diffuse UV'] = results['Clear Sky UVI'] - results['Direct UV']

    if 'uv_attenuation' in factors:
        results['UV Attenuation'] = 1 - (results['Cloudy Sky UVI'] / results['Clear Sky UVI'])

    if 'cloud_impact' in factors:
        results['Cloud Impact Factor'] = 1 - (results['Cloud Transmission'] / 100)

    if 'ozone_protection' in factors:
        kappa = 0.02  
        results['Ozone Protection Factor'] = 1 - np.exp(-kappa * results['Total Column Ozone'])

    if 'transmission_efficiency' in factors:
        results['Transmission Efficiency'] = (results['Cloud Transmission'] / 100) * (results['Aerosol Transmission'] / 100)

    if 'solar_energy_potential' in factors:
        base_irradiance = 1000  
        results['Solar Energy Potential'] = base_irradiance * (results['Cloud Transmission'] / 100) * (results['Aerosol Transmission'] / 100)

    if 'weighted_uv' in factors:
        action_spectrum_weight = 0.7  
        results['Weighted UV'] = results['Clear Sky UVI'] * action_spectrum_weight

    
    fig = go.Figure()
    if 'direct_diffuse' in factors:
        fig.add_trace(go.Scatter(x=results['Date'], y=results['Direct UV'], mode='lines', name='Direct UV'))
        fig.add_trace(go.Scatter(x=results['Date'], y=results['Diffuse UV'], mode='lines', name='Diffuse UV'))

    if 'uv_attenuation' in factors:
        fig.add_trace(go.Scatter(x=results['Date'], y=results['UV Attenuation'], mode='lines', name='UV Attenuation'))

    if 'cloud_impact' in factors:
        fig.add_trace(go.Scatter(x=results['Date'], y=results['Cloud Impact Factor'], mode='lines', name='Cloud Impact Factor'))

    if 'ozone_protection' in factors:
        fig.add_trace(go.Scatter(x=results['Date'], y=results['Ozone Protection Factor'], mode='lines', name='Ozone Protection Factor'))

    if 'transmission_efficiency' in factors:
        fig.add_trace(go.Scatter(x=results['Date'], y=results['Transmission Efficiency'], mode='lines', name='Transmission Efficiency'))

    if 'solar_energy_potential' in factors:
        fig.add_trace(go.Scatter(x=results['Date'], y=results['Solar Energy Potential'], mode='lines', name='Solar Energy Potential'))

    if 'weighted_uv' in factors:
        fig.add_trace(go.Scatter(x=results['Date'], y=results['Weighted UV'], mode='lines', name='Weighted UV'))

    fig.update_layout(title="Derived Factor Trends", xaxis_title="Date", yaxis_title="Values")

    return fig
