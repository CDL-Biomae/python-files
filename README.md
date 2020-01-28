### All python files and functions needed for the Biomae project

You have to install mySQL connector with this command :
```
pip install mysql-connector-python
```
Be sure to have the env.py file before lauch any programm


## Query

Query is an object to make SQL request to database and return the result as an array. It can get 5 arguments:

- 'table' where you are looking for (need to be precise)
- 'column' you wanted to see (can be a list or just a string)
- 'limit' number of result (an integer)
- 'group' to regroup by one particular value (string)
- 'filtre' (egality/inegality or list of that)
- 'interval' (variable, start, end)
- 'distinct' if you only the different outputs without any duplicate (boolean)

Example : Query("agency", "city", "2") is an object with the two first 'city' values from the table 'agency'. (SQL script : SELECT city FROM agency LIMIT 2 )

Finally, you have to run the function execute() to get the response.



If you prefer to write on your own, you can use the object QueryScript. It can get 2 arguments:

- 'script' : ths SQL script you want to use
- 'rows' : when you wanted to add in database plurar rows (Array).

to execute the filler, use the fonction executemany() with the to arguments completed.

## Fill the database with xlsm reference

To add all reference (r2 and r3 sheets) into the database, launch run() from reference_filler.py file with the correct xlsm file nearby.
(You have to fill in the line 4 its name)