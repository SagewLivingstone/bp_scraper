import re
import requests
from bs4 import BeautifulSoup

"""
Class for scraping occupancy data from a rockgympro iframe
"""
class OccupancyScraper:
    PATTERN_BASE = r"'%s' : {.*?\n *?'capacity' : ([0-9]{1,4}).*?\n *?'count' : ([0-9]{1,4}).*?\n.*?\n *?'lastUpdate' : .*?\(([0-9]{1,2}:[0-9]{2} [A-Z]{2})\)"

    def __init__(self, URL, location):
        self.url = URL
        self.location = location

    def get_occupancy(self):
        # Retrieve page
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        # Search patterns
        data_script_pattern = re.compile(r"(var data = {)", re.MULTILINE)
        self.pattern = self.PATTERN_BASE % self.location

        # Search for script tag containing the data pattern
        script = soup.find("script", text=data_script_pattern)
        self.parse_script(script)
    
    def parse_script(self, script):
        if script is None:
            return

        data_pattern = re.compile(self.pattern, re.MULTILINE | re.DOTALL)
        match = data_pattern.search(script.text)
        if (match):
            self.fill_data(match)
    
    def fill_data(self, match_data):
        if match_data is None:
            return

        self.data = {
            'capacity': match_data.group(1),
            'count': match_data.group(2),
            'last_updated_string': match_data.group(3)
        }

    def print_data(self):
        if self.data is None:
            return
        
        print(self.location, ':', self.data['count'], '/', self.data['capacity'], '- Last Updated:', self.data['last_updated_string'])
        
