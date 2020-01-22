### All python files and functions needed for the Biomae project

You have to install mySQL connector with this command :
```
pip install mysql-connector-python
```

## Query

Query is an object to make SQL request to database and return the result as an array. It can get 5 arguments:

- table (need to be precise)
- column (can be a list or just a string)
- limit (an integer)
- filtre (egality/inegality or list of that)
- interval (variable, start, end)