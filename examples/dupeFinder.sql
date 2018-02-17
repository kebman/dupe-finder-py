-- file table
CREATE TABLE
IF NOT EXISTS files (
	id INTEGER PRIMARY KEY,
	filename TEXT NOT NULL,
	checksum BLOB,
	filesize INTEGER,
	btime TIMESTAMP,
	ctime TIMESTAMP,
	mtime TIMESTAMP,
	filepath_id INTEGER,
	FOREIGN KEY (filepath_id) REFERENCES filepaths (id)
);

-- directory table
CREATE TABLE
IF NOT EXISTS filepaths (
	id INTEGER PRIMARY KEY,
	filepath TEXT NOT NULL,
	CONSTRAINT unique_path UNIQUE (filepath)
);

-- example insert:
INSERT OR IGNORE INTO filepaths(filepath)
SELECT id FROM filepaths 
WHERE filepath = '/Users/brkr2801/Dropbox/python/sqlite/documentation';
-- silently ignores errors if the entry already exists

-- example selects:

-- list the files and their paths (stored in different tables)
SELECT files.filename, filepaths.filepath
FROM files
INNER JOIN filepaths on filepaths.id = files.filepath_id;

-- search for an ID
SELECT id FROM filepaths WHERE filepath = '/Users/brkr2801/Dropbox/python/sqlite/documentation';

-- check if exists (returns 0 or 1)
SELECT EXISTS(SELECT id FROM filepaths
WHERE filepath = '/Users/brkr2801/Dropbox/python/sqlite/documentations');

-- check for duplicates
SELECT filename, COUNT(*) c FROM files 
GROUP BY checksum HAVING c > 1;

SELECT id, filename, COUNT(*) FROM files
GROUP BY btime HAVING COUNT(*) > 1;

SELECT id, filename, COUNT(*) FROM files
GROUP BY filesize HAVING COUNT(*) > 1;

-- Despite UNIQUE, it will still double-store a lot of values
-- as the path grows
-- because of this, the db will also become quite large
-- however this is FAR easier to manage than a Nested Set
-- or worse, an Adjacency List (though it's easier to generate)

-- note that ctime is attribute change time and not not file creation time
-- for file creation time, see birth time (btime)

-- birth time (btime) may be used to settle some confusion
-- when the checksum is equal, you may want the older file 
-- it seldom makes much of a difference though, 
-- unless you're entangled in some legal battle...
-- when the checksum is not equal, you probably want the newer file

-- contents modification time (mtime) may however be the most relevant
-- usually you want the file that was modified last, but not always

-- access time (atime) is not relevant for this project
-- as we're not trying to find trespassers
