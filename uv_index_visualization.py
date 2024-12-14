import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
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


app = dash.Dash(__name__)
app.title = "UV Index Visualization"

# Layout
app.layout = html.Div([
    html.H1("Interactive UV Index Map", style={"text-align": "center"}),

    html.Div([
        html.Div([
            html.Label("Select Parameter:"),
            dcc.Dropdown(
                id='parameter-dropdown',
                options=[
                    {'label': 'Clear Sky UVI', 'value': 'Clear Sky UVI'},
                    {'label': 'Cloudy Sky UVI', 'value': 'Cloudy Sky UVI'},
                    {'label': 'Total Column Ozone', 'value': 'Total Column Ozone'}
                ],
                value='Clear Sky UVI',
                clearable=False,
                style={"width": "200px", "margin": "auto"}
            ),
        ], style={"margin": "10px"}),

        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
                value=data['Year'].max(),
                clearable=False,
                style={"width": "200px", "margin": "auto"}
            ),
        ], style={"margin": "10px"}),

        html.Div([
            html.Label("Select Month:"),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': str(month), 'value': month} for month in range(1, 13)],
                value=1,
                clearable=False,
                style={"width": "200px", "margin": "auto"}
            ),
        ], style={"margin": "10px"}),

        html.Div([
            html.Label("Select Day:"),
            dcc.Dropdown(
                id='day-dropdown',
                options=[{'label': str(day), 'value': day} for day in range(1, 32)],
                value=1,
                clearable=False,
                style={"width": "200px", "margin": "auto"}
            ),
        ], style={"margin": "10px"}),
    ], style={"display": "flex", "justify-content": "center", "align-items": "center", "flex-wrap": "wrap"}),

    dcc.Store(id='map-relayout-data'),

    html.Div([
        dcc.Graph(id='uv-map', style={"height": "500px", "width": "1000px", "margin": "auto", "border": "2px solid black"}),
    ], style={"display": "flex", "justify-content": "center", "align-items": "center"}),

    html.Div([
        html.Label("Select Date Range:"),
        dcc.Slider(
            id='date-slider',
            min=data['Date'].min().timestamp(),
            max=data['Date'].max().timestamp(),
            value=data['Date'].min().timestamp(),
            marks={int(date.timestamp()): date.strftime('%Y-%m-%d') for date in pd.date_range(start=data['Date'].min(), end=data['Date'].max(), freq='Y')},
            step=24 * 60 * 60
        )
    ], style={"margin": "20px"}),

    html.Div([
        html.H3("State-Specific Data Visualization", style={"text-align": "center"}),
        html.Div([
            dcc.Graph(id='state-bar-chart', style={"height": "300px", "width": "400px", "margin": "10px", "border": "2px solid black"})
        ], style={"display": "flex", "justify-content": "center", "align-items": "center"}),
        html.Div([
            dcc.Graph(id='state-line-chart', style={"height": "300px", "width": "400px", "margin": "10px", "border": "2px solid black"})
        ], style={"display": "flex", "justify-content": "center", "align-items": "center"})
    ])
])


@app.callback(
    Output('map-relayout-data', 'data'),
    Input('uv-map', 'relayoutData'),
    State('map-relayout-data', 'data')
)
def save_relayout_data(relayout_data, stored_relayout_data):
    if relayout_data is None:
        return stored_relayout_data
    return relayout_data


@app.callback(
    Output('uv-map', 'figure'),
    [Input('parameter-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('day-dropdown', 'value'),
     Input('date-slider', 'value')],
    State('map-relayout-data', 'data')
)
def update_map(selected_parameter, selected_year, selected_month, selected_day, selected_date, relayout_data):
    slider_date = pd.to_datetime(selected_date, unit='s')
    dropdown_date = pd.Timestamp(year=selected_year, month=selected_month, day=selected_day)

    
    final_date = dropdown_date if dropdown_date in data['Date'].values else slider_date

    
    filtered_data = data[data['Date'] == final_date]

    
    state_avg_data = filtered_data.groupby('NAME')[selected_parameter].mean().reset_index()

    
    fig = px.choropleth(
        state_avg_data,
        geojson=geojson,
        locations='NAME',
        featureidkey='properties.name',
        color=selected_parameter,
        color_continuous_scale="Viridis",
        title=f"{selected_parameter} on {final_date.strftime('%Y-%m-%d')}",
        labels={selected_parameter: selected_parameter}
    )

    
    if relayout_data:
        fig.update_layout(relayout_data)

    return fig


@app.callback(
    [Output('state-bar-chart', 'figure'),
     Output('state-line-chart', 'figure')],
    [Input('uv-map', 'clickData'),
     Input('parameter-dropdown', 'value')]
)
def update_state_charts(click_data, selected_parameter):
    if click_data is None:
        empty_fig = px.bar(title="Click a state on the map to view data")
        return empty_fig, empty_fig

    state_name = click_data['points'][0]['location']

    state_data = data[data['NAME'] == state_name]

    bar_fig = px.bar(
        state_data.groupby('Month')[selected_parameter].mean().reset_index(),
        x='Month',
        y=selected_parameter,
        title=f"Monthly Average of {selected_parameter} for {state_name}",
        labels={"Month": "Month", selected_parameter: selected_parameter},
        color_discrete_sequence=px.colors.qualitative.Set2
    )


    line_fig = px.line(
        state_data,
        x='Date',
        y=selected_parameter,
        title=f"Daily {selected_parameter} for {state_name}",
        labels={"Date": "Date", selected_parameter: selected_parameter},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    return bar_fig, line_fig


if __name__ == '__main__':
    app.run_server(debug=True)
