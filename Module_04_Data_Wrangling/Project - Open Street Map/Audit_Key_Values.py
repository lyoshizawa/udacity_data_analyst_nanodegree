# Function to look at the values for a specific key attribute

import xml.etree.cElementTree as ET
import pprint

filename = 'sample.osm'

def audit_data(filename, key_value):
    keys = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag == 'tag':
            if elem.attrib['k'] == key_value:
                if elem.attrib['v'] in keys:
                    keys[elem.attrib['v']] += 1
                else:
                    keys[elem.attrib['v']] = 1
    return keys


postcode = audit_data(filename, 'addr:postcode')
cities = audit_data(filename, 'addr:city')
state = audit_data(filename, 'addr:state')

# uncomment the print statement you wish to audit

#pprint.pprint(cities)
#pprint.pprint(postcode)
#pprint.pprint(state)