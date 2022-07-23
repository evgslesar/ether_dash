import json
import pandas as pd
import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

with open("ether_data.json") as f:
    all_data = json.load(f)

row_df = pd.json_normalize(all_data)

df = row_df[["date", "name", "symbol",
             "market_data.current_price.usd",
             "market_data.current_price.btc",
             "market_data.market_cap.usd",
             "market_data.market_cap.btc",
             "market_data.market_cap.eth",
             "market_data.total_volume.usd",
             "market_data.total_volume.btc",
             "market_data.total_volume.eth",
             "public_interest_stats.alexa_rank"
             ]]
df = df.rename(columns={"market_data.current_price.usd": "Price USD",
                        "market_data.current_price.btc": "Price BTC",
                        "market_data.market_cap.usd": "Cap USD",
                        "market_data.market_cap.btc": "Cap BTC",
                        "market_data.market_cap.eth": "Cap ETH",
                        "market_data.total_volume.usd": "Volume USD",
                        "market_data.total_volume.btc": "Volume BTC",
                        "market_data.total_volume.eth": "Volume ETH",
                        "public_interest_stats.alexa_rank": "Alexa Rank"
                        })

app = dash.Dash(__name__)
app.title = "ETH Historical Data"

app.layout = html.Div([
    dcc.Tabs(id="ether-graphs", value="tab-1-graph", children=[
        dcc.Tab(label="ETH/USD", value="tab-1-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="ETH/BTC", value="tab-2-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="Cap USD", value="tab-3-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="Cap BTC", value="tab-4-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="Cap ETH", value="tab-5-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="Volume USD", value="tab-6-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="Volume BTC", value="tab-7-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="Volume ETH", value="tab-8-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
        dcc.Tab(label="Alexa Rank", value="tab-9-graph", 
            selected_style={"padding": "5px"}, 
            style={"padding": "5px"}),
    ], style={"height": "36px"}),
    html.Div(id="ether-datatable-container", style={"margin-top": "20px"}),
    dash_table.DataTable(
        id="ether-datatable",
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
        ],
        data=df.to_dict("records"),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"},
        style_header={"backgroundColor": "#8e8e8e", "color": "white", "textAlign": "center"},
        style_data={"backgroundColor": "#f0f0f0",},
        style_filter={"backgroundColor": "#d5d5d5"}
    )
], style={"margin-left": "80px", "margin-right": "80px"})


@app.callback(
    Output("ether-datatable", "style_data_conditional"),
    Input("ether-datatable", "selected_columns"))
def update_styles(selected_columns):
    return [{"column_id": i} for i in selected_columns]


@app.callback(Output("ether-datatable-container", "children"),
              Input("ether-graphs", "value"),
              Input("ether-datatable", "derived_virtual_data"))
def update_graphs(tab, rows):
    dff = df if rows is None else pd.DataFrame(rows)
    graphs = [
        html.Div(dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["date"],
                        "y": dff[column],
                        "type": "line",
                        "marker": {"color": "lightblue"},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True,
                              "autorange": "reversed"},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 400,
                    "margin": {"t": 10, "l": 0, "r": 0},
                    "padding": {"t": 0, "l": 5, "r": 5},
                },
            },
        ), style={"margin-top": "20px", "margin-bottom": "20px"})

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
        return html.Div([
            html.H3("ETH/USD"),
            graphs[0]
        ])
    elif tab == "tab-2-graph":
        return html.Div([
            html.H3("ETH/BTC"),
            graphs[1]
        ])
    elif tab == "tab-3-graph":
        return html.Div([
            html.H3("Cap USD"),
            graphs[2]
        ])
    elif tab == "tab-4-graph":
        return html.Div([
            html.H3("Cap BTC"),
            graphs[3]
        ])
    elif tab == "tab-5-graph":
        return html.Div([
            html.H3("Cap ETH"),
            graphs[4]
        ])
    elif tab == "tab-6-graph":
        return html.Div([
            html.H3("Volume USD"),
            graphs[5]
        ])
    elif tab == "tab-7-graph":
        return html.Div([
            html.H3("Volume BTC"),
            graphs[6]
        ])
    elif tab == "tab-8-graph":
        return html.Div([
            html.H3("Volume ETH"),
            graphs[7]
        ])
    elif tab == "tab-9-graph":
        return html.Div([
            html.H3("Alexa Rank"),
            graphs[-1]
        ])


if __name__ == "__main__":
    app.run_server(debug=True)
