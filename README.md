# dupe-finder-py
A bare-bones duplicate file finder with Python and SQLite

## Prereqs
Some knowledge of how to navigate a Terminal application and use SQL is required to use these scripts. Oh, and you need to know how to run a Python script. Google it if you don't know how. You may also have to install SQLite3. The files were originally made for UX systems including Mac OS X. For usage on Windoze, you may have to change the script a little, and change direction of a few slashes.

## Usage
Run /bin/createTables.py first and then edit /bin/dupeFinder.py to search the folder of your desire. Then the SQLite editor of your choice and input the SQL-statements in /examples/dupeFinder.sql to find duplicates. 

## Warning
It will search all sub-directories recursively, so it may take a lot of time if you start it too close to the hard drive root. Hit Ctrl+C if you get bored. Depending on the amount of folders and files you search, the database may also grow very large. However once you're done with it, you can simply delete it (or back it up for later, if you're one of those types).

## Future Ideas
After data is collected, it could be prudent to prune the database of non-dupes. A bash or python script can then be made to automagically erase the dupes by some systemation or another. I never got that far, and I don't really want to make any promises I can't keep either, as this was more of a fun hobby project for me in order to learn Python. Still hope you enjoy it! ^^

## Love
If you liked this project, consider donating a few hundred bitcoins to 1B7axexG6avxtexusiCETzhqeHtAhqtasc :D

Feel free to copy and edit the code, as per BSD3 license.
