# csv_to_sqlite
a somewhat hacky python script to import csv to sqlite and create table if necessary according to csv data types

---
This script will read a CSV file import it into the given sqlite file. Should the given table not exist it will create it. For this it analyses the first data row and tries to determine the data type for each field.

The first line must be the header. It's values are used as column names in the table.

If the table already exists the script assumes that it is in the right format for the csv file and will insert the data into the table. This means that the csv files header matches the column names and the csv files fields will match the column data type.

```
usage: import_csv_to_sqlite.py [-h] csv database table

Imports a CSV file into a SQLite3 database.

positional arguments:
  csv         path to the CSV file
  database    path to the SQLite database file
  table       table name

optional arguments:
  -h, --help  show this help message and exit
```
