import mysql.connector

from datetime import datetime
from pytz import timezone
from configparser import SafeConfigParser

LOCATION_ID = {
    'POP': 1,
    'FRE': 2,
    'UPW': 3
}

class DatabaseConnector:
    INSERT_OCCUPANCY_DATA = (
        "INSERT INTO occupancy_data"
        "(GymId, Count, LastUpdated, Checked)"
        "VALUES"
        "(%(gym_id)s, %(count)s, %(last_updated)s, %(checked)s)"
    )
    TIMEZONE = timezone('US/Pacific')

    def __init__(self, config):
        if config is None:
            raise Exception("No config given to database connector")

        parser = SafeConfigParser()
        parser.read(config)

        self.cnx = mysql.connector.connect(
            user=parser.get('mysql_connection', 'user'),
            password=parser.get('mysql_connection', 'password'),
            host=parser.get('mysql_connection', 'host'),
            database=parser.get('mysql_connection', 'database')
        )
        
        self.TIMEZONE = timezone(parser.get('other', 'timezone'))
    
    def __del__(self):
        if hasattr(self, 'cnx'):
            self.cnx.close()
    
    def post_data(self, data): # TODO: validate data
        if data is None:
            return
        
        cursor = self.cnx.cursor()
        today = datetime.now(self.TIMEZONE)

        occupancy_data = {
            'gym_id': LOCATION_ID[data['location']],
            'count': data['count'],
            'last_updated': data['last_updated'] or today,
            'checked': today
        }

        cursor.execute(self.INSERT_OCCUPANCY_DATA, occupancy_data)
        self.cnx.commit()

        cursor.close()

if __name__ == "__main__":
    # Test method
    dbc = DatabaseConnector(None)
    dbc.post_data(None)