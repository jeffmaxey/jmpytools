import dash  # 1.1.1
from dash.dependencies import Input, Output, State
import dash_table  # 4.1.0
import dash_core_components as dcc  # 1.1.1
import dash_html_components as html
from dash.exceptions import PreventUpdate

import numpy as np  # 1.17.0
import pandas as pd  # 0.25.0


def diff_dashtable(data, data_previous, row_id_name="row_id"):

    """Generate a diff of Dash DataTable data.
    Parameters
    ----------
    data: DataTable property (https://dash.plot.ly/datatable/reference)
        The contents of the table (list of dicts)
    data_previous: DataTable property
        The previous state of `data` (list of dicts).
    Returns
    -------
    A list of dictionaries in form of [{row_id_name:, column_name:, current_value:,
        previous_value:}]
    """

    df, df_previous = pd.DataFrame(data=data), pd.DataFrame(data_previous)

    for _df in [df, df_previous]:

        assert row_id_name in _df.columns

        _df = _df.set_index(row_id_name)

    mask = df.ne(df_previous)

    df_diff = df[mask].dropna(how="all", axis="columns").dropna(how="all", axis="rows")

    changes = []

    for idx, row in df_diff.iterrows():

        row_id = row.name

        row.dropna(inplace=True)

        for change in row.iteritems():

            changes.append(
                {
                    row_id_name: row_id,
                    "column_name": change[0],
                    "current_value": change[1],
                    "previous_value": df_previous.at[row_id, change[0]],
                }
            )

    return changes


app = dash.Dash(__name__)


dt_changes = []

COLUMNS = ["apple", "pear", "orange"]

N_ROWS = 1000


def create_data(columns, n_rows):

    size = n_rows * len(COLUMNS)

    data = np.random.randint(0, n_rows, size=size).reshape(n_rows, len(COLUMNS))

    df = pd.DataFrame(data=data, columns=COLUMNS)

    df.index.name = "row_id"

    return df.reset_index().to_dict(orient="records")


app.layout = html.Div(
    [
        dcc.Store(id="diff-store"),
        html.P("Changes to DataTable:"),
        html.Div(id="data-diff"),
        html.Button("Diff DataTable", id="button"),
        dash_table.DataTable(
            id="table-data-diff",
            columns=[{"id": col, "name": col, "type": "numeric"} for col in COLUMNS],
            editable=True,
            data=create_data(COLUMNS, N_ROWS),
            page_size=20,
        ),
    ]
)


@app.callback(
    Output("diff-store", "data"),
    [Input("table-data-diff", "data_timestamp")],
    [
        State("table-data-diff", "data"),
        State("table-data-diff", "data_previous"),
        State("diff-store", "data"),
    ],
)
def capture_diffs(ts, data, data_previous, diff_store_data):

    if ts is None:

        raise PreventUpdate

    diff_store_data = diff_store_data or {}

    diff_store_data[ts] = diff_dashtable(data, data_previous)

    return diff_store_data


@app.callback(
    Output("data-diff", "children"),
    [Input("button", "n_clicks")],
    [State("diff-store", "data")],
)
def update_output(n_clicks, diff_store_data):

    if n_clicks is None:

        raise PreventUpdate

    if diff_store_data:

        dt_changes = []

        for v in diff_store_data.values():

            dt_changes.append(f"* {v}")

        return [dcc.Markdown(change) for change in dt_changes]

    else:

        return "No Changes to DataTable"


if __name__ == "__main__":

    app.run_server(debug=True)
