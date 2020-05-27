#!/usr/bin/env python3
import re
from bs4 import BeautifulSoup
import csv
import sys
import json

#url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
#page = requests.get(url)
#html = page.content

def print_json(obj):
    json_object = json.loads(json.dumps(obj))
    print(json.dumps(json_object, indent=2))

def parse_line(entries):
    line = []
    for entry in entries:
        result1 = re.sub("(?<=-)\n(?=[A-Z])", "", entry.text)
        result2 = re.sub("(?<=[a-z])[\-\u00ad](?=[a-z])", "", result1)
        result3 = re.sub("(?<=[a-z]) ?\n(?=[a-zA-Z0-9])", " ", result2)
        line.append(result3)
    return line

def parse_table(html):
    soup = BeautifulSoup(html, features="lxml")
    htmltable = soup.find("table")
    if htmltable == None:
        print("Couldn't parse link " + str(line.strip("\n\r")))
        return {}
    table = {}
    table['tabledata'] = []
    for table_row in htmltable.findAll('tr'):
        entries = table_row.findAll('td')
        if entries == []:
            entries = table_row.findAll('th')
            header = parse_line(entries)
            table['header'] = header
            continue
        table['tabledata'].append(parse_line(entries))
    return(table)

def parse_date(html):
    result = {}
    stand = re.findall(r"Stand: .*</p>", html)
    if isinstance(stand, str):
        result['Day'] = re.findall("(?<= )[0-9]+(?=\.)", stand)[0]
        result['Month'] = re.findall("(?<=\.)[0-9]+(?=\.)", stand)[0]
        result['Year'] = re.findall("(?<=\.)[0-9]{4}", stand)[0]
        if not re.findall("[0-9]+:[0-9]{2}(?= Uhr)", stand):
            result['Time'] = "none"
        else:
            result['Time'] = re.findall("[0-9]+:[0-9]{2}(?= Uhr)", stand)[0]
    elif len(stand) >= 1:
        stand = stand[0]
        result['Day'] = re.findall("(?<= )[0-9]+(?=\.)", stand)[0]
        result['Month'] = re.findall("(?<=\.)[0-9]+(?=\.)", stand)[0]
        result['Year'] = re.findall("(?<=\.)[0-9]{4}", stand)[0]
        if not re.findall("[0-9]+:[0-9]{2}(?= Uhr)", stand):
            result['Time'] = "none"
        else:
            result['Time'] = re.findall("[0-9]+:[0-9]{2}(?= Uhr)", stand)[0]
    if len(stand) == 0:
        return None
    return (result)

def get_entry(fname):
    with open(fname,  'r') as f:
        html = f.read()
    return { 'time' : parse_date(html), 'table' : parse_table(html) }

def date_matches(a, b):
    if b['time'] == None or a['time'] == None:
        return False
    elif (a['time']['Day'] == b['time']['Day'] \
        and a['time']['Month'] == b['time']['Month'] \
        and a['time']['Year'] == b['time']['Year'] \
        and a['time']['Time'] == b['time']['Time']):
        return True
    else:
        return False

inputfile = sys.argv[1]

line = ""

with open(inputfile, 'r') as f:
    lines = f.readlines()
    entries = []
    for line in lines:
        if line.strip('\n\r') == "":
            break
        entry = get_entry(line.strip('\n\r'))
        if (len(entries) == 0) or (len(entries) == 1):
            entries.append(entry)
        elif not date_matches(entry, entries[-1]):
            entries.append(entry)
    with open ("output.json", "w") as f:
        json.dump(entries, f)
#    for entry in entries:
#        print_json(entry['time'])
#    print("Total entries: " + str(len(entries)))




#writer = csv.writer(sys.stdout)
#writer.writerows(output_rows)

