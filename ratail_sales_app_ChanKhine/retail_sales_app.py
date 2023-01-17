# author: Chan Khine
# Updated to add charts and cards show individual store data by having user selects a store

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import natsort

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output

from data_loader import retail_sales_df, monthly_sales_df, weekly_sales_df, store_df, dept_df, updated_store_df, \
    weekly_store_sales_df, dept_store_df


# Code for web application
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

'''
The title bar
'''
navbar = dbc.Navbar(id='navbar', children=[
    dbc.Row([
        dbc.Col(dbc.NavbarBrand('Retail Sales Dashboard',
                                style={'color': 'white', 'fontSize': '25px', 'fontFamily': 'Times New Roman'}
                                )
                )
    ], align="center",
        # no_gutters = True
    ),
], color='#090059')

'''
Drop down includes the selection for two months that the user wants to compare for the sales. 
It also includes the dropdown for store selection.
'''
card_content_dropdwn = [
    dbc.CardBody(
        [
            html.H6('Select Months', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([
                    html.H6('Current Period'),
                    dcc.Dropdown(id='dropdown_base',
                                 options=[
                                     {'label': i, 'value': i} for i in monthly_sales_df.sort_values('month')['Month']
                                 ],
                                 value='Feb',
                                 )
                ]),

                dbc.Col([
                    html.H6('Reference Period'),
                    dcc.Dropdown(id='dropdown_comp',
                                 options=[
                                     {'label': i, 'value': i} for i in monthly_sales_df.sort_values('month')['Month']
                                 ],
                                 value='Jan',
                                 )
                ]),
            ])
        ],
    ),
    # Added a new card body so users can choose the store from the dropdown
    dbc.CardBody(
        [
            html.H6('Select Store', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([
                    html.H6('Current Store'),
                    dcc.Dropdown(id='dropdown_store',
                                 options=[
                                             {'label': 'All Stores', 'value': 'All Stores'}
                                         ] + [
                                             {'label': i, 'value': i} for i in
                                             store_df.sort_values('Store', key=natsort.natsort_keygen())[
                                                 'Store'].unique()
                                         ],
                                 value='All Stores',
                                 )
                ])
            ])
        ])
]

# layout of everything
body_app = dbc.Container([

    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([dbc.Card(card_content_dropdwn, style={'height': '300px'})], width=4),
        dbc.Col([dbc.Card(id='card_num1', style={'height': '150px'})]),
        dbc.Col([dbc.Card(id='card_num2', style={'height': '150px'})]),
        dbc.Col([dbc.Card(id='card_num3', style={'height': '150px'})]),

    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([dbc.Card(id='card_num4', style={'height': '350px'})]),
        dbc.Col([dbc.Card(id='card_num5', style={'height': '350px'})]),
        dbc.Col([dbc.Card(id='card_num6', style={'height': '350px'})]),
    ]),
    html.Br(),
    html.Br()
],
    style={'backgroundColor': '#f7f7f7'},
    fluid=True)

app.layout = html.Div(id='parent', children=[navbar, body_app])


# callback for interaction
@app.callback([Output('card_num1', 'children'),
               Output('card_num2', 'children'),
               Output('card_num3', 'children'),
               Output('card_num4', 'children'),
               Output('card_num5', 'children'),
               Output('card_num6', 'children'),
               ],
              [Input('dropdown_base', 'value'),
               Input('dropdown_comp', 'value'),
               Input('dropdown_store', 'value')])
