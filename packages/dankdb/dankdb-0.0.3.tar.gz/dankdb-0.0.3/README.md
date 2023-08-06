# DankDB - Simple Database
[![](https://img.shields.io/badge/Author-DankSideSparkles-lightgrey?style=plastic)](https://github.com/DankSideSparkles)
[![](https://img.shields.io/github/languages/top/DankSideSparkles/DankDB.svg?style=plastic)](https://github.com/DankSideSparkles/DankDB)
[![](https://img.shields.io/github/v/tag/DankSideSparkles/DankDB?style=plastic)](https://github.com/DankSideSparkles/DankDB/releases)
[![](https://img.shields.io/github/issues/DankSideSparkles/DankDB?style=plastic)](https://github.com/DankSideSparkles/DankDB/issues)

This simple, yet useful module allows the user to create a database for small scale projects; the user can easily add values to the database while simultaneously retrieving values. 


## Features:

•    create_table - Takes in a table name and multiple column names then creates a table.
•    insert_row - Takes in a row of values and adds them into the table.
•    delete_rows - Removes all rows from table.
•    fetch_table - Retrieves all values within the table.
•    export_csv - Export table into a csv file with given table name.
•    read_csv - Prints out all values in table with given table name.
•    close - Closes connection to database.


## How to install

`pip install dankdb`


## How to use

#### Example code

```python
from dankdb import Database

db = Database()
db.create_table('example', 'column1 TEXT', 'column2 TEXT', 'column3 TEXT')
db.insert_row('value1', 'value2', 'value3')
db.insert_row('value4', 'value5', 'value6')

print(db.fetch_table())

db.close()
```


## Feature request

If there is a feature that you would like implemented, open an issue, and I will work on it.