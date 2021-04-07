import sqlite3

def generate_docs(db, docs, title):
    # open doc file and define table template
    f = open(docs, "w+")
    f.write(title + "\n")
    table_template = "|{}|{}|\n| :-: | :-:|\n".format(
        "COLUMN", "DESCRIPTION")
    # open database
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in c.fetchall():
        # print table name
        table_name = table[0].upper()
        f.write("### {}\n".format(table_name))
        f.write(table_template)
        # print table columns
        c.execute("SELECT * FROM {};".format(table_name))
        cols = [description[0] for description in c.description]
        for col in cols:
            f.write("| {} | |\n".format(col))
    f.close()


generate_docs("./chinook.sqlite", "Chinook_template.md",
              "# Chinook Database Documentation")
