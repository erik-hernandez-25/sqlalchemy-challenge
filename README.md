# sqlalchemy-challenge

This project uses SQLAlchemy to connect into a sqlite database and reflect the schema into classes that can be used for future queries using Jupyter Notebook for statistical analysis and then uses Flask to show the data through a Web Client.

It uses a database containing two tables: Measurements and Stations. It gives the precipitation volume and temperature taken in some days.

Using Flask, the first page show the APIs created that list the temperatures taken in the last year (using timedelta function), show the list of stations that provides measurements and three basic statistics of a given period of time Start Date till the last record or within a start and end date.

Give it a try...


