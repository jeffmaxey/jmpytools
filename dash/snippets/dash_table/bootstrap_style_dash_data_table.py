import dash_html_components as html
import dash_table
import pandas as pd


def data_table(df):
    table = html.Div(
        className='table table-responsive-md p-3',
        children=dash_table.DataTable(
                id='tabella-milano',
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
    
                page_size=50, 
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                column_selectable="single",
                style_table={"fontFamily": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"'},
                style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'padding':'0.75rem'
                    },
                style_cell={
                    "fontFamily": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                    'fontWeight': '400',
                    'lineHeight': '1.5',
                    'color': '#212529',
                    'textAlign': 'left',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'padding':'0.75rem',
                    'border': '1px solid #dee2e6',
                    'verticalAlign': 'top',
                },
                style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                }
            ],
                ))

    return table
