from oc_scraper import OccupancyScraper

CONNECTION_URL = "https://portal.rockgympro.com/portal/public/314b60a77a6eada788f8cd7046931fc5/occupancy?&iframeid=occupancyCounter&fId=1967"


if __name__ == "__main__":
    print("Starting data update...")

    for location in ('POP', 'FRE', 'UPW'):
        scraper = OccupancyScraper(CONNECTION_URL, location)
        scraper.get_occupancy()
        scraper.print_data()
    
    print("Data update: Done.")