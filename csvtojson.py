import csv
import json
import hashlib
from pathlib import Path
import os
import re

#creating json files from csv file provided in argument
#open the csv file
inFile = input('Enter a file name [do not include file type]: ')
csvfile = open(inFile+'.csv','r')
csvreader = csv.DictReader(csvfile)

nftname = []
seriesno = []
description = []
gender = []
id = []
anothername = []
attributes = []
count = 0
for row in csvreader:
    nftname.append(row['Filename'])
    seriesno.append(row['Series Number'])
    description.append(row['Description'])
    gender.append(row['Gender'])
    id.append(row['UUID'])
    anothername.append(row['Name'])
    attributes.append(row['Attributes'])

    json_object = {
                'format' : 'CHIP-0007',
                'filename' : nftname[count],
                'name':anothername[count],
                'description' : description[count],
                'sensitive_content' : False,
                'series_number' : int(seriesno[count]),
                'series_total' : 400,
                'attributes' :[ {
                    'trait_type' : 'Gender',
                    'value' : gender[count]
                }],
                'collection' : {
                    'name' : 'HNG9Zuri NFT Collection',
                    'id' : id[count],
                    "attributes": [{
                "type": "description",
                "value": "NFT Collection for zuri internship"}]
                },
    }  
    out = json.dumps(json_object, indent=4)
    jsonoutput = open(str(nftname[count])+'.json','w')
    jsonoutput.write(out)
    count +=1

jsonoutput.close()

#hash calulator - calulating sha256 of each json file and out a csv file
input_directory = Path.cwd()
# glob = specific folder
# rglob = including sub floders
files = list(input_directory.glob("*.json"))
list = list()

for path in files:
    with open(path,'rb') as opened_file:
        content = opened_file.read()
        sha256 = hashlib.sha256()
        sha256.update(content)
        sha = sha256.hexdigest()
        list.append(sha)
        list[0] = "Sha256"
        i = 0

        with open(inFile +'.csv','r') as read_obj,\
            open(inFile +'.output.csv','w',newline='') as write_obj:
            csv_reader = csv.reader(read_obj)
            csv_writer = csv.writer(write_obj)
            for row in csv_reader:
                if i>len(list)-1:
                    break
                row.append(list[i])
                csv_writer.writerow(row)
                i+=1

csvfile.close()
