# DankDB - Simple Database
[![](https://img.shields.io/badge/Author-DankSideSparkles-lightgrey?style=plastic)](https://github.com/DankSideSparkles)
[![](https://img.shields.io/github/languages/top/DankSideSparkles/DankDB.svg?style=plastic)](https://github.com/DankSideSparkles/DankDB)
[![](https://img.shields.io/github/v/tag/DankSideSparkles/DankDB?style=plastic)](https://github.com/DankSideSparkles/DankDB/releases)
[![](https://img.shields.io/github/issues/DankSideSparkles/DankDB?style=plastic)](https://github.com/DankSideSparkles/DankDB/issues)

This database module will allow you to create simple databases for small scale projects. Can easily add values to the database and retrieve them.
 
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
