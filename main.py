"""Module Main: process all task"""
from connectdb import ConnectDB
from getairport import GetAirport
from importcsv import ImportCSV

if __name__ == "__main__":
    db = ConnectDB('root', '', 'search')
    db.open()
    db.drop_table('ticket')
    db.drop_table('airport')
    db.close()
    csv = ImportCSV('root', '', 'search')
    csv.create_csv_table('ticket')
    csv.import_csv('/csv/', 'ticket')
    url = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/JP/JPY/en-JP/VN/anywhere/anytime/anytime?apiKey=ho762281241371727571102068156668"
    air = GetAirport(url)
    air.request_api()
    air.filter_data()
    air.create_json_table('airport')
    air.import_json('airport')
