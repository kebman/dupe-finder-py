#!/usr/bin/env python2
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
	"""Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None"""
	try: 
		connection = sqlite3.connect(db_file)
		return connection
	except Error as e:
		print(e)
	return None

def create_table(connection, create_table_sql):
	"""Create a database table
	:param connection:
	:param create_table_sql:
	:return: Table object"""
	try:
		c = connection.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

def main():
	database = "db/pythonsqlite.db"

	sql_create_files_table = """CREATE TABLE IF NOT EXISTS files (
			id INTEGER PRIMARY KEY,
			filename TEXT NOT NULL,
			checksum BLOB,
			filesize INTEGER,
			btime TIMESTAMP,
			ctime TIMESTAMP,
			mtime TIMESTAMP,
			filepath_id INTEGER,
			FOREIGN KEY (filepath_id) REFERENCES filepaths (id)
		);"""
	sql_create_dirs_table = """CREATE TABLE
		IF NOT EXISTS filepaths (
			id INTEGER PRIMARY KEY,
			filepath TEXT NOT NULL,
			CONSTRAINT unique_path UNIQUE (filepath)
		);"""
	# create database connection:
	connection = create_connection(database)
	if connection is not None:
		create_table(connection, sql_create_files_table)
		create_table(connection, sql_create_dirs_table)
	else:
		print("Error: Couldn't create the db cnx")

if __name__ == '__main__':
	main()
