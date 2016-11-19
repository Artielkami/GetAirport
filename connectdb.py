"""Module ConnectDB: connecting to database"""
import mysql.connector
from mysql.connector import errorcode


class ConnectDB(object):
    """Connect to mysql database"""
    _connection = _session = _config = _user = _password = _database = None

    def __init__(self, user, password, database):
        self._user = user
        self._password = password
        self._database = database
        self._config = {
            'user': self._user,
            'password': self._password,
            'host': '127.0.0.1',
            'database': self._database,
            'raise_on_warnings': True,
        }

    def open(self):
        """Open connection to database"""
        try:
            cnx = mysql.connector.connect(**self._config)
            print "Connecting to database '{}' successfully.".format(self._database)
            self._connection = cnx
            self._session = cnx.cursor()
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "wrong username or password"
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist"
            else:
                print error

    def close(self):
        """Close connection to database"""
        self._session.close()
        self._connection.close()
        print "Closing connection to database '{}' successfully.".format(self._database)

    def create_table(self, query, table_name):
        """Create table in database"""
        try:
            print "Creating table '{}'...".format(table_name)
            self._session.execute(query.format(table_name))
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print "Table '{}' already exist.".format(table_name)
            else:
                print error.msg
        else:
            print "Table '{}' was created successfully.".format(table_name)

    def drop_table(self, table_name):
        """Drop table in database"""
        query = """DROP TABLE IF EXISTS {}"""
        try:
            print "Dropping table '{}'...".format(table_name)
            self._session.execute(query.format(table_name))
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_TABLE_ERROR:
                print "Table '{}' does not exist.".format(table_name)
            else:
                print error.msg
        else:
            print "Dropping table '{}' successfully.".format(table_name)

    def insert(self, query, table_name):
        """Insert data to database"""
        try:
            print "Inserting to table '{}'...".format(table_name)
            self._session.execute(query)
            self._connection.commit()
        except mysql.connector.Error as error:
            if error == errorcode.ER_BAD_TABLE_ERROR:
                print "Table '{}' does not exist."
            else:
                print error.msg
        else:
            print "Inserting to table '{}' successfully.".format(table_name)
