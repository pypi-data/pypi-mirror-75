# zbpy: official Zetabase client for Python 

The `zbpy` package provides a pure-Python Zetabase client and reference implementation of the Zetabase protocol, along with integrations for commonly used Python tools like Numpy/Pandas.

For more complete documentation, please refer to the main documentation section on the Zetabase website:

1. [Python quick start](https://zetabase.io/docs/#/pysetup)
2. [Python library reference](https://zetabase.io/static/docs-python/html/zbpy.html)
3. [Zetabase main documentation](https://zetabase.io/docs/#/)

## Prerequisites and external dependencies 

1. Python 3.6 or higher 
2. `gcc` or equivalent compiler (except Windows)
3. `gmp` library and headers (except Windows)

**Note**: a C compiler is not required when running `zbpy` on Windows. However, all requests made with ECDSA on Windows will be 
slightly slower when compared to other operating systems due to limitations of the platform. We recommend that heavy workloads
on Windows use JWT authentication when possible.

### Installing gmp (if needed)

1. OSX: `brew install gmp`
2. Ubuntu: `apt-get install libgmp3-dev`
3. Centos: `yum install gmp gmp-devel gmp-status`

Not required for Windows OS.

## Installation 
Run the following to install: 
```bash
pip3 install zbpy 
```

You may get an error indicating you need to install `cython`. In this case, simply run the following: 

```bash
pip3 install cython
``` 

And then re-run `pip3 install zbpy`.

## Creating an account 
If you do not have an account already you can easily create one through the Python client module. If you are using Juptyer notebooks, simply use the Jupyter account creation magic: 
```python
from zbpy import client 

%createaccount
```
The `%createaccount` magic will run you through an interactive wizard to create a new Zetabase user identity.

Otherwise, run the following code within the Python interactive shell to go through the same wizard
on the console: 

```python
from zbpy import util 

util.new_account_interactive()
```

Answer the prompts that will appear, and if the account is created successfully, three files will be created in your current directory. These are:
1. your private key;
2. your public key; and 
3. an identity file containing both keys along with your user ID.

## Test your installation 
To test that everything has installed correctly run the `test_zbpy` method from `zbpy.util` in Jupyter or the Python interactive shell: 
```python
from zbpy import util 

util.test_zbpy()
```

## Library usage 

### Creating a Zetabase client

When you created your identity, you were assigned a user id (a uuid, or random-looking string of letters and numbers). use this to instantiate your client.
 
```python
from zbpy import client 

zb_client = client.ZetabaseClient('YOUR USER ID')
```

## Connecting your client to Zetabase
### To use JWT authentication for all requests

When you created your identity, you created a "name" (handle) and administrator password. You can use these instead of your public and private keys if your tables are configured to allow it.

```python
zb.login_jwt('YOUR USERNAME', 'YOUR PASSWORD')
```

### To use ECDSA authentication for all requests
```python
zb_client.setup_ecdsa('FILEPATH TO PRIVATE KEY', 'FILEPATH TO PUBLIC KEY')
```

### Creating Tables

#### With Pandas

**Note**: There are two methods to create tables using zbpy. There are two optional parameters with both of the methods: 

1. `perms`: used to specify the permissions of the table (can also be added to an existing table using the `add_perm()` method)
2.  `allow_jwt`: if true, allows data to be put into the table using JWT authentication.  

If you are creating a table to hold a Pandas dataframe, the easiest way is to use the following function. This will create a table with indexed fields that match the names and types of the columns of your dataframe, and then it inserts your dataframe into the given table using some given "dataframe key" to identify it.
```python
zb_client.put_dataframe_new_table('TABLE ID', YOUR DATAFRAME, 'YOUR DF KEY')
```

If you would like a subset of the DataFrame's columns to be turned into indexed fields in the table use the 'specify_fields' parameter. 

```python
zb_client.put_dataframe_new_table('Table ID', YOUR DATAFRAME, 'YOUR DF KEY', specify_fields=['age', 'height'])
```

This field can be `[]` to not index any fields (i.e. if you have no intention of querying the table based on field values).

#### Custom tables (no Pandas)

In this case, we create a new table by passing in a set of zero or more fields to index and some given list of permissions, e.g.: 

```python 
from zbpy.indexedfieldentity import IndexedField
from zbpy import zb_protocol_pb2 as zb

index_age = IndexedField('age', zb.QueryOrdering.INTEGRAL_NUMBERS)
index_height = IndexedField('height', zb.QueryOrdering.REAL_NUMBERS)

zb_client.create_table('TABLE ID', zb.TableDataFormat.JSON, [index_age, index_height], [OPTIONAL PERMS], allow_jwt=True)
```

### Creating permissions and adding them to existing tables

```python
from zbpy.permissionentity import PermEntry
from zbpy import zb_protocol_pb2 as zb

perm = PermEntry(zb.PermissionLevel.READ, zb.PermissionAudienceType.PUBLIC, '')

zb_client.add_permission('TABLE ID', perm)
```

### Retrieving data and Pagination
When using the functions `list_keys()`, `get()`, and `query()`, the data is returned as a `GetPages` object. A `GetPages` objects can be iterated over or turned into a Pandas dataframes using the `to_dataframe()` method (both demonstrated below).

#### Retrieving keys from table
```python
list_keys = zb_client.list_keys('TABLE ID')
keys = [key for key in list_keys]
```

#### Retrieving data by key 
```python
result = zb_client.get('TABLE ID', ['KEY 1', 'KEY 2', 'KEY 3', 'etc.'])

dataframe = result.to_dataframe()
```

### Retrieving data as objects

The `return_pretty` method will pre-parse JSON objects for you.

```python
result = zb_client.get('TABLE ID', ['KEY 1', 'KEY 2', 'KEY 3', 'etc.'])
result.return_pretty()

for i in result:
    print(i)
```

#### Retrieving data by query 

To query data from Zetabase, we have a Python-based DSL ("domain-specific language") that allows you to express queries. The idea is to use `Field` objects to represent indexed fields and to build queries based on them. We can then use comparison operators on each field to create a subquery, and we can combine subquery with logical operators. See [the documentation for more information](https://zetabase.io/docs/#/keyvalue).

The example below assumes that a table exists with indexed fields 'age' and 'name'. Queries use '&' and '|' for 'and' and 'or' operators -- for that reason, use parentheses to avoid operator precedence issues. 

```python
from zbpy import queries

age = Field('age')
name = Field('name')

query = ((age == 19) | ((age > 25) & (age <= 27))) & (name == 'Austin')
result = zb_client.query('TABLE ID', query)

for i in result:
    print(i)
```

### Inserting data 

To insert a Pandas dataframe into an existing table, use the `put_dataframe()` method. Each row of the dataframe will be inserted as its own object, the collection of which is identified by a key: the `df_key` parameter. Dataframes can be appended to one another by simply storing a new dataframe using the same `df_key` on the same table as an existing dataframe.

```python
zb_client.put_dataframe('TABLE ID', YOUR DATAFRAME, 'YOUR DF KEY')
```

To insert data without Pandas, we can use `put_data` for a single object, or `put_multi` for a list of objects:

```python
zb_client.put_data('TABLE ID', 'DATA KEY', DATA AS BYTES)
zb_client.put_multi('TABLE ID', ['KEY 1', 'KEY 2', 'KEY 3', 'etc.'], [DATA1 AS BYTES, DATA2 AS BYTES, etc.])
```

#### Notes

1. For performance reasons, to insert multiple pieces of data, it is suggested to use the `put_multi()` method.
2. When possible, if storing large quantities of data, it is faster to use JWT over ECDSA if possible. 
