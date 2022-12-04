import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px

from graphing import counties, claims_by_year, agg_total

from modeling import df #lrr, df, fb, col_map
from modeling import dfTrain, dfTest,  yTrain, yTest #dfTrainStd, dfTestStd,


def Header(name, app):
    title = html.H2(name, style={"margin-top": 5})
    # logo = html.Img(
    #     src=app.get_asset_url("dash-logo.png"), style={"float": "right", "height": 50}
    # )

    return dbc.Row([dbc.Col(title, md=12)]) #, dbc.Col(logo, md=3)])


# def LabeledSelect(label, **kwargs):
#     return dbc.FormGroup([dbc.Label(label), dbc.Select(**kwargs)])


# Compute the explanation dataframe, GAM, and scores
# xdf = lrr.explain().rename(columns={"rule/numerical feature": "rule"})
# xPlot, yPlot, plotLine = compute_plot_gam(lrr, df, fb, df.columns)
train_acc = 0.91   #accuracy_score(yTrain, lrr.predict(dfTrain, dfTrainStd))
test_acc = 0.88    #accuracy_score(yTest, lrr.predict(dfTest, dfTestStd))


# Start the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Card components
cards = [
    dbc.Card(
        [
            html.H2(f"{train_acc*100:.2f}%", className="card-title"),
            html.P("Model Training Accuracy", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H2(f"{test_acc*100:.2f}%", className="card-title"),
            html.P("Model Test Accuracy", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2(f"{dfTrain.shape[0]} / {dfTest.shape[0]}", className="card-title"),
            html.P("Train / Test Split", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
]

# Graph components
# graphs = [
#     [
#         LabeledSelect(
#             id="select-coef",
#             options='test',
#             value=1,
#             label="Filter Features",
#         ),
#         dcc.Graph(id="graph-coef"),
#     ],
#     [
#         LabeledSelect(
#             id="select-gam",
#             options='testing',
#             value=3,
#             label="Visualize GAM",
#         ),
#         dcc.Graph("graph-gam"),
#     ],
# ]

# Graphs
claims_state = px.histogram(
    df,
    x="state",
    #y="total_claim",
    #color="condition",
    #title="Number of Claims by State",
).update_xaxes(categoryorder="total descending")
claims_state.update_layout(
    title={'text': 'Number of Claims by State','y':0.93,'x':0.5,'xanchor': 'center','yanchor':'top'},
    xaxis_title='State',
    yaxis_title='Number of Claims',
)
# claim_year = px.bar(
#     claims_by_year,
#     x='yearOfLoss',
#     y='total_claims',
#     title='Amount of Property Damage by Year'
# )
claim_year = px.bar(
    claims_by_year,
    x='yearOfLoss',
    y='total_claims',
    #title='',
    #text_auto=True,
    text_auto='.2s',
    #text='yearOfLoss'
)
claim_year.update_traces(textfont_size=20, textangle=0, cliponaxis=False)
claim_year.update_layout(
    title={'text': 'Property Damage by Year (in $)','y':0.93,'x':0.5,'xanchor': 'center','yanchor':'top'},
    xaxis_title='Year of Damage',
    yaxis_title='Claim Amount Paid ($)',
)
map = px.choropleth(agg_total, geojson=counties, locations='countyCode', color='log_total_claims',
                           color_continuous_scale="Viridis",
                           #range_color=(0, 12),
                           scope="usa",
                           labels={'log_total_claims':'Total Amount Claims'}
                          )
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



# map = px.choropleth(df, geojson=counties, locations='countyCode', color='total_claims',
#                     color_continuous_scale="Viridis",
#                     range_color=(0, 12),
#                     scope="usa",
#                     #labels={'unemp':'unemployment rate'}
#         )
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#  = px.histogram(
#     df,
#     x="state",
#     #y="total_claim",
#     #color="condition",
#     title="Total Claims ($) by State",
# )

app.layout = dbc.Container(
    [
        Header("Flood Insurance – Minimizing Opportunity Costs", app),
        html.Hr(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        #dbc.Row([dbc.Col(graph) for graph in graphs]),
        dbc.Row(
            [
            dbc.Col(
                [
                html.H2('Number of Claims by State'),
                html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur faucibus rhoncus tortor eu accumsan. Morbi pellentesque ultrices arcu non molestie. Proin diam quam, vulputate nec consectetur eget, tristique nec nibh."),
                dcc.Graph(
                    id='claim-state',
                    figure=claims_state
                ),
                ]
            ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='example-map',
                    figure=map
                )
            ),
        ),
        dbc.Row(
            [
            dbc.Col(
                [
                html.H2('Property Damage by Year'),
                html.P("Our changing climate has increased the frequency of extreme weather events over time. Climate risk insurance can improve people's protection against climate-related loss and damage."),
                dcc.Graph(
                    id='claim-year',
                    figure=claim_year
                ),
                ]
            ),
            ]
        )
    ],
    fluid=False,
)

# @app.callback(
#     [Output("graph-gam", "figure"), Output("graph-coef", "figure")],
#     [Input("select-gam", "value"), Input("select-coef", "value")],
# )

if __name__ == "__main__":
    app.run_server(debug=True)

# def update_figures(gam_col, coef_col):

#     # Filter based on chosen column
#     xdf_filt = xdf[xdf.rule.str.contains(coef_col)].copy()
#     xdf_filt["desc"] = "<br>" + xdf_filt.rule.str.replace("AND ", "AND<br>")
#     xdf_filt["condition"] = [
#         [r for r in r.split(" AND ") if coef_col in r][0] for r in xdf_filt.rule
#     ]

#     coef_fig = px.bar(
#         xdf_filt,
#         x="desc",
#         y="coefficient",
#         color="condition",
#         title="Rules Explanations",
#     )
#     coef_fig.update_xaxes(showticklabels=False)

#     if plotLine[gam_col]:
#         plot_fn = px.line
#     else:
#         plot_fn = px.bar

#     gam_fig = plot_fn(
#         x=xPlot[gam_col],
#         y=yPlot[gam_col],
#         title="Generalized additive model component",
#         labels={"x": gam_col, "y": "contribution to log-odds of Y=1"},
#     )

#     return gam_fig, coef_fig








# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.

# from dash import Dash, html, dcc
# import plotly.express as px
# import pandas as pd

# app = Dash(__name__)

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)


# import dash
# from dash import dcc
# from dash import html
# import plotly.graph_objects as go
# from dash.dependencies import Input, Output, State


# #external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# external_stylesheets = ["https://raw.githubusercontent.com/plotly/dash-app-stylesheets/master/dash-goldman-sachs-report.css"]


# ################################################################################
# # APP INITIALIZATION
# ################################################################################
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# # this is needed by gunicorn command in procfile
# server = app.server


# ################################################################################
# # PLOTS
# ################################################################################
# LEGEND = ["clicks", "go fish!"]
# SCORES = [0.1, 0.1]


# def get_figure(legend, scores):
#     return go.Figure(
#         [go.Bar(x=legend, y=scores)],
#         layout=go.Layout(template="simple_white"),
#     )


# fig = get_figure(LEGEND, SCORES)

# ################################################################################
# # LAYOUT
# ################################################################################
# app.layout = html.Div(
#     [
#         html.H2(
#             id="title",
#             children="Neuefische Interactive Dash Plotly Dashboard",
#         ),
#         html.H3(
#             id="subtitle",
#             children="Add some fish text and click, and the chart will change",
#         ),
#         html.Div(children="Add some text you want (less than 10 characters)!"),
#         dcc.Textarea(
#             id="textarea-state-example",
#             value="",
#             style={"width": "100%", "height": 100},
#         ),
#         html.Button("Submit", id="textarea-state-example-button", n_clicks=0),
#         html.Div(id="textarea-state-example-output", style={"whiteSpace": "pre-line"}),
#         dcc.Graph(id="bar-chart", figure=fig),
#     ]
# )

# ################################################################################
# # INTERACTION CALLBACKS
# ################################################################################
# # https://dash.plotly.com/basic-callbacks
# @app.callback(
#     [
#         Output("textarea-state-example-output", "children"),
#         Output("bar-chart", "figure"),
#     ],
#     Input("textarea-state-example-button", "n_clicks"),
#     State("textarea-state-example", "value"),
# )
# def update_output(n_clicks, value):
#     fig = get_figure(LEGEND, SCORES)
#     if n_clicks > 0:
#         if 0 < len(value) < 10:
#             text = "you said: " + value
#             scores = [0.1 * n_clicks, 0.1]
#             fig = get_figure(LEGEND, scores)
#             return text, fig
#         else:
#             return "Please add a text between 0 and 10 characters!", fig
#     else:
#         return "", fig


# # Add the server clause:
# if __name__ == "__main__":
#     app.run_server()


# import dash
# from dash import dcc
# from dash import html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output
# import pandas as pd
# import plotly.express as px
# from sklearn.metrics import accuracy_score

# from utils import compute_plot_gam
# from modeling import lrr, df, fb, col_map
# from modeling import dfTrain, dfTrainStd, dfTest, dfTestStd, yTrain, yTest


# def Header(name, app):
#     title = html.H2(name, style={"margin-top": 5})
#     logo = html.Img(
#         src=app.get_asset_url("dash-logo.png"), style={"float": "right", "height": 50}
#     )

#     return dbc.Row([dbc.Col(title, md=9), dbc.Col(logo, md=3)])


# def LabeledSelect(label, **kwargs):
#     return dbc.FormGroup([dbc.Label(label), dbc.Select(**kwargs)])


# # Compute the explanation dataframe, GAM, and scores
# xdf = lrr.explain().rename(columns={"rule/numerical feature": "rule"})
# xPlot, yPlot, plotLine = compute_plot_gam(lrr, df, fb, df.columns)
# train_acc = accuracy_score(yTrain, lrr.predict(dfTrain, dfTrainStd))
# test_acc = accuracy_score(yTest, lrr.predict(dfTest, dfTestStd))


# # Start the app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server


# # Card components
# cards = [
#     dbc.Card(
#         [
#             html.H2(f"{train_acc*100:.2f}%", className="card-title"),
#             html.P("Model Training Accuracy", className="card-text"),
#         ],
#         body=True,
#         color="light",
#     ),
#     dbc.Card(
#         [
#             html.H2(f"{test_acc*100:.2f}%", className="card-title"),
#             html.P("Model Test Accuracy", className="card-text"),
#         ],
#         body=True,
#         color="dark",
#         inverse=True,
#     ),
#     dbc.Card(
#         [
#             html.H2(f"{dfTrain.shape[0]} / {dfTest.shape[0]}", className="card-title"),
#             html.P("Train / Test Split", className="card-text"),
#         ],
#         body=True,
#         color="primary",
#         inverse=True,
#     ),
# ]

# # Graph components
# graphs = [
#     [
#         LabeledSelect(
#             id="select-coef",
#             options=[{"label": v, "value": k} for k, v in col_map.items()],
#             value=list(xPlot.keys())[0],
#             label="Filter Features",
#         ),
#         dcc.Graph(id="graph-coef"),
#     ],
#     [
#         LabeledSelect(
#             id="select-gam",
#             options=[{"label": col_map[k], "value": k} for k in xPlot.keys()],
#             value=list(xPlot.keys())[0],
#             label="Visualize GAM",
#         ),
#         dcc.Graph("graph-gam"),
#     ],
# ]

# app.layout = dbc.Container(
#     [
#         Header("Flood Insurance – Opportunities Analysis", app),
#         html.Hr(),
#         dbc.Row([dbc.Col(card) for card in cards]),
#         html.Br(),
#         dbc.Row([dbc.Col(graph) for graph in graphs]),
#     ],
#     fluid=False,
# )


# @app.callback(
#     [Output("graph-gam", "figure"), Output("graph-coef", "figure")],
#     [Input("select-gam", "value"), Input("select-coef", "value")],
# )
# def update_figures(gam_col, coef_col):

#     # Filter based on chosen column
#     xdf_filt = xdf[xdf.rule.str.contains(coef_col)].copy()
#     xdf_filt["desc"] = "<br>" + xdf_filt.rule.str.replace("AND ", "AND<br>")
#     xdf_filt["condition"] = [
#         [r for r in r.split(" AND ") if coef_col in r][0] for r in xdf_filt.rule
#     ]

#     coef_fig = px.bar(
#         xdf_filt,
#         x="desc",
#         y="coefficient",
#         color="condition",
#         title="Rules Explanations",
#     )
#     coef_fig.update_xaxes(showticklabels=False)

#     if plotLine[gam_col]:
#         plot_fn = px.line
#     else:
#         plot_fn = px.bar

#     gam_fig = plot_fn(
#         x=xPlot[gam_col],
#         y=yPlot[gam_col],
#         title="Generalized additive model component",
#         labels={"x": gam_col, "y": "contribution to log-odds of Y=1"},
#     )

#     return gam_fig, coef_fig


# if __name__ == "__main__":
#     app.run_server(debug=True)
