
Blueprint for cleaning data
- Audit the data
    Auditing validity is determining the constraints on a particular field and checking to ensure the field values adhere to those constraints
- Create a data cleaning plan
    - Identify causes
    - Define operations to correct the data
    - Test
- Execute the plan
- Manually correct


Data quality
- Validity: Conforms to a schema
- Accuracy: conforms to gold standard
- Completeness: contains all records
- Consistency: matches other known data
- Uniformity: units are the same


```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open("chicago.osm", "r")

# regular expression
    # \S+ is string ignoringn white space
    # \.? possibly end with a period
    # $ end of the string
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    

if __name__ == '__main__':
    audit()

```


```python
# Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
# The following things should be done:
# - check if the field "productionStartYear" contains a year
# - check if the year is in range 1886-2014
# - convert the value of the field to be just a year (not full datetime)
# - the rest of the fields and values should stay the same
# - if the value of the field is a valid year in the range as described above,
#   write that line to the output_good file
# - if the value of the field is not a valid year as described above, 
#   write that line to the output_bad file
# - discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
# - you should use the provided way of reading and writing data (DictReader and DictWriter)
#   They will take care of dealing with the header.

# You can write helper functions for checking the data and writing the files, but we will call only the 
# 'process_file' with 3 arguments (inputfile, output_good, output_bad).

import csv
import pprint

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):
    # store data into lists for output
    data_good = []
    data_bad = []
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for row in reader:
            # validate URI value
            if row['URI'].find("dbpedia.org") < 0:
                continue

            ps_year = row['productionStartYear'][:4]
            try: # use try/except to filter valid items
                ps_year = int(ps_year)
                row['productionStartYear'] = ps_year
                if (ps_year >= 1886) and (ps_year <= 2014):
                    data_good.append(row)
                else:
                    data_bad.append(row)
            except ValueError: # non-numeric strings caught by exception
                if ps_year == 'NULL':
                    data_bad.append(row)

    # Write processed data to output files
    with open(output_good, "w") as good:
        writer = csv.DictWriter(good, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data_good:
            writer.writerow(row)

    with open(output_bad, "w") as bad:
        writer = csv.DictWriter(bad, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data_bad:
            writer.writerow(row)



def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()
```
