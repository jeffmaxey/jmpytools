#!/usr/bin/env python

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable
from dash_table.Format import Format
import pandas as pd

app = dash.Dash(__name__)


df= pd.read_csv('outliers_long.csv')
subjects = df[df.columns[0]].values

data_condition = [{
    'if': {'row_index': 'odd'},
    'backgroundColor': 'rgb(240, 240, 240)'
}]

for d in [{
    'if': {
        'column_id': c,
        'filter_query': f'{{{c}}} gt 2',
    },
    'backgroundColor': 'red',
    'color': 'black',
    'fontWeight': 'bold'
} for c in df.columns[1:]]:
    data_condition.append(d)

app.layout = html.Div([

    'Type of visual inspection upon selecting a cell: ',
    html.Div([
        dcc.Dropdown(
            id='view-type',
            options=[{'label': i, 'value': i} for i in ['snapshot', 'freeview']],
            value='snapshot'
        )
    ],
        style={'width': '10%', }),
    html.Br(),

    DataTable(
        id='table',
        columns=[{'name': i,
                  'id': i,
                  'hideable': True,
                  'type': 'numeric',
                  'format': Format(precision=4),
                  } for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        style_data_conditional=data_condition,
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'pre-wrap'
        },

        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },

        tooltip_data=[{c:
            {
                'type': 'text',
                'value': f'{r}, {c}'
            } for c in df.columns
        } for r in subjects]
    ),
    html.Div(id='table-tooltip')
])


if __name__=='__main__':
    app.run_server(debug=True, port= 8030, host= 'localhost')
