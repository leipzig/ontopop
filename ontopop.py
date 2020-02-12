import json
import sys
import os
import subprocess
import shlex
import time
from secrets import api
from eutils import Client
import csv


showUids=False
ec = Client(api_key=api.apikey)

with open('ontologies.jsonld','r') as json_file:
    onts = json.load(json_file)
    with open('citations.json','r') as cite_file:
        cits = json.load(cite_file)
        with open('newcits.json','w') as newcites:
            for f in onts['ontologies']:
                if f['title'] in cits:
                    pass
                else:
                    term="({})".format(f['title'].replace(" ", "+"))

                    try:
                        a = ec.esearch(db='pubmed',term=term)
                    except (TimeoutError, TypeError, NameError):
                        time.sleep(5)
                    cits[f['title']]=a.count
                    if showUids:
                        print("{}\t{}\t{}".format(f['title'],a.count,a.ids))
                    else:
                        print("{}\t{}".format(f['title'],a.count))
                    json.dump(cits, newcites)


# implement

with open("citations.json") as file:
    data = json.load(file)
    with open("citations.csv", "w") as file:
        csv_file = csv.writer(file)
        for item in data.keys():
            csv_file.writerow([item,data[item]])