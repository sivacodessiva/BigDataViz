from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import json
import dash_bootstrap_components as dbc


uv_data_path = 'todaysdata.csv'
geojson_path = 'us-states.json'

data = pd.read_csv(uv_data_path)
with open(geojson_path) as f:
    geojson = json.load(f)

data['Year'] = data['Year'].astype(int)
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

layout = html.Div(
    style={"backgroundColor": "#f8f9fa", "padding": "20px"},
    children=[
        html.H1(
            "Interactive UV Index Map",
            style={
                "textAlign": "center",
                "marginBottom": "20px",
                "color": "#343a40",
                "fontWeight": "bold",
            },
        ),
        # Filters Section
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-around",
                "flexWrap": "wrap",
                "marginBottom": "20px",
            },
            children=[
                dbc.Card(
                    style={"width": "250px", "padding": "20px", "margin": "10px"},
                    children=[
                        html.Label("Select Parameter:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="parameter-dropdown",
                            options=[
                                {"label": "Clear Sky UVI", "value": "Clear Sky UVI"},
                                {"label": "Cloudy Sky UVI", "value": "Cloudy Sky UVI"},
                                {"label": "Total Column Ozone", "value": "Total Column Ozone"},
                            ],
                            value="Clear Sky UVI",
                            clearable=False,
                        ),
                    ],
                ),
                dbc.Card(
                    style={"width": "250px", "padding": "20px", "margin": "10px"},
                    children=[
                        html.Label("Select Year:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": str(year), "value": year} for year in data["Year"].unique()
                            ],
                            value=data["Year"].max(),
                            clearable=False,
                        ),
                    ],
                ),
                dbc.Card(
                    style={"width": "250px", "padding": "20px", "margin": "10px"},
                    children=[
                        html.Label("Select Month:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="month-dropdown",
                            options=[
                                {"label": str(month), "value": month} for month in range(1, 13)
                            ],
                            value=1,
                            clearable=False,
                        ),
                    ],
                ),
                dbc.Card(
                    style={"width": "250px", "padding": "20px", "margin": "10px"},
                    children=[
                        html.Label("Select Day:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="day-dropdown",
                            options=[
                                {"label": str(day), "value": day} for day in range(1, 32)
                            ],
                            value=1,
                            clearable=False,
                        ),
                    ],
                ),
            ],
        ),
        # Map Section
        dcc.Store(id="map-relayout-data"),
        html.Div(
            children=[
                dcc.Graph(
                    id="uv-map",
                    style={
                        "height": "500px",
                        "width": "90%",
                        "margin": "auto",
                        "border": "2px solid #dee2e6",
                        "borderRadius": "10px",
                    },
                ),
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        # Date Slider
        html.Div(
            style={"padding": "20px", "textAlign": "center"},
            children=[
                html.Label("Select Date Range:", style={"fontWeight": "bold", "fontSize": "16px"}),
                dcc.Slider(
                    id="date-slider",
                    min=data["Date"].min().timestamp(),
                    max=data["Date"].max().timestamp(),
                    value=data["Date"].min().timestamp(),
                    marks={
                        int(date.timestamp()): date.strftime("%Y-%m-%d")
                        for date in pd.date_range(
                            start=data["Date"].min(), end=data["Date"].max(), freq="YE"
                        )
                    },
                    step=24 * 60 * 60,
                ),
            ],
        ),
        # State Visualization Section
        html.Div(
            children=[
                html.H3(
                    "State-Specific Data Visualization",
                    style={"textAlign": "center", "marginBottom": "20px", "color": "#343a40"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "flexWrap": "wrap",
                        "padding": "10px",
                    },
                    children=[
                        dbc.Card(
                            style={
                                "width": "400px",
                                "padding": "20px",
                                "margin": "10px",
                                "border": "2px solid #dee2e6",
                                "borderRadius": "10px",
                            },
                            children=[
                                dcc.Graph(
                                    id="state-bar-chart",
                                    style={"height": "300px"},
                                ),
                            ],
                        ),
                        dbc.Card(
                            style={
                                "width": "400px",
                                "padding": "20px",
                                "margin": "10px",
                                "border": "2px solid #dee2e6",
                                "borderRadius": "10px",
                            },
                            children=[
                                dcc.Graph(
                                    id="state-line-chart",
                                    style={"height": "300px"},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


def save_relayout_data(relayout_data, stored_relayout_data):
    if relayout_data is None:
        return stored_relayout_data
    return relayout_data


def update_map(selected_parameter, selected_year, selected_month, selected_day, selected_date, relayout_data):
    slider_date = pd.to_datetime(selected_date, unit="s")
    dropdown_date = pd.Timestamp(year=selected_year, month=selected_month, day=selected_day)

    final_date = dropdown_date if dropdown_date in data["Date"].values else slider_date
    filtered_data = data[data["Date"] == final_date]

    if filtered_data.empty:
        return px.choropleth(title="No data available for the selected date.")

    state_avg_data = filtered_data.groupby("NAME")[selected_parameter].mean().reset_index()

    fig = px.choropleth(
        state_avg_data,
        geojson=geojson,
        locations="NAME",
        featureidkey="properties.name",
        color=selected_parameter,
        color_continuous_scale="Viridis",
        title=f"{selected_parameter} on {final_date.strftime('%Y-%m-%d')}",
    )
    if relayout_data:
        fig.update_layout(relayout_data)

    return fig


def update_state_charts(click_data, selected_parameter):
    if click_data is None:
        return px.bar(title="No state selected"), px.line(title="No state selected")

    state_name = click_data["points"][0]["location"]
    state_data = data[data["NAME"] == state_name]

    if state_data.empty:
        return px.bar(title="No data available"), px.line(title="No data available")

    bar_fig = px.bar(
        state_data.groupby("Month")[selected_parameter].mean().reset_index(),
        x="Month",
        y=selected_parameter,
        title=f"Monthly Average {selected_parameter} for {state_name}",
    )

    line_fig = px.line(
        state_data,
        x="Date",
        y=selected_parameter,
        title=f"Daily {selected_parameter} for {state_name}",
    )

    return bar_fig, line_fig


def register_callbacks(app):
    app.callback(
        Output("map-relayout-data", "data"),
        Input("uv-map", "relayoutData"),
        State("map-relayout-data", "data"),
    )(save_relayout_data)

    app.callback(
        Output("uv-map", "figure"),
        [
            Input("parameter-dropdown", "value"),
            Input("year-dropdown", "value"),
            Input("month-dropdown", "value"),
            Input("day-dropdown", "value"),
            Input("date-slider", "value"),
        ],
        State("map-relayout-data", "data"),
    )(update_map)

    app.callback(
        [Output("state-bar-chart", "figure"), Output("state-line-chart", "figure")],
        [Input("uv-map", "clickData"), Input("parameter-dropdown", "value")],
    )(update_state_charts)


__all__ = ["layout", "register_callbacks"]
