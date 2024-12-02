import dash  # type: ignore
from dash import html, dcc, Input, Output, callback  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
from data import GDP_EXCEL_FILE, GDP_FOR_ALL_COUNTRY, GDP_years


dash.register_page(__name__)


africa_dropdown_years = dcc.Dropdown(
                    id='africa-year-dropdown',
                    options=[
                            {
                                "label": html.Span(year, style={'color': 'black', 'font-size': 12}),
                                "value": year,
                            } for year in GDP_years  # type: ignore
                    ],
                    value=GDP_years[-1],
                    clearable=False,
                    style={"width": "110px"}
                ),

africa_gdp_card = dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col("Rwanda GDP Comparison in Africa"),
                dbc.Col(africa_dropdown_years, className="d-flex justify-content-end")
            ]
        )
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
            ], id="africa-list")
        ], style={"padding": "0"},
    ),
    dbc.CardFooter([html.Sup("*", style={"color": "red"}), "Source: Kaggle"]),
], outline=False)


world_dropdown_years = dcc.Dropdown(
                    id='world-year-dropdown',
                    options=[
                            {
                                "label": html.Span(year, style={'color': 'black', 'font-size': 12}),
                                "value": year,
                            } for year in GDP_years  # type: ignore
                    ],
                    value=GDP_years[-1],
                    clearable=False,
                    style={"width": "110px"}
                ),

world_gdp_card = dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col("Rwanda GDP Comparison to the world", width=6),
                dbc.Col(world_dropdown_years, className="d-flex justify-content-end", width=6)
            ]
        )
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div(id="world-list"),
        ], style={"padding": "0"},
    ),
    dbc.CardFooter([html.Sup("*", style={"color": "red"}), "Source: Kaggle"]),
], outline=False)


dgp_2017_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/GDP.jpg",
                        className="img-fluid mt-0 mb-0",
                        style={"height": "153px", "padding": "0", "margin": "0"},
                    ),
                    className="col-md-5",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H6("Constant 2017 prices, Billions RFW", className="card-title"),
                            html.Small(
                                GDP_EXCEL_FILE['Years'].values[-1],  # type: ignore
                                className="card-text text-muted",
                            ),
                            html.P(GDP_EXCEL_FILE['GDP at constant 2017 prices'].values[-1],  # type: ignore
                                    className="card-text",  # noqa
                                    style={"font": "bold", "font-size": 45, 'color': "#97d26f", "text-align": "right"}),  # noqa
                        ]
                    ),
                    className="col-md-7",
                ),
            ],
            className="g-0 d-flex align-items-center",
            style={"padding": "0", "margin": "0"},
        )
    ],
    style={"maxWidth": "540px", "padding": "0"},
)

dgp_current_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/gdp.jpg",
                        className="img-fluid mt-0 mb-0",
                        style={"height": "153px", "padding": "0", "margin": "0"},
                    ),
                    className="col-md-5",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H6("Current prices, Billions RFW", className="card-title"),
                            html.Small(
                                GDP_EXCEL_FILE['Years'].values[-1],  # type: ignore
                                className="card-text text-muted",
                            ),
                            html.P(GDP_EXCEL_FILE['GDP at current prices'].values[-1],  # type: ignore
                                    className="card-text",  # noqa
                                    style={"font": "bold", "font-size": 45, 'color': "#419b3c", "text-align": "right"}),  # noqa
                        ]
                    ),
                    className="col-md-7",
                ),
            ],
            className="g-0 d-flex align-items-center",
            style={"padding": "0", "margin": "0"},
        )
    ],
    style={"maxWidth": "540px", "padding": "0"},
)


# GDP Card
gdp_card = dbc.Card(
    [
        dbc.CardHeader("Gross Domestic Product (GDP)", style={"color": "#284fa1"}),
        dbc.CardBody(
            [
                html.P(
                    "GDP represents the total value of all goods and services produced "
                    "within a country's borders over a specific time period.",
                    className="card-text",
                ),
                html.P(
                    "It is a key indicator of a country's economic health and is often "
                    "used to assess and compare the economic performance of different nations.",
                    className="card-text",
                ),
            ]
        ),
    ],
    color="#284fa1",
    inverse=True,
)

