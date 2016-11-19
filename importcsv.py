"""Module ImportCSV: import CSV file to database"""
import os
from connectdb import ConnectDB


class ImportCSV(object):
    """Import CSV file to database"""
    _user = _password = _database = _db = None

    def __init__(self, user, password, database):
        self._user = user
        self._password = password
        self._database = database
        self._db = ConnectDB(self._user, self._password, self._database)
        self._db.open()

    def create_csv_table(self, table_name):
        """Create table to import CSV file"""
        query = """CREATE TABLE {} (
        id INT NOT NULL UNIQUE AUTO_INCREMENT,
        out_carrier VARCHAR(10) NOT NULL,
        in_carrier VARCHAR(10) NOT NULL,
        departure VARCHAR(3) NOT NULL,
        arrival VARCHAR(3) NOT NULL,
        out_start_date DATE NOT NULL,
        out_end_date DATE NOT NULL,
        out_start_time TIME NOT NULL,
        out_end_time TIME NOT NULL,
        in_start_date DATE NOT NULL,
        in_end_date DATE NOT NULL,
        in_start_time TIME NOT NULL,
        in_end_time TIME NOT NULL,
        out_agent VARCHAR(100) NOT NULL,
        in_agent VARCHAR(100) NOT NULL,
        out_price DECIMAL(10,1) NOT NULL,
        in_price DECIMAL(10,1) NOT NULL,
        total_price DECIMAL(10,1) NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_unicode_ci;"""
        self._db.create_table(query, table_name)

    def import_csv(self, path, table_name):
        """Import CSV file to database"""
        query = """LOAD DATA INFILE '{}'
        INTO TABLE {}
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (@dummy, out_carrier, in_carrier, departure, arrival,
        @out_start_date, @out_end_date, @out_start_time, @out_end_time,
        @in_start_date, @in_end_date, @in_start_time, @in_end_time,
        out_agent, in_agent, @out_price, @in_price, @total_price)
        SET out_start_date = STR_TO_DATE(@out_start_date, '%Y-%m-%d'),
        out_end_date = STR_TO_DATE(@out_end_date, '%Y-%m-%d'),
        out_start_time = STR_TO_DATE(@out_start_time, '%H:%i'),
        out_end_time = STR_TO_DATE(@out_end_time, '%H:%i'),
        in_start_date = STR_TO_DATE(@in_start_date, '%Y-%m-%d'),
        in_end_date = STR_TO_DATE(@in_end_date, '%Y-%m-%d'),
        in_start_time = STR_TO_DATE(@in_start_time, '%H:%i'),
        in_end_time = STR_TO_DATE(@in_end_time, '%H:%i'),
        out_price = CAST(@out_price AS DECIMAL(10,2)),
        in_price = CAST(@in_price AS DECIMAL(10,2)),
        total_price = CAST(@total_price AS DECIMAL(10,2));"""

        current_dir = os.getcwd().replace('\\', '/')
        csv_dir = os.listdir('.' + path)
        for csv_file in csv_dir:
            if csv_file.endswith('.csv') or csv_file.endswith('.CSV'):
                print "Importing '{}'...".format(csv_file)
                self._db.insert(query.format(
                    current_dir + path + csv_file, table_name), table_name)
        self._db.close()
