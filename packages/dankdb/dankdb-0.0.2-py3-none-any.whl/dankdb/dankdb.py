import sqlite3


class Database():
	"""This is a simple multi use case database class"""
	def __init__(self, useMemory=True):
		if useMemory:
			self.conn = sqlite3.connect(':memory:')
		else:
			user_input = input("Name of db?\n")
			self.conn = sqlite3.connect(f"{user_input}.db")

		self.c = self.conn.cursor()

		self.table_name = ""

		print("Database initialized...")

	def create_table(self, table_name, *args, **kwargs):
		"""This function will take a table name and mutliple column names then create a table"""
		self.table_name = table_name

		string = ["("]
		x = 1
		for column in args:
			if x == len(args):
				string.append(f"{column})")
			else:
				string.append(f"{column}, ")
			x += 1

		string = "".join(string)

		command = f"CREATE TABLE {self.table_name} {string}"
		self.c.execute(command)
		self.conn.commit()
		print("Table created...")


	def insert_row(self, *args, **kwargs):
		"""This function will take values and add them into the rows of the table"""
		string = ["("]
		for x in range(len(args)):
			if x == (len(args) - 1):
				string.append("?)")
			else:
				string.append('?, ')

		string = "".join(string)

		command = f"INSERT INTO {self.table_name} VALUES {string}"
		self.c.execute(command, args)
		self.conn.commit()
		print("Values added...")

	def delete_rows(self):
		"""This function will remove all rows from db"""
		command = f"DELETE FROM {self.table_name}"
		self.c.execute(command)
		self.conn.commit()
		print("All rows removed...")

	def fetch_table(self):
		"""This function will retrieve all values from the table"""
		self.c.execute("SELECT * FROM " + self.table_name)
		values = self.c.fetchall()
		self.conn.commit()
		print("Values retrieved...")
		return values

	def close(self):
		"""This function will close the connection to the db"""
		self.conn.close()
		print("Connection to db closed...")
