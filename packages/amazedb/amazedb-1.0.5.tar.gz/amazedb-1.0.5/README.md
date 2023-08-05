# amazedb
![Upload Python Package](https://github.com/jalaj-k/amazedb/workflows/Upload%20Python%20Package/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.5-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

 It is a file based NoSQL database management system written in python.
 
 All the databases are stored in the ```db``` sub-directory of the current directory. This behaviour can be manipulated as we'll see later on.

## Using the database

 The database can simply be used by cloning the project in a directory you may call ```amazedb``` and then create another directory named ```db``` in your projects root. Then import the main file as:

```python
from amazedb import dbms as db
```

This will create the namespace ```db``` in your file.

## Creating and accessing databases

 Now that you have imported the dbms, you can access a database with the following code:

```python
mydb = db.db('mydb')
```

This will try to locate the ```./db``` directory relative to the file you are working on. To locate a different directory, you can use:

```python
mydb = db.db('mydb', dbPath="D:/project")
```

In this case, it will look for ```D:/project/db``` directory. 

Now, what next? The project will see if the *mydb* database exists in that directory. If it exists, well and good otherwise it will be created by default. To override this behaviour, simply use:

```python
mydb = db.db('mydb', safeMode=False)
```

In this case, an exception will be raised if the database is not found.

*This page is still incomplete. We're working on it*