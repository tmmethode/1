from dash import html, callback, Output, Input, dcc, State  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import dash  # type: ignore
import pandas as pd  # type: ignore
from config import CONFIG
import plotly.express as px  # type: ignore
from data import CPI_EXCEL_FILE
from llm import chat_with_csv


dash.register_page(__name__)

data = CPI_EXCEL_FILE

# Get the months
months = pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime("%b %Y")  # type: ignore

# years
years = sorted(pd.to_datetime(data["Urban"]["Date"][1:]).dt.year.unique())  # type: ignore

graphs = []

# Plot 1: Urban vs. Rural vs. All Rwanda CPI
graph1 = dcc.Graph(
    id='dynamic-plot',
    config=CONFIG
)

graphs.append(dbc.Card([
    dbc.CardHeader(
        dbc.Row([
            dbc.Col("Urban vs. Rural vs. All Rwanda CPI", ),
            dbc.Col(dbc.RadioItems(
                id='plot-selection',
                options=[
                    {'label': html.Span('All CPI'), 'value': 'current'},
                    {'label': 'Average CPI', 'value': 'average'}
                ],
                value='current', inline=True
            ), className="d-flex justify-content-end")]), className="figTitle"
    ),
    dbc.CardBody(
        [
            html.Div([
                graph1
            ])
        ], style={"padding": "0"},
    ),
    dbc.CardFooter([
            dbc.Row([
                dbc.Col(id="graph1-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="graph1-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="graph1-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="graph1-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True
                )
            )
        ], ),
], outline=False))

# Plot 2: Urban vs. Rural vs. All Rwanda Weights
graph2 = dcc.Graph(
    id='plot2',
    figure={
        'data': [
            {'x': data["Urban"].columns[2:], 'y': data["Urban"].iloc[0, 2:], 'type': 'bar', 'name': 'Urban'},  # type: ignore
            {'x': data["Rural"].columns[2:], 'y': data["Rural"].iloc[0, 2:], 'type': 'bar', 'name': 'Rural'},  # type: ignore
            {'x': data["All Rwanda"].columns[2:], 'y': data["All Rwanda"].iloc[0, 2:], 'type': 'bar', 'name': 'All Rwanda'}  # type: ignore  # noqa
        ],
        'layout': {
            'title': '',
            'barmode': 'group',
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
            'margin': {'l': 30, 'r': 9, 't': 30},  # margin
        }
    }, config=CONFIG
)
graphs.append(dbc.Card([
    dbc.CardHeader(dbc.Col("Urban vs. Rural vs. All Rwanda Weights", className="figCard"), className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph2
            ])
        ], style={"padding": "0"},
    ),
    dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "284fa1"}), "Comparison by Foods."]),
                        id="graph2-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="graph2-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="graph2-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="graph2-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True,
                )
            )
        ], ),
], outline=False))

# Plot 3: CPI Yearly for Urban
graph3 = dcc.Graph(id='combined-cpi-graph', config=CONFIG)

graphs.append(dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col(id='cpi-year-title'),
                dbc.Col([
                    # year selection
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': html.Span(year, style={'color': 'black', 'font-size': 15}), 'value': year} for year in years],  # noqa
                        value=years[-1],  # Default value is the latest year
                        clearable=False,
                        style={"width": "80px", "margin-right": "3px"},
                        className="mr-2 me-2"
                    ),
                    dbc.RadioItems(
                        id='graph-type-selection',
                        options=[
                            {'label': 'Monthly', 'value': 'cpi_monthly'},
                            {'label': 'Monthly Change', 'value': 'cpi_monthly_change'},
                            {'label': 'Histogram', 'value': 'cpi_histogram'}
                        ],
                        value='cpi_monthly', inline=True, className="ml-2"
                    ),
                ], className="d-flex justify-content-end"),
            ]
        )
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph3
            ])
        ], style={"padding": "0"},
    ),
    dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "#284fa1"}), ""]),
                        id="graph3-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="graph3-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="graph3-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="graph3-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True,
                )
            )
        ], ),
], outline=False))

