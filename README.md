# GetAirport
## Tutorial
Start MySQL service first.
And then run the main process with command:
```
python main.py
```
## Modules
* **ConnectDB**: connect to database, with some method to interactive with table in database.
* **ImportCSV**: import CSV file to table name 'ticket', all CSV files should put into csv folder.
* **GetAirport**: request data from skyscanner API and import it to table name 'airport'