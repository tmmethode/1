from dash import html, dcc   # type: ignore
import dash_bootstrap_components as dbc   # type: ignore


CONFIG = {
    # 'scrollZoom': False,
    # 'editable': False,
    # 'showLink': False,
    'displaylogo': False,
}


# Create a card for figure
def create_card(title, right_header_composent, fig, graph_id):
    card = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col(title),
                dbc.Col(right_header_composent)
                ])], style={"color": "white", 'font-size': 15}
        ),
        dbc.CardBody(
            [
                html.Div([
                  dcc.Graph(fig, id=graph_id, config=CONFIG)
                ])
            ], style={"padding": "0"},
        ),
    ], color="#284fa1", outline=False)
    return card
