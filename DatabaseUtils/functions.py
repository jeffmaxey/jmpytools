def get_unique(connection, db, table, col):
    query = f"""
    SELECT DISTINCT {col}
    FROM {db}.dbo.{table};
    """
    return [x[0] for x in connection.execute(query).fetchall()]


def get_range(connection, db, table, col):
    query = f"""
    SELECT MIN({col}), MAX({col})
    FROM {db}.dbo.{table};
    """
    return connection.execute(query).fetchall()[0]


def get_column_strings(df):
    # Load the actual csv file

    # Create SQL columns based on the columns of that dataframe
    types = (
        df.dtypes.copy()
        .replace("float64", "FLOAT")
        .replace("int64", "INT")
        .replace("object", "VARCHAR(100) COLLATE Latin1_General_BIN2")
    )

    ls = [f"{ix.lower()} {t}" for ix, t in zip(types.index, types.values)]
    return ",\n".join(ls)
