import pandas as pd

conn = pyodbc.connect(r"Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=Test;autocommit = True;")
df_sql = pd.read_sql_query("SELECT * FROM %s".format(s=table), conn)

app = dash.Dash(__name__)
app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_sql.columns],
    data=df_sql.to_dict('records'),
)
