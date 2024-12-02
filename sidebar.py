from dash import html   # type: ignore
import dash_bootstrap_components as dbc   # type: ignore


# Function to create the sidebar
def sidebar():
    return html.Ul([
        html.H2([html.Img(className="aims_logo", src="assets/nisr_logo.png", style={'width': '150px'}),
                 html.Span("Dashboard", id="sidebar-text-Dashboard")],
                className="display-8 row d-flex justify-content-center align-items-center"),
        html.Hr(),
        html.P([
            html.I(className="fa fa-home fa-lg"),
            dbc.Label("Home", style={'padding-left': '0.5rem'}, id="sidebar-text-Home")
            ], style={"color": "#284fa1"}),
        dbc.Nav(
            [
                dbc.NavLink([html.Span("Overview", id="sidebar-text-Overview")],
                            href="/home",
                            style={'color': "#696969"},
                            className="nav-link nav-home-link"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.P([
            html.I(className="fa fa-file-excel fa-lg"),
            dbc.Label("Datasets", style={'padding-left': '0.5rem'}, id="sidebar-text-Components")
            ], style={"color": "#284fa1"}),
        dbc.Nav(
            [
                dbc.NavLink(html.Span("GDP National Accounts", id="sidebar-text-GDP"),
                            href="/gdp",
                            style={'color': "#696969"},
                            className="nav-link nav-home-link",
                            id="GDP"),
                dbc.NavLink([html.Span("Consumer Price Index", id="sidebar-text-CPI")],
                            href="/cpi",
                            style={'color': "#696969"},
                            className="nav-link nav-home-link",
                            id="CPI"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.P([
            html.I(className="fa fa-question-circle fa-lg"),
            dbc.Label("AI Assistant", style={'padding-left': '0.5rem'}, id="sidebar-text-machine")
            ], style={"color": "#284fa1"}),
        dbc.Nav(
            [
                dbc.NavLink(html.Span("Chat with the data", id="sidebar-text-chat"),
                            href="/chat",
                            style={'color': "#696969"},
                            className="nav-link nav-home-link",
                            id="LLM"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        # html.P([
        #     html.I(className="fa fa-table fa-lg"),
        #     dbc.Label("Data", style={'padding-left': '0.5rem'}, id="sidebar-text-data")
        #     ], style={"color": "#284fa1"}),
        # dbc.Nav(
        #     [
        #         dbc.NavLink(html.Span("View", id="sidebar-text-view"),
        #                     href="/view",
        #                     style={'color': "#696969"},
        #                     className="nav-link nav-home-link",
        #                     id="View-Data"),
        #         dbc.NavLink(html.Span("Pivot Table", id="sidebar-text-pivot"),
        #                     href="/pivottable",
        #                     style={'color': "#696969"},
        #                     className="nav-link nav-home-link",
        #                     id="Pivot-Table"),
        #     ],
        #     vertical=True,
        #     pills=True,
        # ),
    ], className="navbar-nav sidebar sidebar-dark accordion w-100", id="accordionSidebar", style={'padding': '1rem', "position": "fixed"})  # noqa
