import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px

from graphing import counties, claims_by_year, agg_total

from modeling import df #lrr, df, fb, col_map
from modeling import dfTrain, dfTest,  yTrain, yTest #dfTrainStd, dfTestStd,


def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
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
            html.H2(f"{dfTrain.shape[0]:,} / {dfTest.shape[0]:,}", className="card-title"),
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
    title={'text': 'Number of Claims Filed by State','y':0.93,'x':0.5,'xanchor': 'center','yanchor':'top'},
    xaxis_title='State',
    yaxis_title='Number of Claims Filed',
)
claim_year = px.bar(
    claims_by_year,
    x='yearOfLoss',
    y='total_claims',
    #title='',
    #text_auto=True,
    #text_auto='.2s',
    #text='yearOfLoss'
)
#claim_year.update_traces(textfont_size=20, textangle=0, cliponaxis=False)
claim_year.update_layout(
    title={'text': 'Property Damage by Year (in $)','y':0.93,'x':0.5,'xanchor': 'center','yanchor':'top'},
    xaxis_title='Year of Damage',
    yaxis_title='Claim Amount Paid ($)',
)

app.layout = dbc.Container(
    [
        Header("Flood Insurance – Minimizing Opportunity Costs", app),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                [

                ]
            )
        ),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        #dbc.Row([dbc.Col(graph) for graph in graphs]),
        dbc.Row(
            [
            dbc.Col(
                [
                html.H3('Number of Claims by State'),
                html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur faucibus rhoncus tortor eu accumsan. Morbi pellentesque ultrices arcu non molestie. Proin diam quam, vulputate nec consectetur eget, tristique nec nibh."),
                dcc.Graph(
                    id='claim-state',
                    figure=claims_state
                ),
                ]
            ),
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                [
                html.H3("Mapping Claims, Coverage, and Policies by County"),
                html.P("Select a map:"),
                dcc.RadioItems(
                    id='map_select', 
                    options={
                        "log_total_claims": "Total Claim Amount ", 
                        "log_total_coverage":"Total Coverage", 
                        },
                    value="log_total_claims",
                    labelStyle = {'display': 'block', 'cursor': 'pointer', 'margin-left':'20px'}
                    #inline=True
                ),
                dcc.Graph(
                    id='map',
                    #figure=map
                )
                ]
            ),
        ),
        html.Br(),
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

@app.callback(
    Output("map", "figure"), 
    Input("map_select", "value"),
)
def display_choropleth(map_select):
    map = px.choropleth(agg_total, geojson=counties, locations='countyCode', color=map_select,
                           color_continuous_scale="Viridis_r",
                           #range_color=(0, 12),
                           scope="usa",
                           labels={'log_total_claims':'Claims Total','log_total_coverage':'Coverage Total'},
                           hover_name="NAME",
                           hover_data=['state',"countyCode","total_claims",'total_coverage'],
                           # custom_data=["countyCode","total_claims",'total_coverage'],
                          )
    # map.update_traces(
    #     hovertemplate="<br>".join([
    #         # "Col: %{x}",
    #         # "ColY: %{y}",
    #         "countyCode: %{customdata[0]}",
    #         "total_claims: %{customdata[1]}",
    #         "total_coverage: %{customdata[2]}",
    #     ])
    # )
    map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return map

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


if __name__ == "__main__":
    app.run_server(debug=True)