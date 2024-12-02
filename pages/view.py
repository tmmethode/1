import dash  # type: ignore
from dash import html, dcc, dash_table  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
from data import GDP_EXCEL_FILE
from datetime import date

dash.register_page(__name__)


def get_dropdown_sheetnames():
    card_content = [
        dbc.CardHeader(dbc.Col("Datasets", className="figCard"), className="figTitle"),
        dbc.CardBody(
            [
                html.P("Select a dataset:", className="card-title", style={"color": "#284fa1"}),
                dcc.Dropdown(
                    id='view-dataset-dropdown',
                    options=[
                            {
                                "label": html.Span(['GDP National Accounts'], style={'color': 'black', 'font-size': 16}),
                                "value": "GDP",
                            },
                            {
                                "label": html.Span(['Consumer Price Index'], style={'color': 'black', 'font-size': 16}),
                                "value": "CPI",
                            },
                    ],
                    value='GDP',
                    clearable=False,
                ),
            ],
        ),
    ]
    return dbc.Card(card_content, color="white", style={"color": "#284fa1"})


table = dash_table.DataTable(
    data=GDP_EXCEL_FILE.to_dict('records'),  # type: ignore
    sort_action='native',
    filter_action='native',
    filter_options={"placeholder_text": "Filter column..."},
    style_header={
        'backgroundColor': '#284fa1',
        'color': 'white',
        'fontWeight': 'bold'
    },
    # style_data={
    #     'backgroundColor': 'rgb(50, 50, 50)',
    #     'color': 'white'
    #  },
    columns=[
        {"name": i, "id": i} for i in GDP_EXCEL_FILE.columns  # type: ignore
    ],
)


timeline = dcc.DatePickerRange(
        id='view-date-picker-range',
        min_date_allowed=date(1999, 1, 1),
        max_date_allowed=date(2024, 1, 1),
        initial_visible_month=date(2005, 1, 1),
        start_date=date(2005, 1, 1),
        end_date=date(2023, 12, 31)
    )

# the main gdp card
data_view_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("Gross Domestic Product", className="figCard", id="view-title"),
                dbc.Col(
                    className="d-flex justify-content-end",
                )
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    table
                ], style={"overflow": "scroll"})
            ], style={"padding": "0"},
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col("", id="view-info-footer"),
                dbc.Col(
                    [html.Label("Data from: ", className="label align-middle mr-2",
                                style={"vertical-align": "bottom", "font-size": 20, "font-wieght": "bold"}),
                     timeline
                     ], className="d-flex justify-content-end align-middle",
                )
            ], className="mb-2"),
        ], ),
    ], outline=False)


def layout():
    return [html.Div([
        html.Div(
            html.H1("Dashboard > Data View", className="h5 mb-0 text-gray-800"),
            className="d-sm-flex align-items-center justify-content-between mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(get_dropdown_sheetnames(), width=3),
                dbc.Col(),
                dbc.Col(),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(data_view_card, width=8),
                dbc.Col(width=4),
            ],
            className="mb-3",
        ),
    ])]
