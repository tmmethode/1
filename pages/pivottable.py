import dash  # type: ignore
from dash import html  # type: ignore

dash.register_page(__name__)


def layout():
    return [html.Div([
        html.Div(
            html.H1("Dashboard > Pivot Table", className="h5 mb-0 text-gray-800"),
            className="d-sm-flex align-items-center justify-content-between mb-4",
        ),
    ])]
