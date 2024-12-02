import dash  # type: ignore
from dash import html, callback, Input, Output, dcc, State  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
from config import CONFIG
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from data import GDP_EXCEL_FILE
from datetime import date
from llm import chat_with_csv, qa_csv


dash.register_page(__name__)


def get_proportions_of_gdp_by_sectors():
    years = list(GDP_EXCEL_FILE['Years'].values)
    years.append('All')
    dropdown_years = dcc.Dropdown(
                    id='gdp-by-sectors-year-dropdown',
                    options=[
                            {
                                "label": html.Span(year, style={'color': 'black', 'font-size': 16}),
                                "value": year,
                            } for year in years
                    ],
                    value=2022,
                    clearable=False,
                ),
    # "Proportion of GDP by Sectors",
    content = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("Proportion of GDP by Sectors", className="figCard"),
                dbc.Col(dropdown_years)
                ])], className="figTitle"
        ),
        dbc.CardBody(
            [
                html.Div([
                  dcc.Graph(id='donut-gdp-by-sector-fig', config=CONFIG)
                ])
            ], style={"padding": "0"},
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "black"}), "Contribution of each sector on GDP"]),
                        id="proportions_of_gdp-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="proportions_of_gdp-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="proportions_of_gdp-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="proportions_of_gdp-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True, id="proportions_of_gdp-collapse"
                )
            )
        ], ),
    ], outline=False, style={'padding': 0})

    return content


# price and growth rate selector for gdp
gdp_current_price_inline_radioitems = dbc.RadioItems(
    options=[
        {"label": html.Span(["Price", html.Sup(1, style={"color": "red"})]), "value": 1},
        {"label": "Growth Rate", "value": 2},
    ],
    value=1,
    id="gdp-radioitems-inline-input",
    inline=True,
)


date_range_picker = dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=date(1999, 1, 1),
        max_date_allowed=date(2024, 1, 1),
        initial_visible_month=date(2005, 1, 1),
        start_date=date(2005, 1, 1),
        end_date=date(2023, 12, 31)
    )

explain_card = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.Div("Here is the output of AI engine.", id="ai-explain-ouput"),
                ],
                title="AI Output",
            ),
        ], id="ai-explain-btn", start_collapsed=True,
    )
)


form = html.Div(
    dbc.Row(
        [
            dbc.Row(
                dbc.Input(type="text", placeholder="Ask me something about the GDP...", id="input-chat"),
                className="mb-3"
            ),
            html.Div([dbc.Button(
                        [dbc.Spinner(html.Span(id="ai-loading"), size="sm"), " Submit"],
                        color="primary",
                        id="chat-btn"
                    ),
            ]),
        ],
    )
)

# the main gdp card
gdp_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("Gross Domestic Product", className="figCard", id="gdp-title"),
                dbc.Col(
                    gdp_current_price_inline_radioitems, className="d-flex justify-content-end",
                )
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='gdp-figure', config=CONFIG)
                ])
            ], style={"padding": "0"},
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col("", id="gdp-info-footer"),
            ], className="mb-2"),
            html.Hr(),
            dbc.Row([dbc.Col(form), dbc.Col(explain_card)]),
        ], ),
    ], outline=False)

# gdp control panel card
gdp_panel_control_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("GDP Panel Control", className="figCard"),
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    html.H6("GDP Types", className="h6 text-gray-600", style={"border-bottom": 2}),
                    dbc.RadioItems(
                        options=[
                            {"label": "Current Prices", "value": "GDP at current prices"},
                            {"label": "Constant 2017 Prices", "value": "GDP at constant 2017 prices"},
                            {"label": "Implicit GDP Deflator", "value": "Implicit GDP deflator"},
                            {"label": "All", "value": "All"},
                        ],
                        value="GDP at current prices",
                        id="gdp-type",
                        inline=False,
                    ),
                    html.Hr(),
                    html.H6("Chart Types", className="h6 text-gray-600", style={"border-bottom": 2}),
                    html.Div([
                        dcc.Dropdown(
                            id='gdp-chart-type-dropdown',
                            options=[
                                    {
                                        "label": html.Span("Bullet", style={'color': 'black', 'font-size': 16}),
                                        "value": "bullet",
                                    },
                                    {
                                        "label": html.Span("Bar Chart", style={'color': 'black', 'font-size': 16}),
                                        "value": "bar",
                                    },
                                    {
                                        "label": html.Span("Line Chart", style={'color': 'black', 'font-size': 16}),
                                        "value": "line",
                                    },
                            ],
                            value="bullet",
                            clearable=False,
                         ),
                    ]),
                ])
            ],
        ),
    ], outline=False, style={'padding': 0})


