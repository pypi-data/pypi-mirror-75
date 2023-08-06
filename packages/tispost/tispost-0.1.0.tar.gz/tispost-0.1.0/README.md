Tispost
=======

[![Latest PyPI package version](https://badge.fury.io/py/tispost.svg)](https://pypi.org/project/tispost)

Key Features
------------

- Supports asyncio.

Getting started
---------------

`tispost` allows you to quickly use postgres as a nosql database.

Example
```python
# import
from tispost import Server, Collection, Session

# create connection
server = Server(dbname=database, user=postgres, password=postgres, host=dlnxiot001)

# connect
server.connect()

# get session
session = await server.session()

# create new collection
session.create("collection")

# delete a collection
session.delete("collection")

# get a collection
collection = session.collection("collection")

# insert document into a collection:
collection.save({'item':'value'...})

# get document from collection with id
collection.get(id="930f43ed-7bb5-46b9-a6d2-45c345ec959e")

# query items
collection.query(filter={'key':'value'}, offset=0, limit=50)
```

Installation
------------
It's very simple to install tispost:
```sh
pip install tispost
```

Notes
-----

 - The db user must have the create/drop table permission


Requirements
------------

-   Python >= 3.6
-   [aiopg](https://pypi.python.org/pypi/aiopg)

License
-------

`tispost` is offered under the Apache 2 license.

Source code
-----------

The latest developer version is available in a GitHub repository:
<https://github.com/aiselis/tispost>