graph4 = dcc.Graph(
            id='cpi-annual-change',
            figure={
                'data': [
                    # Urban
                    {
                        'x': [date for date in data['Urban']['Date'][1:]],  # type: ignore
                        'y': [value for value in data["Urban"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100],  # type: ignore  # noqa
                        'type': 'line', 'name': 'Urban'},

                    # Rural
                    {
                        'x': [date for date in data['Rural']['Date'][1:]],  # type: ignore
                        'y': [value for value in data["Rural"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100],  # type: ignore  # noqa
                        'type': 'line', 'name': 'Rural'},

                    # All Rwanda
                    {
                        'x': [date for date in data['All Rwanda']['Date'][1:]],  # type: ignore
                        'y': [value for value in data["All Rwanda"]['GENERAL INDEX (CPI)'][1:].pct_change(periods=12) * 100],  # type: ignore  # noqa
                        'type': 'line', 'name': 'All Rwanda'}
                ],
                'layout': {
                    'title': '',
                    'xaxis': {
                        'tickmode': 'linear',
                        'dtick': "M12",
                        'tickformat': "%Y"
                    },
                    'yaxis': {
                        'title': None
                    },
                    'paper_bgcolor': 'rgb(243, 243, 243)',
                    'plot_bgcolor': 'rgb(243, 243, 243)',
                    'margin': {'l': 30, 'r': 9, 't': 30, 'b': 35},  # margin
                }
            }
        )

graphs.append(dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col("CPI Annual Change", id='cpi-year-title-3', className="figCard"),
                dbc.Col([
                ])
            ]
        )
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph4
            ])
        ], style={"padding": "0"},
    ),
    dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "#284fa1"}), "Change in %"]),
                        id="graph4-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="graph4-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="graph4-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="graph4-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True,
                )
            )
        ], ),
], outline=False))

graph5 = dcc.Graph(id='cpi-bar-chart', config=CONFIG)
regions = ['Urban', 'Rural', 'All Rwanda']
graphs.append(dbc.Card([
    dbc.CardHeader([
        dbc.Row(
            [
                dbc.Col("Monthly CPI Values by Year", id='cpi-year-title-6', className="figCard"),
                dbc.Col([
                    # year selection
                    dcc.Dropdown(
                        id='cpi-region-selector-dropdown',
                        options=[
                            {
                                "label": html.Span(region, style={'color': 'black'}),
                                "value": region,
                            } for region in regions
                        ],
                        value=regions[0],  # Default value is the latest year
                        clearable=False
                    ),
                ])
            ]
        )
    ], className="figTitle"),
    dbc.CardBody(
        [
            html.Div([
                graph5
            ])
        ], style={"padding": "0"},
    ),
    dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "orange"}), "Exchange rate: Rwf per US dollar"]),
                        id="graph5-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="graph5-ai-loading"), size="sm"), " Explain"],
                        color="primary",
                        id="graph5-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="graph5-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True,
                )
            )
        ], ),
], outline=False))


# Render the CPI content
def layout():
    content = html.Div([
        dbc.Row(
            [
                dbc.Col(graphs[0], width=6),
                dbc.Col(graphs[3], width=6),
            ],
            className="mb-3 py-0 px-0",
        ),
        dbc.Row(
            [
                dbc.Col(graphs[2], width=6),
                dbc.Col(graphs[1], width=6),
            ],
            className="mb-3 py-0 px-0",
        ),
        dbc.Row(
            [
                dbc.Col(graphs[4]),
            ],
            className="mb-3 py-0 px-0",
        ),
    ])

    return [html.Div([
        html.Div(
            html.H1("Dashboard > Consumer Price Index", className="h5 mb-0 text-gray-800"),
            className="d-sm-flex align-items-center justify-content-between mb-4",
        ),
        html.Div([content], id="graphs-container")])]


# computer yearly average CPI
def compute_yearly_average(data, category):
    data_filtered = data[category][1:]
    data_filtered['Date'] = pd.to_datetime(data_filtered['Date'])

    # Group by year
    yearly_data = data_filtered.groupby(data_filtered['Date'].dt.year).mean()
    return yearly_data


