# mdbh - A MongoDB helper collection to use with Sacred and Omniboard.

This repository holds mostly two purposes: 

First, it provides a Python module together with some CLI scripts to ease the 
usage of MongoDB together with [Sacred](https://github.com/IDSIA/sacred)
and [Omniboard](https://github.com/vivekratnavel/omniboard), 
filling a low-level gap. 
Whereas [Omniboard](https://github.com/vivekratnavel/omniboard) is well suited 
to  quickly explore data and compare Sacred experiments, it is not meant for
more complex data visualization and low-level database access.
This can for example be useful when preparing print-quality plots.

Second, it provides a [Wiki](https://gitlab.com/MaxSchambach/mdbh/-/wikis/home)
to collect guidelines on how to use Sacred with MongoDB, Omniboard and mdbh.
In particular, a multi-user, multi-database setup with password restriction and controlled
read/write access to multiple databases is provided. This Wiki is not meant
to be exhaustive, but shall get you started with your own setup.

>**Note:** This is still somewhat under development.


[[_TOC_]]


## Installation

Install via PyPi using pip 
```bash
pip install mdbh
```

## Setup
The MongoDB instance configuration is done using one (or multiple) configuration
files which simply store the server IP, port and possible the username, password
and authentication methods and database names. 
See the `examples` folder for an example.

By default, it is assumed the this configuration
file can be found under
```bash 
~/.mongo.conf
```

This config file is central to the use of mdbh. As this config file might
contain userdata, make sure only the current user has read access to it,
e.g. run
```bash 
chmod 400 .mongo.conf
```

## Use Cases
Some use cases of mdbh are as follows:


### MongoDB URI creation
Often times, services or modules (such as the MongoObserver in Sacred)
need a URI to connect to the MongoDB following the 
[official format specification](https://docs.mongodb.com/manual/reference/connection-string/).
However, this often results in boilerplate code and, in the case of
user authentification, security risks as the username and/or password have
to be specified in the corresponding code.

To this end, mdbh provides the [get_uri](https://gitlab.com/MaxSchambach/mdbh/-/blob/master/mdbh/core.py#L27) 
function which creates the connection URI based on the `.mongo.conf` file
and a specific database name.

### Sacred Experiment query
To query and manipulate data that has been logged to the MongoDB instance
via Sacred, mdbh provides several functions, the most comprehensive one being
[get_df_full](https://gitlab.com/MaxSchambach/mdbh/-/blob/master/mdbh/core.py#L190)
which returns a Pandas `DataFrame` object created from the specified 
Sacred database. It convenently combines configuration information
as well as logged metrics of all experiments in the specified database.
Using the `DataFrame`, complex data aggregation and/or plotting
(e.g. via [Seaborn](https://seaborn.pydata.org/)) is quite comfortable.

### MongoDB Setup and Omniboard
See the corresponding 
[Omniboard Wiki entry](https://gitlab.com/MaxSchambach/mdbh/-/wikis/omniboard-setup) 
to see how mbdh can ease the use with Omniboard.

See the corresponding 
[MongoDB Wiki entry](https://gitlab.com/MaxSchambach/mdbh/-/wikis/mongodb-setup) 
to see how to properly setup a MobgoDB instance.