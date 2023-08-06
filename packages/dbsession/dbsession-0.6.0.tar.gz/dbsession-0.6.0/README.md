# dbsession
The python postgreSQL ORM 

## introduction

DBSession gives simplicity, flexibility and order to the abstraction of database tables into python objects. Right now it's only supporting postgreSQL with psycopg2

## Usage

Assuming we have a table named `A` with the following estructure

```
 id | name  
----+-------
  1 | Paul  
  2 | George  
```

Create an archive `A.py` and create a class for the database abstraction `A` that inherits from `DatabaseObject`. The attribute `_TABLE_NAME` is the database table actual name

```py
from DBSession import DatabaseObject

TABLE_NAME = 'A'

class _A(DatabaseObject):

    _TABLE_NAME = TABLE_NAME

    def __init__(self, row):
        super().__init__(row)

wrapper = _A
```

Now implement every function associated with this table in the same file. Every function receives the params that goes in the query, and returns a tuple of four items:
- query (str): The actual query
- values (Tuple): The params to be replaced into the query
- wrapper (Object): The class that represent the table
- many (bool): Whether the query will return one or many instances

```py

def find_by_id(a_id):
    
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE id = %s
    """

    values = (a_id, )

    return query, values, wrapper, False

def get_all():

	query = f"""
        SELECT *
        FROM {TABLE_NAME}
    """

    values = ()

    return query, values, wrapper, True
```

Create a connection to the database using the `DBConnection` class. It receives the pool instance from psycopg2.

```py
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    MINIMUM_CONNECTION,
    MAXIMUM_CONNECTION,
    user=POSTGRES_USER, 
    password=POSTGRES_PASSWORD, 
    host=POSTGRES_HOST, 
    port=POSTGRES_PORT, 
    database=POSTGRES_DB)


db_connection = DBConnection(connection_pool)
```

Finally, in the main code. To execute the query just create a `DBSession` instance, and call the `A` module functions by using de `query` function

```py
import A


db_session = db_connection.get_session()
a_1 = db_session.query(A.find_by_id, 1)
print(a_1)
# (1, 'Paul')

all_a = db_session.query(A.get_all)
print(all_a)
# [(1, 'Paul'), (2, 'George')]
```