# date picker card
date_picker_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("Date Range", className="figCard"),
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    html.H6("Pick a date range", className="h6 text-gray-600"),
                    html.Hr(),
                    date_range_picker
                ])
            ],
        ),
        dbc.CardFooter([
            dbc.Row([
                "Note: This date range is used for all figures in this page."
            ], className="mb-2"),
        ], ),
    ], outline=False, style={'padding': 0}, className="mt-3")


# exchange rate card
exchange_rate_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("Exchange Rate Over Time", className="figCard"),
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='exchange-figure', config=CONFIG)
                ])
            ], style={"padding": "0"}
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "orange"}), "Exchange rate: Rwf per US dollar"]),
                        id="exhange-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="exchange-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="exchange-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="exchange-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True,
                )
            )
        ], ),
    ], outline=False, style={'padding': 0})

population_rate_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("Population Over Time", className="figCard", width=7),
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='population-figure', config=CONFIG)
                ])
            ], style={"padding": "0"}
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "green"}), "Population (in millions)"]),
                        id="exhange-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="population-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="population-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="population-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True, id="population-collapse"
                )
            )
        ], ),
    ], outline=False, style={'padding': 0})


gdp_per_capita_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("GDP Per Capita Metrics", className="figCard", width=7),
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='gdp_per_capita-figure', config=CONFIG)
                ])
            ], style={"padding": "0"}
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "orange"}), "Population (in millions)"]),
                        id="gdp_per_capita-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="gdp_per_capita-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="gdp_per_capita-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="gdp_per_capita-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True, id="gdp_per_capita-collapse"
                )
            )
        ], )
    ], outline=False, style={'padding': 0})


national_income_expenditure_card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("National Income and Expenditure", className="figCard", width=6),
            ])
        ], className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='national_income_expenditure-figure', config=CONFIG)
                ])
            ], style={"padding": "0"}
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "orange"}), "In RWF billion"]),
                        id="national_income_expenditure-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="national_income_expenditure-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="national_income_expenditure-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="national_income_expenditure-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True, id="national_income_expenditure-collapse"
                )
            )
        ], ),
    ], outline=False, style={'padding': 0})


# Expenditure
expenditure = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col("Expenditure on GDP", className="figCard"),
                dbc.Col(
                    # year selection
                    dcc.Dropdown(
                        id='expenditure-gdp-dropdown',
                        options=[
                            {
                                "label": html.Span("GDP at current prices", style={'color': 'black'}),
                                "value": 1,
                            },
                            {
                                "label": html.Span("GDP at constant 2017 prices", style={'color': 'black'}),
                                "value": 2,
                            },
                        ],
                        value=1,
                        clearable=False
                    ),
                )
            ]
            )
        ], style={"color": "white", 'font-size': 16}, className="figTitle"),
        dbc.CardBody(
            [
                html.Div([
                    dcc.Graph(id='expenditure_fig', config=CONFIG)
                ])
            ], style={"padding": "0"},
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col(html.Span([html.Sup("*", style={"color": "orange"}), "In RWF billion"]),
                        id="expenditure-info-footer", width=6),
                dbc.Col(dbc.Button(
                        [dbc.Spinner(html.Span(id="expenditure-ai-loading"), size="sm"), " Summarize"],
                        color="primary",
                        id="expenditure-explain-btn"
                        ), width=6, className="d-flex justify-content-end")
            ], className="mb-2"),
            html.Hr(),
            dbc.Row(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Div("Here is the output of AI engine.", id="expenditure-ai-ouput"),
                            ],
                            title="AI Output",
                        ),
                    ], start_collapsed=True, id="expenditure-collapse"
                )
            )
        ], ),
    ], outline=False)


