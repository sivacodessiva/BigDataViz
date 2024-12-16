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


app.layout = html.Div([
    html.H1("UV Index Visual Analytics", style={"text-align": "center"}),

    html.Div(
        style={"backgroundColor": "#f8f9fa", "minHeight": "100vh", "padding": "20px"},
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content")
        ]
    )
])

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
                            "UV Index Visualizations",
                            style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "color": "#343a40"}
                        ),
                        html.P(
                            "Visualizations of UV Index trends and data points.",
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
                            "Forecasting - Regression Model",
                            style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "color": "#343a40"}
                        ),
                        html.P(
                            "Regression Model for Cloudy Sky UVI forecasting with different influencing factors.",
                            style={"fontSize": "14px", "color": "#6c757d"}
                        ),
                        dbc.Button(
                            "Go to Regression Model Forecasting",
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
                            "Forecasting using Prophet model",
                            style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "color": "#343a40"}
                        ),
                        html.P(
                            "Predictive analysis and forecasts of UV Index levels for future dates, Skin Damage Risk Analysis, Minimal Erythemal Doese (MED) Analysis",
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
                            "Analyze and visualize derived factors of UV Index",
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
