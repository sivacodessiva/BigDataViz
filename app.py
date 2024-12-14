import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from uv_visualization import layout as uv_layout, register_callbacks
from dynamic_calculations import layout as dynamic_layout
from forecasting import layout as forecasting_layout 
from derived_factors import layout as derived_factors_layout  

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "UV Index Dashboard"

register_callbacks(app)


app.layout = html.Div(
    style={"backgroundColor": "#f8f9fa", "minHeight": "100vh", "padding": "20px"},
    children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content")
    ]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/uv-visualization":
        return uv_layout
    elif pathname == "/dynamic-calculations":
        return dynamic_layout
    elif pathname == "/forecasting":
        return forecasting_layout
    elif pathname == "/derived-factors":
        return derived_factors_layout 
    else:
        # Home Page layout
        return html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "center",
                "gap": "20px"
            },
            children=[
                # Box 1
                html.Div(
                    style={
                        "width": "300px",
                        "padding": "20px",
                        "border": "2px solid #dee2e6",
                        "borderRadius": "10px",
                        "backgroundColor": "#ffffff",
                        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3(
                            "UV Index Visualization",
                            style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "color": "#343a40"}
                        ),
                        html.P(
                            "Explore detailed visualizations of UV Index trends and data points.",
                            style={"fontSize": "14px", "color": "#6c757d"}
                        ),
                        dbc.Button(
                            "Go to UV Index Visualization",
                            href="/uv-visualization",
                            color="primary",
                            style={"marginTop": "10px"}
                        )
                    ]
                ),
                # Box 2
                html.Div(
                    style={
                        "width": "300px",
                        "padding": "20px",
                        "border": "2px solid #dee2e6",
                        "borderRadius": "10px",
                        "backgroundColor": "#ffffff",
                        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3(
                            "Dynamic Calculations",
                            style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "color": "#343a40"}
                        ),
                        html.P(
                            "Perform dynamic calculations using custom parameters and analyze results.",
                            style={"fontSize": "14px", "color": "#6c757d"}
                        ),
                        dbc.Button(
                            "Go to Dynamic Calculations",
                            href="/dynamic-calculations",
                            color="success",
                            style={"marginTop": "10px"}
                        )
                    ]
                ),
                # Box 3
                html.Div(
                    style={
                        "width": "300px",
                        "padding": "20px",
                        "border": "2px solid #dee2e6",
                        "borderRadius": "10px",
                        "backgroundColor": "#ffffff",
                        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3(
                            "Forecasting",
                            style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "color": "#343a40"}
                        ),
                        html.P(
                            "View predictive analysis and forecasts of UV Index levels for future dates.",
                            style={"fontSize": "14px", "color": "#6c757d"}
                        ),
                        dbc.Button(
                            "Go to Forecasting",
                            href="/forecasting",
                            color="info",
                            style={"marginTop": "10px"}
                        )
                    ]
                ),
                # Box 4
                html.Div(
                    style={
                        "width": "300px",
                        "padding": "20px",
                        "border": "2px solid #dee2e6",
                        "borderRadius": "10px",
                        "backgroundColor": "#ffffff",
                        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3(
                            "Derived Factors Analysis",
                            style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "color": "#343a40"}
                        ),
                        html.P(
                            "Analyze and visualize derived factors from UV Index data for deeper insights.",
                            style={"fontSize": "14px", "color": "#6c757d"}
                        ),
                        dbc.Button(
                            "Go to Derived Factors Analysis",
                            href="/derived-factors",
                            color="warning",
                            style={"marginTop": "10px"}
                        )
                    ]
                )
            ]
        )

if __name__ == "__main__":
    app.run_server(debug=True)