# CPI Card
cpi_card = dbc.Card(
    [
        dbc.CardHeader("Consumer Price Index (CPI)", style={"color": "#284fa1"}),
        dbc.CardBody(
            [
                html.P(
                    "CPI is a measure that examines the average change in prices paid by "
                    "consumers for a basket of goods and services over time.",
                    className="card-text",
                ),
                html.P(
                    "It is widely used to assess inflation and to adjust income and spending "
                    "for changes in the cost of living.",
                    className="card-text",
                ),
            ]
        ),
    ],
    color="success",
    inverse=True,
)


# CPI Card
welome_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Container(
                            [
                                html.H1("Welcome to the NISR Hackathon Dashboard", className="display-4"),
                                html.P("This dashboard showcases statistical data visualizations generated using Python. "
                                    "Explore the various features to gain insights into the provided datasets.", className="lead"),

                                html.H2("Key Features", className="mt-4"),
                                html.Ul([
                                    html.Li(["Interactive visualizations of NISR datasets:",
                                            html.Ul([
                                                html.Li("GDP National Accounts"),
                                                html.Li("Consumer Price Index"),
                                                # Add more features as needed
                                            ], className="list-styled"),]),
                                    html.Li("Data exploration tools and filters."),
                                    html.Li("Insights and trends analysis."),
                                    # Add more features as needed
                                ], className="list-styled"),

                                html.P("To get started, use the sidebar navigation to explore different sections of the dashboard.",
                                    className="mt-3 font-italic"),
                            ],
                            fluid=True  # Use a fluid layout for a full-width container
                        )
                    ],
                    className="mb-3 py-0 px-0 mt-4",
                ),
            ]
        ),
    ],
    color="info",
    inverse=True,
    className="mb-3",
)


def layout():
    return html.Div([
        html.Div(
            html.H1("Dashboard > Overview", className="h3 mb-0 text-gray-800"),
            className="d-sm-flex align-items-center justify-content-between mb-4",
        ),
        welome_card,
        dbc.Row(
            [
                dbc.Col(gdp_card, width=6),
                dbc.Col(cpi_card, width=6),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [

                dbc.Col(africa_gdp_card, width=3),
                dbc.Col(world_gdp_card, width=3),
                dbc.Col(dgp_2017_card, width=3),
                dbc.Col(dgp_current_card, width=3),
            ],
            className="mb-3 mt-2 py-0 px-0",
        ),
    ])


@callback(
    [Output("africa-list", "children")],
    [
        Input("africa-year-dropdown", "value"),
    ],
)
def gdp_africa_year_dropdown_on_change(items_value):
    data = GDP_FOR_ALL_COUNTRY[GDP_FOR_ALL_COUNTRY['year'] == items_value]
    # Select records where the 'Region' column contains the word 'Africa'
    africa_data = data[data['region'].str.contains('Sub-Saharan Africa', case=False, regex=False)]

    data = africa_data.sort_values(by="value", ascending=False).reset_index()
    top_5_df = data.nlargest(4, 'value')
    rwanda_gdp = data.loc[data['country_name'] == 'Rwanda', 'value'].values[0]
    position = data[data['value'] > rwanda_gdp].shape[0] + 1
    top_5_countries = [
        html.Li(f"{index+1} - {row['country_name']}: ${row['value']}", className='list-group-item')
        for index, row in top_5_df.iterrows()
    ]
    if "Rwanda" not in top_5_df['country_name']:
        top_5_countries += [html.Li(f"{position} - Rwanda: ${rwanda_gdp}", className='list-group-item')]
    output = [html.Ul(top_5_countries, className='list-group')]
    return [output]


@callback(
    [Output("world-list", "children")],
    [
        Input("world-year-dropdown", "value"),
    ],
)
def gdp_world_year_dropdown_on_change(items_value):
    data = GDP_FOR_ALL_COUNTRY[GDP_FOR_ALL_COUNTRY['year'] == items_value]
    data = data.sort_values(by="value", ascending=False).reset_index()
    top_5_df = data.nlargest(4, 'value')
    rwanda_gdp = data.loc[data['country_name'] == 'Rwanda', 'value'].values[0]
    position = data[data['value'] > rwanda_gdp].shape[0] + 1
    top_5_countries = [
        html.Li(f"{index+1} - {row['country_name']}: ${row['value']}", className='list-group-item')
        for index, row in top_5_df.iterrows()
    ]
    if "Rwanda" not in top_5_df['country_name']:
        top_5_countries += [html.Li(f"{position} - Rwanda: ${rwanda_gdp}", className='list-group-item')]
    output = [html.Ul(top_5_countries, className='list-group')]
    return [output]