def update_cards(base, comparison, store):
    """
    If the user wants to view all stores, all figures will update for all stores' sales.
    If the user wants to view individual store data, all figures will update for individual store data.
    :param base: base month
    :param comparison: the month to compare
    :param store: the store the user wants to look at
    :return: the sales calculations and figures
    """

    if store == 'All Stores':
        # Calculating all stores sales for base and comparison months
        sales_base = monthly_sales_df.loc[monthly_sales_df['Month'] == base].reset_index()['Weekly_Sales'][0]
        sales_comp = monthly_sales_df.loc[monthly_sales_df['Month'] == comparison].reset_index()['Weekly_Sales'][0]

        diff_1 = np.round(sales_base - sales_comp, 1)

        # Calculating all stores sales for base and comparison months on holidays
        holi_base = monthly_sales_df.loc[monthly_sales_df['Month'] == base].reset_index()['Holiday_Sales'][0]
        holi_comp = monthly_sales_df.loc[monthly_sales_df['Month'] == comparison].reset_index()['Holiday_Sales'][0]

        diff_holi = np.round(holi_base - holi_comp, 1)

        # Calculating store count for base and comparison months
        base_st_ct = retail_sales_df.loc[retail_sales_df['Month'] == base, 'Store'].drop_duplicates().count()
        comp_st_ct = retail_sales_df.loc[retail_sales_df['Month'] == comparison, 'Store'].drop_duplicates().count()

        diff_store = np.round(base_st_ct - comp_st_ct, 1)

        # Calculating weekly sales for base and comparison months
        weekly_base = weekly_sales_df.loc[weekly_sales_df['Month'] == base].reset_index()
        weekly_comp = weekly_sales_df.loc[weekly_sales_df['Month'] == comparison].reset_index()

        # Calculating the stores with the highest sales for base and comparison months
        store_base = store_df.loc[store_df['Month'] == base].sort_values('Weekly_Sales',
                                                                         ascending=False).reset_index()[:10]
        store_comp = store_df.loc[store_df['Month'] == comparison].sort_values('Weekly_Sales',
                                                                               ascending=False).reset_index()[:10]

        # Calculating the sales difference between top departments for base and comparison months
        dept_base = dept_df.loc[dept_df['Month'] == base].sort_values('Weekly_Sales',
                                                                      ascending=False).reset_index()[:10]
        dept_base = dept_base.rename(columns={'Weekly_Sales': 'Weekly_Sales_base'})
        dept_comp = dept_df.loc[dept_df['Month'] == comparison].sort_values('Weekly_Sales',
                                                                            ascending=False).reset_index()
        dept_comp = dept_comp.rename(columns={'Weekly_Sales': 'Weekly_Sales_comp'})

        merged_df = pd.merge(dept_base, dept_comp, on='Dept', how='left')
        merged_df['diff'] = merged_df['Weekly_Sales_base'] - merged_df['Weekly_Sales_comp']

    else:
        # Calculating individual store sales for base and comparison months
        sales_base = store_df.loc[(store_df['Month'] == base) & (store_df['Store'] == store)] \
            .reset_index()['Weekly_Sales'][0]
        sales_comp = store_df.loc[(store_df['Month'] == comparison) & (store_df['Store'] == store)] \
            .reset_index()['Weekly_Sales'][0]

        diff_1 = np.round(sales_base - sales_comp, 1)

        # Calculating individual stores sales for base and comparison months on holidays
        holi_base = updated_store_df.loc[(updated_store_df['Month'] == base) & (updated_store_df['Store'] == store)] \
            .reset_index()['Holiday_Sales'][0]
        holi_comp = \
        updated_store_df.loc[(updated_store_df['Month'] == comparison) & (updated_store_df['Store'] == store)] \
            .reset_index()['Holiday_Sales'][0]

        diff_holi = np.round(holi_base - holi_comp, 1)

        # Store count
        base_st_ct = store_df.loc[(store_df['Month'] == base) & (store_df['Store'] == store)]. \
            drop_duplicates().count()[0]
        comp_st_ct = store_df.loc[(store_df['Month'] == comparison) & (store_df['Store'] == store)]. \
            drop_duplicates().count()[0]

        diff_store = np.round(base_st_ct - comp_st_ct, 1)

        # Weekly sales for the store
        weekly_base = weekly_store_sales_df.loc[(weekly_store_sales_df['Month'] == base) &
                                                (weekly_store_sales_df['Store'] == store)].reset_index()
        weekly_comp = weekly_store_sales_df.loc[(weekly_store_sales_df['Month'] == comparison) &
                                                (weekly_store_sales_df['Store'] == store)].reset_index()

        # Total sales for the store
        store_base = store_df.loc[(store_df['Month'] == base) & (store_df['Store'] == store)].reset_index()
        store_comp = store_df.loc[(store_df['Month'] == comparison) & (store_df['Store'] == store)].reset_index()

        # Total sales for each department of the store
        dept_base = dept_store_df.loc[(dept_store_df['Month'] == base) & (dept_store_df['Store'] == store)]. \
                        sort_values('Weekly_Sales', ascending=False).reset_index()[:10]
        dept_base = dept_base.rename(columns={'Weekly_Sales': 'Weekly_Sales_base'})
        dept_comp = dept_store_df.loc[(dept_store_df['Month'] == comparison) & (dept_store_df['Store'] == store)]. \
            sort_values('Weekly_Sales', ascending=False).reset_index()
        dept_comp = dept_comp.rename(columns={'Weekly_Sales': 'Weekly_Sales_comp'})

        merged_df = pd.merge(dept_base, dept_comp, on='Dept', how='left')
        merged_df['diff'] = merged_df['Weekly_Sales_base'] - merged_df['Weekly_Sales_comp']

    # Figures for retail sales
    # Line charts for weekly sales comparison for each month
    fig = go.Figure(data=[go.Scatter(x=weekly_base['week_no'], y=weekly_base['Weekly_Sales'],
                                     line=dict(color='firebrick', width=4), name='{}'.format(base)),
                          go.Scatter(x=weekly_comp['week_no'], y=weekly_comp['Weekly_Sales'],
                                     line=dict(color='#090059', width=4), name='{}'.format(comparison))])

    fig.update_layout(plot_bgcolor='white',
                      margin=dict(l=40, r=5, t=60, b=40),
                      yaxis_tickprefix='$',
                      yaxis_ticksuffix='M')

    # Total sales for each month in bar chart
    fig2 = go.Figure([go.Bar(x=store_base['Weekly_Sales'],
                             y=store_base['Store'],
                             name='{}'.format(base),
                             text=store_base['Weekly_Sales'], orientation='h',
                             textposition='outside'
                             ),
                      ])

    fig3 = go.Figure([go.Bar(x=store_comp['Weekly_Sales'],
                             y=store_comp['Store'],
                             name='{}'.format(comparison),
                             text=store_comp['Weekly_Sales'], orientation='h',
                             textposition='outside'
                             ),
                      ])

    fig2.update_layout(plot_bgcolor='white',
                       xaxis=dict(range=[0, '{}'.format(store_base['Weekly_Sales'].max() + 3)]),
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_tickprefix='$',
                       xaxis_ticksuffix='M',
                       title='{}'.format(base),
                       title_x=0.5)

    fig3.update_layout(plot_bgcolor='white',
                       xaxis=dict(range=[0, '{}'.format(store_comp['Weekly_Sales'].max() + 3)]),
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_tickprefix='$',
                       xaxis_ticksuffix='M',
                       title='{}'.format(comparison),
                       title_x=0.5)

    # Sales difference between top departments for the store
    fig4 = go.Figure([go.Bar(x=merged_df['diff'],
                             y=merged_df['Dept'],
                             text=merged_df['diff'].round(1),
                             orientation='h',
                             textposition='outside'
                             ),
                      ])

    fig4.update_layout(plot_bgcolor='white',
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_tickprefix='$',
                       xaxis_ticksuffix='M'
                       )

    # Adding metrics for different card bodies
    # Total sales
    if diff_1 >= 0:
        a = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>+{0}{1}{2}</sub>".format('$', diff_1, 'M')],
                         style={'textAlign': 'center'})
    elif diff_1 < 0:
        a = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>-{0}{1}{2}</sub>".format('$', np.abs(diff_1), 'M')],
                         style={'textAlign': 'center'})

    # Holiday sales
    if diff_holi >= 0:
        b = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>+{0}{1}{2}</sub>".format('$', diff_holi, 'M')],
                         style={'textAlign': 'center'})
    elif diff_holi < 0:
        b = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>-{0}{1}{2}</sub>".format('$', np.abs(diff_holi), 'M')],
                         style={'textAlign': 'center'})

    # Store count
    if diff_store >= 0:
        c = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>+{0}</sub>".format(diff_store)],
                         style={'textAlign': 'center'})
    elif diff_store < 0:
        c = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>-{0}</sub>".format(np.abs(diff_store))],
                         style={'textAlign': 'center'})

    # Contents for card bodies
    # Total sales
    card_content = [
        dbc.CardBody(
            [
                html.H6('Total sales', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
                html.H3('{0}{1}{2}'.format("$", sales_base, "M"),
                        style={'color': '#090059', 'textAlign': 'center'}),
                a
            ]
        )
    ]

    # Holiday sales
    card_content1 = [
        dbc.CardBody(
            [
                html.H6('Holiday Sales', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
                html.H3('{0}{1}{2}'.format("$", holi_base, "M"), style={'color': '#090059', 'textAlign': 'center'}),
                b
            ]
        )
    ]

    # Store count
    card_content2 = [
        dbc.CardBody(
            [
                html.H6('Total Stores', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
                html.H3('{0}'.format(base_st_ct), style={'color': '#090059', 'textAlign': 'center'}),
                c
            ]
        )
    ]

    # Line charts to compare weekly sales in each month
    card_content3 = [
        dbc.CardBody(
            [
                html.H6('{0} Weekly Sales Comparison'.format(store),
                        style={'fontWeight': 'bold', 'textAlign': 'center'}),
                dcc.Graph(figure=fig, style={'height': '250px'})
            ]
        )
    ]

    # Bar charts to compare total sales
    if store == 'All Stores':
        card_content4 = [
            dbc.CardBody(
                [
                    html.H6('Stores with highest Sales', style={'fontWeight': 'bold', 'textAlign': 'center'}),
                    dbc.Row([
                        dbc.Col([dcc.Graph(figure=fig2, style={'height': '300px'}), ]),
                        dbc.Col([dcc.Graph(figure=fig3, style={'height': '300px'}), ])

                    ])
                ]
            )
        ]

    else:
        card_content4 = [
            dbc.CardBody(
                [
                    html.H6('{0} Total Sales'.format(store), style={'fontWeight': 'bold', 'textAlign': 'center'}),
                    dbc.Row([
                        dbc.Col([dcc.Graph(figure=fig2, style={'height': '300px'}), ]),
                        dbc.Col([dcc.Graph(figure=fig3, style={'height': '300px'}), ])

                    ])
                ]
            )
        ]

    card_content5 = [
        dbc.CardBody(
            [
                html.H6(
                    'Sales difference between Top departments for {0} ({1} - {2})'.format(store, base, comparison),
                    style={'fontWeight': 'bold', 'textAlign': 'center'}),
                dcc.Graph(figure=fig4, style={'height': '300px'})
            ]
        )
    ]
    return card_content, card_content1, card_content2, card_content3, card_content4, card_content5


if __name__ == '__main__':
    app.run_server(debug=True)