# callback for average CPI plot and All CPI plot
@callback(
    [Output('dynamic-plot', 'figure'),
     Output('graph1-info-footer', 'children')],
    [Input('plot-selection', 'value')]
)
def all_n_average(plot_type):
    title = ""
    if plot_type == 'average':
        title = html.Span([html.Sup("*", style={"color": "#284fa1"}), "Yearly average CPI values"])
        # Compute yearly averages
        urban_avg = compute_yearly_average(data, "Urban")
        rural_avg = compute_yearly_average(data, "Rural")
        all_rwanda_avg = compute_yearly_average(data, "All Rwanda")

        # Create the average CPI plot
        average_cpi_plot = {
            'data': [
                {'x': urban_avg.index, 'y': urban_avg['GENERAL INDEX (CPI)'], 'type': 'line', 'name': 'Urban Average'},
                {'x': rural_avg.index, 'y': rural_avg['GENERAL INDEX (CPI)'], 'type': 'line', 'name': 'Rural Average'},
                {'x': all_rwanda_avg.index,
                 'y': all_rwanda_avg['GENERAL INDEX (CPI)'], 'type': 'line', 'name': 'All Rwanda Average'}
            ],
            'layout': {
                'title': '',
                'xaxis': {'title': None, 'tickangle': 45},
                'yaxis': {'title': None},
                'paper_bgcolor': 'rgb(243, 243, 243)',
                'plot_bgcolor': 'rgb(243, 243, 243)',
                'margin': {'l': 30, 'r': 9, 't': 30, 'b': 50},  # margin
            }
        }
        return average_cpi_plot, title
    else:
        # Urban vs. Rural vs. All Rwanda CPI plot
        title = html.Span([html.Sup("*", style={"color": "#284fa1"}), "Monthly CPI values"])
        return {
            'data': [
                {'x': months, 'y': data["Urban"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Urban'},
                {'x': months, 'y': data["Rural"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'Rural'},
                {'x': months, 'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:], 'type': 'line', 'name': 'All Rwanda'}
            ],
            'layout': {
                'title': '',
                'xaxis': {'title': None, 'tickangle': 45},
                'yaxis': {'title': None},
                'paper_bgcolor': 'rgb(243, 243, 243)',
                'plot_bgcolor': 'rgb(243, 243, 243)',
                'margin': {'l': 30, 'r': 9, 't': 30, 'b': 50},  # margin
            }
        }, title


# cpi monthly
def CPI_Monthly(selected_year):
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year
    return {
        'data': [
            {
                'x': pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime('%B').iloc[mask_urban.values],
                'y': data["Urban"]["GENERAL INDEX (CPI)"][1:].iloc[mask_urban.values],
                'type': 'line',
                'name': 'Urban'
            },
            {
                'x': pd.to_datetime(data["Rural"]["Date"][1:]).dt.strftime('%B').iloc[mask_rural.values],
                'y': data["Rural"]["GENERAL INDEX (CPI)"][1:].iloc[mask_rural.values],
                'type': 'line',
                'name': 'Rural'
            },
            {
                'x': pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.strftime('%B').iloc[mask_all_rwanda.values],
                'y': data["All Rwanda"]["GENERAL INDEX (CPI)"][1:].iloc[mask_all_rwanda.values],
                'type': 'line',
                'name': 'All Rwanda'
            }
        ],
        'layout': {
            'title': None,
            'xaxis': {
                'ticktext': ['January', 'February', 'March', 'April',
                             'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            },
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
            'margin': {'l': 30, 'r': 9, 't': 30, 'b': 50},  # margin
        }
    }


# cpi monthly change
def CPI_monthly_change(selected_year):
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year

    monthly_change_urban = data["Urban"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100
    monthly_change_rural = data["Rural"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100
    monthly_change_all_rwanda = data["All Rwanda"]["GENERAL INDEX (CPI)"][1:].pct_change() * 100

    return {
        'data': [
            {
                'x': pd.to_datetime(data["Urban"]["Date"][1:]).dt.strftime('%B').iloc[mask_urban.values],
                'y': monthly_change_urban.iloc[mask_urban.values],
                'type': 'line',
                'name': 'Urban'
            },
            {
                'x': pd.to_datetime(data["Rural"]["Date"][1:]).dt.strftime('%B').iloc[mask_rural.values],
                'y': monthly_change_rural.iloc[mask_rural.values],
                'type': 'line',
                'name': 'Rural'
            },
            {
                'x': pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.strftime('%B').iloc[mask_all_rwanda.values],
                'y': monthly_change_all_rwanda.iloc[mask_all_rwanda.values],
                'type': 'line',
                'name': 'All Rwanda'
            }
        ],
        'layout': {
            'title': None,
            'xaxis': {
                'ticktext': ['January', 'February', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'November', 'December']
            },
            'yaxis': {
                'title': None
            },
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
            'margin': {'l': 30, 'r': 9, 't': 30, 'b': 50},  # margin
        }
    }


# cpi histogram
def CPI_histogram(selected_year):
    mask_urban = pd.to_datetime(data["Urban"]["Date"][1:]).dt.year == selected_year
    mask_rural = pd.to_datetime(data["Rural"]["Date"][1:]).dt.year == selected_year
    mask_all_rwanda = pd.to_datetime(data["All Rwanda"]["Date"][1:]).dt.year == selected_year

    cpi_urban = data["Urban"]["GENERAL INDEX (CPI)"][1:][mask_urban]
    cpi_rural = data["Rural"]["GENERAL INDEX (CPI)"][1:][mask_rural]
    cpi_all_rwanda = data["All Rwanda"]["GENERAL INDEX (CPI)"][1:][mask_all_rwanda]

    cpi_data = pd.DataFrame({'Urban': cpi_urban, 'Rural': cpi_rural, 'All Rwanda': cpi_all_rwanda}).reset_index(drop=True)

    long_format_data = cpi_data.melt(var_name='Region', value_name='CPI')

    fig = px.histogram(long_format_data, x='CPI', color='Region', barmode='overlay')

    fig.update_layout(
            title=None,
            xaxis_title='CPI',
            yaxis_title='Count',
            xaxis={'showgrid': True},
            yaxis={'showgrid': True},
            font=dict(size=12),
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
            margin=dict(l=30, r=9, t=30, b=25)
        )
    return fig


# call back for cpi monthly, cpi monthly change and cpi histogram
@callback(
    [Output('combined-cpi-graph', 'figure'),
     Output('cpi-year-title', 'children'),
     Output('graph3-info-footer', 'children')],
    [Input('year-dropdown', 'value'),
     Input('graph-type-selection', 'value')]
)
def monthly__mnthlychange(selected_year, graph_type):
    note = html.Span([html.Sup("*", style={"color": "#284fa1"}), f"CPI values for {selected_year}"])
    fig = dash.no_update
    title = None

    if graph_type == 'cpi_monthly':
        title = "Monthly CPI"
        # Code to generate the 'CPI Monthly' plot for the selected year
        fig = CPI_Monthly(selected_year)

    elif graph_type == 'cpi_monthly_change':
        title = "Monthly CPI Change in %"
        # Code to generate the 'CPI Monthly Change' plot for the selected year
        fig = CPI_monthly_change(selected_year)

    elif graph_type == 'cpi_histogram':
        title = "Histogram - CPI"
        # Code to generate the 'CPI Histogram' for the selected year
        fig = CPI_histogram(selected_year)

    return fig, title, note


# Callback to update the bar chart based on the selected region
@callback(
    Output('cpi-bar-chart', 'figure'),
    [Input('cpi-region-selector-dropdown', 'value')]
)
def update_cpi_chart(selected_region):
    sheet_data = data[selected_region].iloc[1:]
    sheet_data['Date'] = pd.to_datetime(sheet_data['Date'])
    sheet_data['Year'] = sheet_data['Date'].dt.year
    sheet_data['MonthName'] = sheet_data['Date'].dt.strftime('%b')
    sheet_data['CPI'] = sheet_data.iloc[:, 1]
    sheet_data.sort_values(by='Date', inplace=True)
    pivot_data = sheet_data.pivot_table(index='Year', columns='MonthName', values='CPI', aggfunc='mean')
    pivot_data.reset_index(inplace=True)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pivot_data = pivot_data.reindex(columns=['Year'] + month_order)
    fig = px.bar(pivot_data, x='Year', y=month_order, barmode='group')

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="CPI",
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        margin=dict(l=30, r=9, t=30, b=25)
    )
    return fig


@callback(
    [Output("graph1-ai-ouput", "children"),
     Output("graph1-ai-loading", "children")],
    [
        Input("graph1-explain-btn", "n_clicks"),
        State('plot-selection', 'value'),
    ]
)
def graph1_explain(btn, val):
    # Compute yearly averages
    urban_avg = compute_yearly_average(data, "Urban")
    rural_avg = compute_yearly_average(data, "Rural")
    all_rwanda_avg = compute_yearly_average(data, "All Rwanda")

    data_dict = pd.DataFrame({
        "Years": urban_avg.index,
        "GENERAL INDEX (CPI) - Urban": urban_avg['GENERAL INDEX (CPI)'],
        "GENERAL INDEX (CPI) - Rural": rural_avg['GENERAL INDEX (CPI)'],
        "GENERAL INDEX (CPI) - All Rwanda": all_rwanda_avg['GENERAL INDEX (CPI)'],
    })
    if btn is not None:
        if val == 1:
            return chat_with_csv(data_dict, "line"), ""
        else:
            return chat_with_csv(data_dict, "line"), ""
    return dash.no_update, dash.no_update
