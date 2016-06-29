## General Information

#### Programming Languages and Technologies
Limit Manual is a Flask Application using a Postgres database.
This means two major categories of technology used in this project are Python-related and Database-related.
There are also things that come into play because this is a web application, so you can assume at least HTML and CSS are used.
Broken down into three categories, the components of this project are as follows.

##### Python
The Python version this is being primarily developed with is `3.4.3`.

The following packages are at the core of the project at this current point.

- [Flask]: The web app microframework at the core of the project.
- [Jinja2]: A templating engine used to create out Dynamic HTML.
- [psycopg2]: A simple DB2-compliant database access package for Postgres.

Additionally, at this time *Flask-Assets* and *pyScss* are also in use to compile SCSS, however they may be abandoned at some point in favor of using plain CSS, at least from the application's point of view (compiling the SCSS manually).

All of these packages can be installed via pip. Version information is listed in requirements.txt in the project's root directory.

[flask]: http://flask.pocoo.org
[jinja2]: http://jinja2.pocoo.org
[psycopg2]: http://initd.org/psycopg/

##### Web
The core skills for web skills for this project are HTML and CSS, but in order to improve the ease and speed of development plain HTML and CSS are not used.

The [Jinja2] templating system is used to extend the functionality of HTML. Through this partial templates and template extension and inclusion are used to reduce the amount of markup that needs to be rewritten in multiple places. However, the major benefit of this is to allow variables and loops in our markup. Extensive use is made of this feature, but at the end of the day anyone with a working knowledge of HTML should be able to read and understand the extended markup syntax.

CSS is currently written as [SCSS] and compiled on application start or when a watched file is changed. This is done using the packages listed in the python section.

[scss]: http://sass-lang.com/documentation/file.SASS_REFERENCE.html

##### Postgres
Postgres itself is the only requirement here. The specific version in use is `9.5.3`.

#### Design Philosophy

##### Clarity of Code
To the greatest extent possible, everything a reader needs to know about something should be able to be found in the same file. Emphasis should be placed on good variable naming convention, but due to the multiple-part nature of this project further care needs to be taken to ensure readability and understandability. This manifests in two major forms: good object design and clear query writing.

Objects created to be passed to the templates are written to structure the data in a more easily-understood way than it can be stored in the database in. It is important that the naming conventions and data types make sense here without referencing the python code or database schema.

Similarly, good queries (on the python side through psycopg2) should request the specific parameters they are looking for in the query. This means do not use `SELECT prop1, prop2, ..., propN FROM table` over `SELECT * FROM table` in all cases. This is especially important where you do not need every property in the table, but improves readability even when you do. Additionally, a dependency on the names of the properties is much more meaningful than one on the order the properties were specified in a `CREATE TABLE ... ;` statement.
