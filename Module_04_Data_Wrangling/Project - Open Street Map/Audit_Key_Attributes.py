# Script to show a list and count of tag keys

import xml.etree.cElementTree as ET
import pprint
filename = 'sample.osm'
# modified from Case Study Quiz: Iterative Parsing
attributes ={}
for event, elem in ET.iterparse(filename):
    if elem.tag == 'tag':
        if elem.attrib['k'] in attributes:
            attributes[elem.attrib['k']] += 1
        else:
            attributes[elem.attrib['k']] = 1

print (len(attributes))
pprint.pprint(attributes)