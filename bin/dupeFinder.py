#!/usr/bin/env python2
import os
import hashlib
import datetime
import sqlite3
from sqlite3 import Error

def sha256(fname):
	"""Return sha256 hash from input file (fname).
	:param fname:
	:return: Sha256 hash digest in hexadecimal"""
	hash_sha256 = hashlib.sha256()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(65536), b""):
			hash_sha256.update(chunk)
	return hash_sha256.hexdigest()

def getHRT(timestamp):
	"""Get human readable time from a Python timestamp.
	:param timestamp:
	:return: Human readable timestamp (HRT)"""
	dtval = datetime.datetime.fromtimestamp(timestamp)
	return dtval.strftime('%Y-%m-%d %H:%M:%S')

def getSQLT(timestamp):
	"""Make timestamp for SQLite from Python timestamp, meaning a UNIX epoch INTEGER.
	:param timestamp:
	:return: SQLite compatible timestamp in the form of a UNIX epoch INTEGER"""
	# I know this is a very small function, but now it's clear what SQL needs
	return int(timestamp) 

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

def check_exists(connection, path):
	"""Check the file path in the SQL filepaths table.
	:param connection:
	:param path:
	:return: path id"""
	exists = '''SELECT EXISTS(SELECT 1 FROM filepaths
		WHERE filepath = ?);'''
	cursor = connection.cursor()
	cursor.execute(exists, (path,))
	return cursor.fetchone()

def get_path(connection, path):
	"""Get the file path in the SQL filepaths table.
	:param connection:
	:param path:
	:return: path id"""
	select = '''SELECT id FROM filepaths 
		WHERE filepath = ?;'''
	cursor = connection.cursor()
	cursor.execute(select, (path,))
	return cursor.fetchone()[0]

def store_path(connection, path):
	"""Store the file path in the SQL filepaths table.
	:param connection:
	:param path:
	:return: path id"""
	insert = '''INSERT OR IGNORE INTO filepaths(filepath)
		VALUES(?)'''
	cursor = connection.cursor()
	cursor.execute(insert, (path,))
	return cursor.lastrowid

def store_file(connection, file):
	"""Store the file, hash and relevant file attributes in the SQL files table.
	:param connection:
	:param file:
	:return: Filepath ID"""
	sql = '''INSERT INTO files(filename, checksum, filesize, btime, ctime, mtime, filepath_id)
		VALUES(?, ?, ?, ?, ?, ?, ?)'''
	cursor = connection.cursor()
	cursor.execute(sql, file)
	return None
	# return cursor.lastrowid

def main():
	path = "."
	# UX (and OS X) spesific path names
	# homedir = os.path.expanduser('~')

	db_file = "db/pythonsqlite.db"
	connection = create_connection(db_file)
	with connection:
		os.chdir(path)
		for entry in os.walk("."):
			folder = str(entry[0])
			for file in entry[2]:
				filepath = 		os.getcwd() + folder[1:] #[1:] cuts out the preceding dot
				
				# only write if exists
				exists = check_exists(connection, filepath)
				if exists[0]:
					filepath_id = get_path(connection, filepath)
					# print('Fetched '+ str(filepath_id))
				else:
					filepath_id = store_path(connection, filepath)
					# print('Written '+ str(filepath_id))
				
				fullpathfile = 	os.getcwd() + folder[1:] + "/" + file
				file = 			file
				checksum = 		sha256(fullpathfile)
				size = 			os.stat(fullpathfile).st_size
				bstamp = 		os.stat(fullpathfile).st_birthtime
				cstamp = 		os.stat(fullpathfile).st_ctime
				mstamp = 		os.stat(fullpathfile).st_mtime

				fileInfo = (file, checksum, size, bstamp, cstamp, mstamp, filepath_id)
				store_file(connection, fileInfo)
				
				# test print:
				# print(str(getSQLT(birthstamp)) + " " + sha256(fullpathfile) + " " + fullpathfile + " " + str(size) + "b")

if __name__ == '__main__':
	main()
