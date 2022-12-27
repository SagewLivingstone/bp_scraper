import requests
import re
from bs4 import BeautifulSoup

url = "https://portal.rockgympro.com/portal/public/314b60a77a6eada788f8cd7046931fc5/occupancy?&iframeid=occupancyCounter&fId=1967"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

data_script_pattern = re.compile(r"(var data = {)", re.MULTILINE | re.DOTALL)

script = soup.find("script", text=data_script_pattern)

pattern = r"'POP' : {.*\n *'capacity' : ([0-9]{1,4}).*\n *'count' : ([0-9]{1,4}).*\n.*\n *'lastUpdate' : .*\(([0-9]{1,2}:[0-9]{2} [A-Z]{2})\)"

if (script):
    poplar_pattern = re.compile(pattern, re.MULTILINE | re.DOTALL)
    match = poplar_pattern.search(script.text)
    if (match):
        print('POP', match.group(1), match.group(2), match.group(3))

