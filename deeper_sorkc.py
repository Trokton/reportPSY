import csv
import re

# This will store a list of dictionaries from the CSV
dict_list = []

# Open and read the CSV file
with open('sorkc_2.csv', 'r') as f:
    csv_reader = csv.DictReader(f)
    # Append each row dictionary to dict_list
    for row in csv_reader:
        dict_list.append(row)

set_emotionen = set()
set_physis = set()
set_kognition = set()

# Iterate over each dictionary in the list
for each_dict in dict_list:

    id = each_dict['Chiffre']
    icd10 = each_dict['Diagnose']
    kognitionen = each_dict['Kognitionen'].split('"')
    emotionen = each_dict['Emotionen'].split(',')
    physis = each_dict['Physiologie'].split(',')
    Sbsp = each_dict['Sbsp']

    _kognition = []
    _emotion = []
    _physis = []

    for k in kognitionen:
        if re.search(r'ich|mir|mich', k, re.IGNORECASE):
            _kognition.append(k)
            set_kognition.add(k)

    for e in emotionen:
        _emotion.append(e)
        set_emotionen.add(e)

    for p in physis:
        _physis.append(p)
        set_physis.add(p)



with open('kognition.txt', 'w') as f:
    for k in set_kognition:
        f.write(k + '\n')


with open('physis.txt', 'w') as f:
    for p in set_physis:
        f.write(p + '\n')


with open('emotion.txt', 'w') as f:
    for e in set_emotionen:
        f.write(e + '\n')