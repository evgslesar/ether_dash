import sqlite3
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

conn = sqlite3.connect("ether_data.db")
df = pd.read_sql('''SELECT date as 'Date', name as 'Name',
             "market_data.current_price.usd" as 'Price USD',
             "market_data.current_price.btc" as 'Price BTC',
             "market_data.market_cap.usd" as 'Cap USD',
             "market_data.market_cap.btc" as 'Cap BTC',
             "market_data.market_cap.eth" as 'Cap ETH',
             "market_data.total_volume.usd" as 'Volume USD',
             "market_data.total_volume.btc" as 'Volume BTC',
             "market_data.total_volume.eth" as 'Volume ETH',
             "public_interest_stats.alexa_rank" as 'Alexa Rank'
             FROM ether_data''', conn, index_col=None)
conn.close()

df = df.iloc[::-1]

df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.date

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.FLATLY])
app.title = "ETH Historical Data"

app.layout = dbc.Container([
    dbc.Tabs(id="ether-graphs", active_tab="tab-1-graph", children=[
        dbc.Tab(label="ETH/USD", tab_id="tab-1-graph"),
        dbc.Tab(label="ETH/BTC", tab_id="tab-2-graph"),
        dbc.Tab(label="Cap USD", tab_id="tab-3-graph"),
        dbc.Tab(label="Cap BTC", tab_id="tab-4-graph"),
        dbc.Tab(label="Cap ETH", tab_id="tab-5-graph"),
        dbc.Tab(label="Volume USD", tab_id="tab-6-graph"),
        dbc.Tab(label="Volume BTC", tab_id="tab-7-graph"),
        dbc.Tab(label="Volume ETH", tab_id="tab-8-graph"),
        dbc.Tab(label="Alexa Rank", tab_id="tab-9-graph"),
    ]),
    dbc.Row(id="ether-datatable-container", style={"margin-top": "10px"}),
    dbc.Row(dash_table.DataTable(
        id="ether-datatable",
        columns=[
            {"name": i, "id": i} for i in df.columns
        ],
        data=df.to_dict("records"),
        fixed_rows = {"headers":True},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell = {
            "textAlign":"center",
            "fontFamily":"Arial",
            "border":"4px solid white",
            "maxWidth" :"50px",
            "textOverflow": "ellipsis",
        },
        style_header = {
            "color": "white",
            "backgroundColor":"rgb(125,125,125)",
            "fontWeight":"bold",
            "border":"4px solid white",
            "fontSize":"12px"
        },
        style_data_conditional = [
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "rgb(240,240,240)",
            },            
            {
                "if": {"row_index": "even"},
                "backgroundColor": "rgb(255, 255, 255)",     
            }
        ],
        style_data={"fontSize":"12px"},
        style_filter={"backgroundColor": "rgb(220,220,220)"}
    ))
])

@app.callback(Output("ether-datatable-container", "children"),
              Input("ether-graphs", "active_tab"),
              Input("ether-datatable", "derived_virtual_data"))
def update_graphs(tab, rows):
    dff = df if rows is None else pd.DataFrame(rows)
    graphs = [
        dbc.Row(dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["Date"],
                        "y": dff[column],
                        "type": "line",
                        "marker": {"color": "rgb(108,195,175)"},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 400,
                    "margin": {"t": 10, "l": 0, "r": 0},
                    "padding": {"t": 0, "l": 3, "r": 3},
                },
            },
        ), style={"margin-top": "10px", "margin-bottom": "10px"})

        for column in ["Price USD",
                       "Price BTC",
                       "Cap USD",
                       "Cap BTC",
                       "Cap ETH",
                       "Volume USD",
                       "Volume BTC",
                       "Volume ETH",
                       "Alexa Rank",
                       ] if column in dff
    ]
    if tab == "tab-1-graph":
        return dbc.Row([
            html.H4("ETH/USD"),
            graphs[0]
        ])
    elif tab == "tab-2-graph":
        return dbc.Row([
            html.H4("ETH/BTC"),
            graphs[1]
        ])
    elif tab == "tab-3-graph":
        return dbc.Row([
            html.H4("Cap USD"),
            graphs[2]
        ])
    elif tab == "tab-4-graph":
        return dbc.Row([
            html.H4("Cap BTC"),
            graphs[3]
        ])
    elif tab == "tab-5-graph":
        return dbc.Row([
            html.H4("Cap ETH"),
            graphs[4]
        ])
    elif tab == "tab-6-graph":
        return dbc.Row([
            html.H4("Volume USD"),
            graphs[5]
        ])
    elif tab == "tab-7-graph":
        return dbc.Row([
            html.H4("Volume BTC"),
            graphs[6]
        ])
    elif tab == "tab-8-graph":
        return dbc.Row([
            html.H4("Volume ETH"),
            graphs[7]
        ])
    elif tab == "tab-9-graph":
        return dbc.Row([
            html.H3("Alexa Rank"),
            graphs[-1]
        ])


if __name__ == "__main__":
    app.run_server(debug=True)
