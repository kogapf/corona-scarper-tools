import requests
import re
from bs4 import BeautifulSoup
import csv
import sys

url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
page = requests.get(url)
html = page.content
soup = BeautifulSoup(html, features="lxml")
table = soup.find("table")

output_rows= []
for table_row in table.findAll('tr'):
    entries = table_row.findAll('td')
    if entries == []:
        entries = table_row.findAll('th')
    output_row = []
    for entry in entries:
        result1 = re.sub("(?<=-)\n(?=[A-Z])", "", entry.text)
        result2 = re.sub("(?<=[a-z])[\-\u00ad](?=[a-z])", "", result1)
        result3 = re.sub("(?<=[a-z]) ?\n(?=[a-zA-Z0-9])", " ", result2)
        output_row.append(result3)
    output_rows.append(output_row)

writer = csv.writer(sys.stdout)
writer.writerows(output_rows)
