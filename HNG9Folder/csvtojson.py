import csv
import json
import hashlib
from pathlib import Path
import os

#creating json files from csv file provided in argument
#open the csv file
inFile = input('Enter a file name [do not include file type]: ')
csvfile = open(inFile+'.csv','r')
csvreader = csv.DictReader(csvfile)

count = 0
for row in csvreader:
    row1 = json.dumps(row)
    json_object = json.loads(row1)
    out = json.dumps(json_object, indent=2)
    #save json file
    jsonoutput = open('./nft'+'inFile'+'.json','w')
    jsonoutput.write(out)
    count +=1

os.remove('NFT0.json')
jsonoutput.close()

#hash calulator - calulating sha256 of each json file and out a csv file
input_directory = Path.cwd()
# glob = specific folder
# rglob = including sub floders
files = list(input_directory.rglob("*.json"))
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