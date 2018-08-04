The following files are included in this project submission:

1.	osm_project.pdf: This is the report containing the process of auditing, cleaning, and analyzing the extracted Open Street Map data.

2.	map_selection.txt: This text file contains a link to the subject area of the analysis.

3.	code - audit key attributes.py: This python script iterates through the .osm file and prints a dictionary of all tag 'k' values as well as the frequency they appear.  This is for auditing the types of keys that are contained within the tags

4.	code - audit key values.py: This python script contains a function which will print a dictionary of all tag 'v' values that have a specific 'k' value and their frequency of appearance.  The 'k' values used are from the dictionary produced from the "code - audit key attributes.py" script.

5.	code -audit street types.py: This python script iterates through the osm file and looks for tags with a 'k' value of 'addr:street.'  It extracts the last word from the street name and prints a dictionary of the last word and their frequency of appearance.

6.	code -clean and export.py:  This python script iterates through the osm file, cleans incorrect data pertaining to incorrect street types, city names, or states, and exports the information into five different .csv files depending on the element.

7.	sample.osm : This is a sample of the data extracted from the original .osm file.  It contains every 20 lines from the original.

8.	resources.txt: This text file contains a list of resources used when working on this project.
