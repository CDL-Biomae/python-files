### All python files and functions needed for the Biomae project

You have to install mySQL connector with this command :
```
pip install mysql-connector-python
```
Be sure to have the env.py file before lauch any programm


## Query

Query is an object to make SQL request to database and return the result as an array. It can get 5 arguments:

- 'table' where you are looking for(need to be precise)
- 'column' you wanted to see (can be a list or just a string)
- 'limit' number of result (an integer)
- 'group' to regroup by one particular value (string)
- 'filtre' (egality/inegality or list of that)
- 'interval' (variable, start, end)
- 'distinct' if you only the different outputs without any duplicate (boolean)  