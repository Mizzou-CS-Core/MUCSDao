# mucs_database

This project is a set of wrappers and abstractions for creating and interacting with a SQLite3 database as it relates to a MUCSv2 course instance
Models and accessors are provided using the Peewee ORM library.

Nearly all projects in the MUCSv2 family of applications use this library.

## Set Up as Pip Library

For best results, you should use `piptools`. Add the GitHub Repo as an HTTPS URL along with `#egg-info=database` to a `requirements.in`. Then compile it using `pip-compile requirements.in`. This will generate a `requirements.txt` with the appropriate URL for downloading. 

## Usage

Prior to using accessors from the library, you will need to initialize the database by calling `mucs_database.init.initialize_database`. You will need to provide a path to your database in your MUCSv2 course instance, as well as the MUCSv2 instance code. If there is not a `.db` at the provided path, one will be created. This call will ensure that the DB matches the necessary MUCSv2 DB schema. 

Once the DB is initialized, calls to the various model accessors will be available. Each model has its own accessor methods; for example `GradingGroup` is exposed as `mucs_database.grading_group.accessors`. The model class is also exposed as `mucs_database.grading_group.model`. 




