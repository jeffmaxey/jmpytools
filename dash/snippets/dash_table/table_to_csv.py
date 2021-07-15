import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="Hello Subscriptions!"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "height": "180px",
                "lineHeight": "180px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "40px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="output-data-upload", style={"margin": "40px"}),
    ]
)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    if "csv" in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode("utf-8")),
            names=["date", "desc", "debit", "credit", "balance"],
        )
    elif "xls" in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(
            io.BytesIO(decoded), names=["date", "desc", "debit", "credit", "balance"]
        )

    return df


@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")],
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is None:
        raise PreventUpdate

    try:
        dfs = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    df = pd.concat(dfs)
    df = df.dropna(subset=["debit"])
    df["date"] = pd.to_datetime(df["date"])

    months = df.date.dt.month.unique()
    if len(months) < 4:
        return html.Div(["You must have at least 2 full months of data"])

    months = months[1:-1]
    first_month, months = months[0], months[1:]

    m1 = df[df["date"].dt.month == first_month]["desc"]
    is_rep = m1.isin(m1)
    for m in months:
        next_month = df[df["date"].dt.month == m]["desc"]
        is_rep = is_rep & m1.isin(next_month)

    rep = df[df["desc"].isin(m1[is_rep])]
    rep = rep.drop(columns=["credit", "balance"])
    rep["date"] = rep["date"].dt.strftime("%B %d, %Y")
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in rep.columns],
        data=rep.to_dict("records"),
    )

      
@app.callback(Output("download", "href"), [Input("choose-file", "value")])
def table_to_csv(val):
    df = my_dfs[val]
    df_b64 = b64encode(df.to_csv(index=False).encode())

    return "data:text/csv;base64," + df_b64.decode()

if __name__ == "__main__":
    app.run_server(debug=True)
    
