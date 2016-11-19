"""Module GetAirport: get airport information through skyscanner API"""
import requests
import simplejson as json

from connectdb import ConnectDB


class GetAirport(object):
    """Get airport information through skyscanner API"""
    _url = _data = _response = _places = _db = None
    _airport_info = []

    def __init__(self, url):
        self._url = url
        self._db = ConnectDB('root', '', 'search')
        self._db.open()

    def request_api(self):
        """Get data from API in JSON format"""
        self._response = requests.get(self._url)
        self._response.encoding = 'utf-8'
        self._data = self._response.json()
        self._places = self._data['Places']
        if self._response.status_code == 200:
            print "Request successfully."
        return self._data

    def filter_data(self):
        """Filter necessary data from API"""
        for info in self._places:
            if info.has_key('IataCode'):
                del info['SkyscannerCode']
                del info['PlaceId']
                del info['CityId']
                del info['Type']
                self._airport_info.append(info)
        return self._airport_info

    def create_json_table(self, table_name):
        """Create table to import JSON data"""
        query = """CREATE TABLE {} (
            iata_code VARCHAR(3) NOT NULL UNIQUE,
            name VARCHAR(50) NOT NULL,
            city_name VARCHAR(50) NOT NULL,
            country_name VARCHAR(50) NOT NULL,
            PRIMARY KEY (iata_code)
        ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_unicode_ci;"""
        self._db.create_table(query, table_name)

    def import_json(self, table_name):
        """Import JSON to database"""
        query = "INSERT INTO {} ".format(table_name)
        for info in self._airport_info:
            value = """VALUES ("{}", "{}", "{}", "{}")
            ON DUPLICATE KEY UPDATE iata_code = iata_code;""".format(
                info['IataCode'], info['Name'], info['CityName'], info['CountryName'])
            self._db.insert(query + value, table_name)
        self._db.close()

    def write_file(self, data_str, file_name):
        """Open and write data to file with extension json"""
        file_json = open('./json/' + file_name, 'w+')
        file_json.write(data_str)
        file_json.close()
        print "Write data to '{}' successfully.".format(file_name)

    def json_str(self, data_json):
        """Convert JSON to STRING"""
        return json.dumps(data_json, indent=4 * ' ')

    def test(self):
        """Test filter data from API"""
        data = self.request_api()
        self.write_file(self.json_str(data), 'data.json')
        filter_data = self.filter_data()
        self.write_file(self.json_str(filter_data), 'filter.json')
