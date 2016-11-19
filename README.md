# GetAirport
## Tutorial
* Start MySQL service first.
* Install some packages below:

```
pip install simplejson
pip install requests
```

* Download and install Connector/Python that suit your system: [Download Connector/Python](http://dev.mysql.com/downloads/connector/python/)
* And then run the main process with command:

```
python main.py
```
## Modules
* **ConnectDB**: connect to database, with some method to interactive with table in database.
* **ImportCSV**: import CSV file to table name 'ticket', all CSV files should put into csv folder.
* **GetAirport**: request data from skyscanner API and import it to table name 'airport'