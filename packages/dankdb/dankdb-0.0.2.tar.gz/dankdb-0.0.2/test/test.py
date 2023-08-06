from dankdb import Database

db = Database()
db.create_table('example', 'column1 TEXT', 'column2 TEXT', 'column3 TEXT')
db.insert_row('value1', 'value2', 'value3')
db.insert_row('value4', 'value5', 'value6')

print(db.fetch_table())

db.delete_rows()

print(db.fetch_table())

db.close()