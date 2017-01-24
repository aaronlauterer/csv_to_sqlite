import sqlite3
import argparse
import unicodecsv as csv
import numbers
import sys

def db_init(reader:csv.DictReader, cur:sqlite3.Cursor, filein, table) -> list:
    line = next(reader)
    db_fields = {}
    db_columns = []

    for key in line.keys():
        db_columns.append(key)
        if line[key].isdigit():
            # is integer
            db_fields[key] = 'INTEGER'
        elif line[key].lstrip('-').replace('.', '', 1).isdigit():
            # is float/complex
            db_fields[key] = 'FLOAT'
        else:
            db_fields[key] = 'TEXT'
    # reset file line iterator
    filein.seek(0)
    next(reader)
    # run db init with key value concatenated to string
    cur.execute('CREATE TABLE IF NOT EXISTS '+table+' (' +
                ', '.join(['%s %s' % (key, value) for (key, value) in db_fields.items()]) + ')')

    return db_columns

def import_csv():
    parser = argparse.ArgumentParser(description="Imports a CSV file into a SQLite3 database.")
    parser.add_argument('csv', help='path to the CSV file')
    parser.add_argument('database', help='path to the SQLite database file')
    parser.add_argument('table', help='table name')

    args = parser.parse_args()

    try:
        filein = open(args.csv, 'rb')
    except OSError as err:
        print('''-----------------------
Error opening CSV file!
-----------------------''')
        print("OS error: {0}".format(err) + "\n")
        sys.exit(1)

    reader = csv.DictReader(filein, delimiter='|')
    csv.field_size_limit(500 * 1024 * 1024)

    try:
        conn = sqlite3.connect(args.database)
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(e)
        sys.exit(1)
    cur = conn.cursor()

    db_columns = db_init(reader, cur, filein, args.table)

    # add papers to table
    for line in reader:
        db_fields = []
        print("csv line nr: " + str(reader.line_num))
        for key in line.keys():
            db_fields.append(line[key])

        qmarks = ','.join(['?'] * len(db_fields))
        columns = ','.join(db_columns)
        # print("INSERT INTO papers (" + columns + ") VALUES ({qm});".format(qm=qmarks))
        cur.execute("INSERT INTO " + args.table + " (" + columns + ") VALUES ({qm});".format(qm=qmarks), db_fields)

    conn.commit()


    filein.close()

    print("---- Done ----")

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    import sys
    import_csv()
