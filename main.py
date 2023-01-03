from occupancy_scraper import OccupancyScraper
from dbc import DatabaseConnector

CONNECTION_URL = "https://portal.rockgympro.com/portal/public/314b60a77a6eada788f8cd7046931fc5/occupancy?&iframeid=occupancyCounter&fId=1967"


if __name__ == "__main__":
    print("Starting data update...")

    dbc = DatabaseConnector('dbconfig.ini')

    for location in ('POP', 'FRE', 'UPW'):
        scraper = OccupancyScraper(CONNECTION_URL, location)
        scraper.get_occupancy()
        scraper.print_data()
        dbc.post_data(scraper.data)
    
    print("Data update: Done.")