# Render the dgp content
def layout():
    return [html.Div([
        html.Div(
            html.H1("Dashboard > GDP National Accounts", className="h5 mb-0 text-gray-800"),
            className="d-sm-flex align-items-center justify-content-between mb-4",
        ),
        dbc.Row([
            dbc.Col([
                gdp_card
            ], width=9),
            dbc.Col([
                gdp_panel_control_card,
                date_picker_card
            ], width=3, style={'margin': 0}),
        ], className="mb-3"),
        dbc.Row(
            [
                dbc.Col(exchange_rate_card, width=6),
                dbc.Col(population_rate_card, width=6)
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(get_proportions_of_gdp_by_sectors(), width=6),
                dbc.Col(expenditure, width=6)
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(gdp_per_capita_card, width=6),
                dbc.Col(national_income_expenditure_card, width=6)
            ],
            className="mb-3",
        ),
    ])
    ]


@callback(
    [Output("gdp-figure", "figure"),
     Output("gdp-title", "children"),
     Output("exchange-figure", "figure"),
     Output("gdp-info-footer", "children")],
    [Input("gdp-radioitems-inline-input", "value"),
     Input("gdp-chart-type-dropdown", "value"),
     Input("gdp-type", "value"),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")]
)
def gdp_on_change(val, chart, gdp, start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    exchange_fig = {
        'data': [
            {
                'x': data['Years'].values,
                'y': data["Exchange rate: Rwf per US dollar"].values,
                'type': 'line',
                'name': '',
                'line': {'color': 'orange'},  # Set the color you prefer
                'hovertemplate': '%{x}: 1 USD = %{y} RWF',
            },
            ],
        'layout': {
            'title': '',
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
            'xaxis': {
                'title': '',
                'tickmode': 'array',  # Set tickmode to 'array'
                'tickvals': data['Years'].values,  # Provide all years as tickvals
            },
            'yaxis': {
                'title': '',
                'range': [400, data["Exchange rate: Rwf per US dollar"].max() + 100],  # Set y-axis range
                'tick0': 400,  # Set the starting tick
                'dtick': 100,  # Set the tick spacing
            },
            'margin': {'l': 30, 'r': 9, 't': 30, 'b': 25},  # margin
        }
    }

    fig = {
        "data": None,
        'layout': {
                'title': '',
                'paper_bgcolor': 'rgb(243, 243, 243)',
                'plot_bgcolor': 'rgb(243, 243, 243)',
                'legend': {'x': 0, 'y': 1},  # Legend position
                'margin': {'l': 30, 'r': 9, 't': 30, 'b': 25},  # margin
            }
    }
    if gdp == "All":
        if val == 2:
            fig['data'] = [
                    {
                        'x': data['Years'],
                        'y': data['GDP at current prices'], 'type': 'scatter', 'name': 'Current prices',
                        'line': {'dash': 'solid'},
                        'hovertemplate': '%{x}: GDP = %{y} RWF Billion',
                    },
                    {
                        'x': data['Years'],
                        'y': data['GDP at constant 2017 prices'], 'type': 'line', 'name': 'Constant 2017 prices',
                        'line': {'dash': 'dash'},
                        'hovertemplate': '%{x}: GDP = %{y} RWF Billion',
                    },
                    {
                        'x': data['Years'],
                        'y': data['Implicit GDP deflator'], 'type': 'bar', 'name': 'Implicit Deflator',
                        'line': {'dash': 'dot'}, 'hovertemplate': '%{x}: GDP = %{y} RWF Billion'
                    },
                ]
        else:
            if chart == "line":
                fig['data'] = [
                        {
                            'x': data['Years'],
                            'y': data['GDP at current prices'], 'type': 'line', 'name': 'Current prices',
                            'line': {'dash': 'solid'},
                            'hovertemplate': '%{x}: GDP = %{y} RWF Billion',
                        },
                        {
                            'x': data['Years'],
                            'y': data['GDP at constant 2017 prices'], 'type': 'line', 'name': 'Constant 2017 prices',
                            'line': {'dash': 'dash'},
                            'hovertemplate': '%{x}: GDP = %{y} RWF Billion',
                        },
                    ]
            elif chart == "bar":
                fig = px.bar(data, y=[
                    'GDP at current prices',
                    'GDP at constant 2017 prices',
                ], x='Years', title='')

                fig.update_layout(
                    barmode='group',
                    xaxis_title=None,
                    yaxis_title=None,
                    paper_bgcolor='rgb(243, 243, 243)',
                    plot_bgcolor='rgb(243, 243, 243)',
                    margin=dict(l=30, r=9, t=30, b=25)
                )
        title = "GDP Comparison"
        info = html.Span([html.Sup(1, style={"color": "red"}), "GDP in RWF Billion"])
        return fig, title, exchange_fig, info

    if val == 1:
        if chart == "bullet":
            fig = px.scatter(data, x="Years", y=gdp, color=gdp, size=gdp, hover_data=[gdp])
        elif chart == "line":
            # Create the line plot with markers and text labels
            fig = px.line(data, x="Years", y=gdp, markers=True)

            # Customize the text labels
            fig.update_traces(marker=dict(size=10), textposition="top center")
        else:
            # Create the line plot with markers and text labels
            fig = px.bar(data, x="Years", y=gdp)
    else:
        # Calculate the growth rate as percentages and format them as strings
        data['Growth Rate'] = data[gdp].pct_change()
        data["Growth Rate (Percentage)"] = (data["Growth Rate"] * 100).round(1).astype(str) + '%'
        y = "Growth Rate"
        data = data.dropna()
        if chart == "bullet":
            y_size = [int(val+10) for val in data[y].values if val]
            fig = px.scatter(data, x="Years", y=y, color=y, size=y_size, hover_data=["Growth Rate (Percentage)"])
        elif chart == "line":
            # Create the line plot with markers and text labels
            fig = px.line(data, x="Years", y=y, markers=True, text="Growth Rate (Percentage)")

            # Customize the text labels
            fig.update_traces(marker=dict(size=10), textposition="top center")
        else:
            # Create the line plot with markers and text labels
            fig = px.bar(data, x="Years", y=y)

    # Increase the size of the figure
    # Remove the x-label and y-label
    fig.update_layout(xaxis_title=None,
                      yaxis_title=None,
                      margin_t=30,
                      margin_l=9,
                      margin_b=9,
                      margin_r=9,
                      xaxis={'type': 'category'},
                      paper_bgcolor='rgb(243, 243, 243)',
                      plot_bgcolor='rgb(243, 243, 243)',)

    title = f"Gross Domestic Product - {gdp}"
    info = ""
    if gdp != "Implicit GDP deflator":
        if val == 1:
            info = html.Span([html.Sup("*", style={"color": "red"}), f"{gdp} (in RWF Billion)"])
        else:
            info = html.Span([html.Sup("*", style={"color": "red"}), f"{gdp} (growth rate in %)"])
    else:
        if val == 1:
            info = html.Span([html.Sup("*", style={"color": "red"}), "Implicit GDP deflator (in RWF Billion)"])
        else:
            info = html.Span([html.Sup("*", style={"color": "red"}), "Implicit GDP deflator (growth rate in %)"])

    return fig, title, exchange_fig, info


@callback(
    Output("donut-gdp-by-sector-fig", "figure"),
    [
        Input("gdp-by-sectors-year-dropdown", "value"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date")
    ],
)
def gdp_by_sector_year_dropdown_on_change(radio_items_value, start_date, end_date):
    labels = ["Agriculture", "Industry", "Services", "Adjustments"]
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year

    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    data = data[["Years"] + labels]

    if radio_items_value != "All":
        data = data[data['Years'] == radio_items_value][labels]
        values = list(data.values[0])
        total = GDP_EXCEL_FILE[GDP_EXCEL_FILE['Years'] == radio_items_value]['GDP at current prices'].values[0]

        # Create a smaller pie chart (the "hole" in the donut)
        fig = px.pie(values=values, names=labels, hole=0.5)

        # Create a larger pie chart to overlay the smaller one (the outer "ring")
        fig2 = px.pie(values=[total], names=["GDP at current prices"], hole=0.9)
        # fig2.update_traces(marker=dict(color='white'))

        # Combine the two charts to create the donut chart
        fig.add_traces(fig2.data)
        # # Use `hole` to create a donut-like pie chart
        # fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
        fig.update_layout(annotations=[dict(text=f"{total} (RWF Billion)", font_size=15, showarrow=False,)],
                          legend={'x': 0, 'y': 4, 'orientation': 'h'})
        # Remove the x-label and y-label
        fig.update_layout(margin_t=30,
                          margin_l=7,
                          margin_b=7,
                          margin_r=0,
                          xaxis={'type': 'category'},
                          paper_bgcolor='rgb(243, 243, 243)',
                          plot_bgcolor='rgb(243, 243, 243)',)
    else:
        fig = px.bar(data, y=labels, x='Years', title='')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group',
                          legend={'x': 0, 'y': 4, 'orientation': 'h'})
        # Remove the x-label and y-label
        fig.update_layout(margin_t=30,
                          margin_l=9,
                          margin_b=9,
                          margin_r=9,
                          paper_bgcolor='rgb(243, 243, 243)',
                          plot_bgcolor='rgb(243, 243, 243)',)
    return fig


@callback(
    Output("expenditure_fig", "figure"),
    [Input("expenditure-gdp-dropdown", "value"),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")])
def update_expenditure_bar_chart(value, start_date, end_date):
    cols = ["Resource balance", "Gross capital formation", "Private (includes changes in stock)", "Government"]
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    years = list(data['Years'].values)

    if value == 1:
        # Create traces
        fig = go.Figure(data=[
            go.Bar(name=col, x=years,
                   y=list(data[col]*data['GDP at current prices'])) for col in cols
        ])
        fig.add_trace(go.Scatter(x=years, y=list(data['GDP at current prices']),
                                 mode='lines', name='GDP', marker_color='black'))
    else:
        # Create traces
        fig = go.Figure(data=[
            go.Bar(name=col, x=years,
                   y=list(data[col]*data['GDP at constant 2017 prices'])) for col in cols
        ])
        fig.add_trace(go.Scatter(x=years, y=list(data['GDP at constant 2017 prices']),
                                 mode='lines', name='GDP', marker_color='black'))

    fig.update_layout(barmode='relative',
                      legend={'x': 0, 'y': 4, 'orientation': 'h'},
                      xaxis={'type': 'category'},
                      margin_t=30,
                      margin_l=9,
                      margin_b=9,
                      margin_r=9,
                      paper_bgcolor='rgb(243, 243, 243)',
                      plot_bgcolor='rgb(243, 243, 243)',
                      )
    return fig


@callback(
    [Output("population-figure", "figure")],
    [Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")]
)
def population_on_change(start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    data["Population Growth Rate"] = data["Total population (millions)"].pct_change()
    data["Population Growth Rate"] = (data["Population Growth Rate"] * 100).round(1)

    population_fig = {
        'data': [
            {
                'x': data['Years'].values,
                'y': data["Total population (millions)"].values,
                'type': 'line',
                'name': '',
                'line': {'color': 'green'},  # Set the color
                'hovertemplate': '%{x}: Population = %{y}',
            },
            ],
        'layout': {
            'title': '',
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
            'xaxis': {
                'title': '',
                'tickmode': 'array',  # Set tickmode to 'array'
                'tickvals': data['Years'].values,  # Provide all years as tickvals
            },
            'yaxis': {
                'title': '',
            },
            'margin': {'l': 30, 'r': 9, 't': 30, 'b': 25},  # margin
        }
    }
    return [population_fig]


@callback(
    [Output("gdp_per_capita-figure", "figure")],
    [Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")]
)
def gdp_per_capita_on_change(start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]

    fig = {
        'data': [
            {
                'x': data['Years'],
                'y': data['GDP per head (in \'000 Rwf)'], 'type': 'line', 'name': 'GDP per head (in \'000 Rwf)',
                'line': {'dash': 'solid'},
                'hovertemplate': '%{x}: GDP Per Head = %{y} (in \'000 Rwf)',
            },
            {
                'x': data['Years'],
                'y': data['GDP per head (in current US dollars)'], 'type': 'line', 'name': 'GDP per head (in current US dollars)',  # noqa
                'line': {'dash': 'dash'},
                'hovertemplate': '%{x}: GDP Per Head = %{y} (in current US dollars)',
            },
        ],
        'layout': {
            'title': '',
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
            'legend': {'x': 0, 'y': 1},  # Adjust legend position
            'margin': {'l': 30, 'r': 9, 't': 30, 'b': 25},  # margin
        }
    }
    return [fig]


@callback(
    [Output("national_income_expenditure-figure", "figure")],
    [Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")]
)
def national_income_expenditure_on_change(start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year

    if start_date is None or end_date is None:
        return dash.no_update

    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]

    fig = {
        'data': [
            {
                'x': data['Years'],
                'y': data['Gross National Income'],
                'type': 'area',
                'name': 'Gross National Income',
                'marker': {'color': 'green'},  # Set the color
            },
            {
                'x': data['Years'],
                'y': data['Current transfers, net'],
                'type': 'area',
                'name': 'Current transfers, net',
                'marker': {'color': 'blue'},  # Set the color
            },
            {
                'x': data['Years'],
                'y': data['Gross National Disposible Income'],
                'type': 'area',
                'name': 'Gross National Disposable Income',
                'marker': {'color': 'orange'},  # Set the color
            },
        ],
        'layout': {
            'title': '',
            'paper_bgcolor': 'rgb(243, 243, 243)',
            'plot_bgcolor': 'rgb(243, 243, 243)',
            'legend': {'x': 0, 'y': 1},
            'margin': {'l': 30, 'r': 9, 't': 30, 'b': 25},
        }
    }
    fig = px.area(data, x='Years', y=[
        'Gross Domestic Product at current prices',
        'Factor income from abroad, net',
        'Gross National Income',
        'Current transfers, net',
        'Gross National Disposible Income',
        'Less Final consumption expenditure',
        'Gross National Saving',
        'Less Gross capital formation',
        'Net lending to the rest of the world'
    ], title='')
    fig.update_layout(
        xaxis_title='Years',
        yaxis_title='Amount',
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        legend=dict(x=0, y=1),
        margin=dict(l=30, r=9, t=30, b=25)
    )

    fig = px.bar(data, y=[
        'Net lending to the rest of the world',
        'Gross Domestic Product at current prices',
        'Factor income from abroad, net',
        'Gross National Income',
        'Current transfers, net',
        'Gross National Disposible Income',
        'Less Final consumption expenditure',
        'Gross National Saving',
        'Less Gross capital formation'
    ], x='Years', title='')

    fig.update_layout(
        barmode='relative',
        xaxis_title=None,
        yaxis_title=None,
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        margin=dict(l=30, r=9, t=30, b=25)
    )

    return [fig]


@callback(
    [Output("ai-explain-ouput", "children"), Output("ai-loading", "children")],
    [
        Input("chat-btn", "n_clicks"),
        State("input-chat", "value"),
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
        State("gdp-radioitems-inline-input", "value"),
        State("gdp-chart-type-dropdown", "value"),
        State("gdp-type", "value")
    ]
)
def gdp_figure_chat(btn, input_text, start_date, end_date, gdp_value, chart, gdp):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    if gdp != "All":
        data = data[["Years", gdp]]
    else:
        data = data[["Years", "GDP at current prices", "GDP at constant 2017 prices"]]
    # query = f"The figure chart type is {chart} and the GDP value is {gdp_value} \n. Answer the following prompt: {input_text}"

    if input_text is None:
        return dash.no_update, dash.no_update
    return [qa_csv(data, input_text)], ""


@callback(
    [Output("exchange-ai-ouput", "children"), Output("exchange-ai-loading", "children")],
    [
        Input("exchange-explain-btn", "n_clicks"),
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
    ]
)
def exchange_rate_explain(btn, start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]

    if btn is not None:
        return chat_with_csv(data[["Years", "Exchange rate: Rwf per US dollar"]], "line"), ""
    return dash.no_update, dash.no_update


@callback(
    [Output("population-ai-ouput", "children"),
     Output("population-ai-loading", "children"),
     Output("population-collapse", "start_collapsed")],
    [
        Input("population-explain-btn", "n_clicks"),
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
    ]
)
def population_rate_explain(btn, start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    data = data[["Years", "Total population (millions)"]]

    if btn is not None:
        return chat_with_csv(data, "line"), "", False
    return dash.no_update, dash.no_update, dash.no_update


@callback(
    [Output("proportions_of_gdp-ai-ouput", "children"),
     Output("proportions_of_gdp-ai-loading", "children"),
     Output("proportions_of_gdp-collapse", "start_collapsed")],
    [
        Input("proportions_of_gdp-explain-btn", "n_clicks"),
        State("gdp-by-sectors-year-dropdown", "value"),
    ]
)
def proportions_of_gdp_rate_explain(btn, selected_date):
    labels = ["Years", "Agriculture", "Industry", "Services", "Adjustments", "GDP at current prices"]

    if btn is not None:
        if selected_date != "All":
            data = GDP_EXCEL_FILE[GDP_EXCEL_FILE["Years"] == selected_date][labels]
            return chat_with_csv(data, "pie chart to see the contribution of each sector on GDP at current prices"), "", False
        else:
            return chat_with_csv(GDP_EXCEL_FILE[labels],
                                 "grouped bar chart to see the contribution of each sector on GDP at current prices"), "", False
    return dash.no_update, dash.no_update, dash.no_update


@callback(
    [Output("national_income_expenditure-ai-ouput", "children"),
     Output("national_income_expenditure-ai-loading", "children"),
     Output("national_income_expenditure-collapse", "start_collapsed")],
    [
        Input("national_income_expenditure-explain-btn", "n_clicks"),
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
    ]
)
def national_income_expenditure_explain(btn, start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    cols = [
        "Years",
        'Gross Domestic Product at current prices',
        'Factor income from abroad, net',
        'Gross National Income',
        'Current transfers, net',
        'Gross National Disposible Income',
        'Less Final consumption expenditure',
        'Gross National Saving',
        'Less Gross capital formation',
        'Net lending to the rest of the world'
    ]
    chart_type = "stacked bar plot to see the contribution of each columns on National Income and Expenditure (in billion RWF)"
    if btn is not None:
        return chat_with_csv(data[cols], chart_type), "", False
    return dash.no_update, dash.no_update, dash.no_update


@callback(
    [Output("expenditure-ai-ouput", "children"),
     Output("expenditure-ai-loading", "children"),
     Output("expenditure-collapse", "start_collapsed")],
    [
        Input("expenditure-explain-btn", "n_clicks"),
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
    ]
)
def expenditure_explain(btn, start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    cols = ["Resource balance", "Gross capital formation", "Private (includes changes in stock)", "Government"]
    data = data[["Years"] + cols]
    if btn is not None:
        return chat_with_csv(data, "stacked bar plot to see the contribution of each sector on GDP"), "", False
    return dash.no_update, dash.no_update, dash.no_update


@callback(
    [Output("gdp_per_capita-ai-ouput", "children"),
     Output("gdp_per_capita-ai-loading", "children"),
     Output("gdp_per_capita-collapse", "start_collapsed")],
    [
        Input("gdp_per_capita-explain-btn", "n_clicks"),
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
    ]
)
def gdp_per_capita_explain(btn, start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    start_date = start_date_object.year
    end_date = end_date_object.year
    data = GDP_EXCEL_FILE[(GDP_EXCEL_FILE["Years"] >= start_date) & (GDP_EXCEL_FILE["Years"] <= end_date)]
    cols = ["GDP per head (in \'000 Rwf)", "GDP per head (in current US dollars)"]
    data = data[["Years"] + cols]
    if btn is not None:
        return chat_with_csv(data, "line chart of both in the same figure"), "", False
    return dash.no_update, dash.no_update, dash.no_update
