import sqlite3
import csv


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

		self.values = []
		self.columns = []

		print("Database initialized...\n")

	def create_table(self, table_name, *args, **kwargs):
		"""Takes in a table name and multiple column names then creates a table"""
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
		print("Table created...\n")

	def insert_row(self, *args, **kwargs):
		"""Takes in a row of values and adds them into the table"""
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
		print("Values added...\n")

	def delete_rows(self):
		"""Removes all rows from table"""
		command = f"DELETE FROM {self.table_name}"
		self.c.execute(command)
		self.conn.commit()
		print("All rows removed...\n")

	def fetch_table(self):
		"""Retrieves all values within the table"""
		self.c.execute("SELECT * FROM " + self.table_name)
		values = self.c.fetchall()
		self.conn.commit()
		print("Values retrieved...\n")
		return values

	def export_csv(self, file_name):
		"""Export table into a csv file with given name."""
		self.c.execute("SELECT * FROM "+ self.table_name)
		columns = [tuple[0] for tuple in self.c.description]
		rows = self.fetch_table()

		with open(f'{file_name}.csv', 'w') as f:
		    writer = csv.writer(f, delimiter='\t')
		    writer.writerow(columns)
		    for row in rows:
		    	writer.writerow(row)
		print("DB exported to csv...\n")

	def read_csv(self, file_name):
		"""prints out all values in table"""
		with open(f'{file_name}.csv', 'r') as f:
			reader = csv.reader(f, delimiter="\t")
			for row in reader:
				if (row):
					print(row)

	def close(self):
		"""closes connection to db"""
		self.conn.close()
		print("Connection to db closed...\n")
