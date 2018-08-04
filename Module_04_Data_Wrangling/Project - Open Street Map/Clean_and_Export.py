import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import schema
import cerberus

OSM_PATH = "oahu.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# Expected Values for Street Type
street_expected = ["Avenue", "Boulevard", "Circle", "Drive", "Highway", "Lane",
                   "Loop", "Mall", "Parkway", "Place", "Promenade", "Road", "Street", "Terrace", "Walk", "Way"]

# Mappings to correct Street, City, and State names.
street_mapping = { 
                "Ave.": "Avenue",
                "Blvd": "Boulevard",
                "Blvd.": "Boulevard",
                "Dr": "Drive",
                "Dr.": "Drive",
                "highway": "Highway",
                "Hwy": "Highway",
                "Hwy.": "Highway",
                "Pkwy": "Parkway",
                "Pl": "Place",
                "Rd": "Road",
                "St": "Street",
                "St.": "Street",
                "street": "Street"
                }
city_mapping = {
                "Haleiwa": "Hale'iwa",
                "Hale`iwa": "Hale'iwa",
                "Honlulu": "Honolulu",
                "Honoluu, HI": "Honolulu",
                "honolulu": "Honolulu",
                "kailua": "Kailua"
                }
state_mapping = {
                "Hawaii": "HI",
                "Hi": "HI",
                "hawaii": "HI",
                "hi": "HI"
                }


# function to fix the street name if there is a problem type
def fix_street_type(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in street_expected:
            better_type = street_type
            for k, v in street_mapping.items():
                if street_type == k:
                    better_type = v
            street_name = street_name.replace(street_type, better_type)
    return (street_name)


# function to update values based on mapping
def update_values(child, mapping):
    name = child.attrib['v']
    for k, v in mapping.items():
        if name == k:
            new_name = v
            return (new_name)
        else:
            return name

# functions to check for key values
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def is_state_name(elem):
    return (elem.attrib['k'] == "addr:state")

# function to fix values
def fix_values(child):
    if is_street_name(child):
        child.attrib['v'] = fix_street_type(child.attrib['v'])
        
    elif is_city_name(child):
        child.attrib['v'] = update_values(child, city_mapping)
        
    elif is_state_name(child):
        child.attrib['v'] = update_values(child, state_mapping)
        
    return (child)

# Function to extract the information from a "tag"
def child_tag(child, elem_attrib):
    # if the key value has problem characters, ignore the key
    if re.search(PROBLEMCHARS, child.attrib['k']):
        pass
                
    else:
        child = fix_values(child)
        
        split_key = child.attrib['k'].split(':')
        split_first = split_key[0]
        split_second = ':'.join(split_key[1:])
                
        # if there is no colon, set 'key' as k and 'type' as 'regular'
        if split_first == child.attrib['k']:
            tag = {
                'id': elem_attrib,
                'value': child.attrib['v'],
                'key': child.attrib['k'],
                'type': 'regular'
            }

        else:
        # if there is a colon, set 'type' as first part, and 'key' as second part
            tag = {
                'id': elem_attrib,
                'value': child.attrib['v'],
                'key': split_second,
                'type': split_first
            }        
    return (tag)
                        


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS):

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []


    # Check if element tag is Node
    if element.tag == 'node':
        for attribute in element.attrib:
            # check if the attribute is listed in the NODE_FIELDS list.  If so, save into node_attribs dictionary.
            if attribute in node_attr_fields:
                node_attribs[attribute] = element.attrib[attribute]

        # Identify child elements
        for child in element:          
            if child.tag == 'tag':
              tags.append(child_tag(child, element.attrib['id']))

        return {'node': node_attribs, 'node_tags': tags}

    # check if element type is 'way'    
    elif element.tag == 'way':
        # check if attributes are in the WAY_FIELDS list.  If there is a match, store it in the ways_attribs dictionary.
        for attribute in element.attrib:
            if attribute in way_attr_fields:
                way_attribs[attribute] = element.attrib[attribute]

        # initialize a counter for way_nodes
        wn_counter = 0        

        for child in element:

            # if child tag is 'tag', then call the child_tag function           
            if child.tag == 'tag':
                tags.append(child_tag(child, element.attrib['id']))

            # check if child tag is 'nd' and set waynode id, node id, and position
            elif child.tag == 'nd':
                way_nodes.append({
                    'id': element.attrib['id'],
                    'node_id' : child.attrib['ref'],
                    'position': wn_counter
                  })
                # increase counter by 1 for additional waynodes
                wn_counter += 1 

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    # Yield element if it is the right type of tag

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    # Raise ValidationError if element does not match schema
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.items())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


#class UnicodeDictWriter(csv.DictWriter, object):
    # Extend csv.DictWriter to handle Unicode input

#    def writerow(self, row):
#        super(UnicodeDictWriter, self).writerow({
#            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
#        })

#    def writerows(self, rows):
#        for row in rows:
#            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w', encoding='utf8') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w', encoding='utf8') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w', encoding='utf8') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w', encoding='utf8') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w', encoding='utf8') as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
