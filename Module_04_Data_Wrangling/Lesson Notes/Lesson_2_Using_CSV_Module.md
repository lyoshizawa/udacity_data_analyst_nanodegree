
#!/usr/bin/env python
"""
Your task is to process the supplied file and use the csv module to extract data from it.
The data comes from NREL (National Renewable Energy Laboratory) website. Each file
contains information from one meteorological station, in particular - about amount of
solar and wind energy for each hour of day.

Note that the first line of the datafile is neither data entry, nor header. It is a line
describing the data source. You should extract the name of the station from it.

The data should be returned as a list of lists (not dictionaries).
You can use the csv modules "reader" method to get data in such format.
Another useful method is next() - to get the next line from the iterator.
You should only change the parse_file function.
"""


```python
import csv
import os

DATADIR = ""
DATAFILE = "745090.csv"


def parse_file(datafile):
    name = ""
    data = []
    with open(datafile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        name = reader.next()[1]
        print(name)
        header = r.next()
        print(header)
        for line in reader:
            data.append(line)
    # Do not change the line below
    return (name, data)

parse_file(DATAFILE)
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-93-640b450a4b84> in <module>()
         20     return (name, data)
         21 
    ---> 22 parse_file(DATAFILE)
    

    <ipython-input-93-640b450a4b84> in parse_file(datafile)
         11     with open(datafile,'r') as f:
         12         reader = csv.reader(f, delimiter=',')
    ---> 13         name = reader.next()[1]
         14         print(name)
         15         header = r.next()
    

    AttributeError: '_csv.reader' object has no attribute 'next'



```python
def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"


if __name__ == "__main__":
    test()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-86-b44ed136a219> in <module>()
         10 
         11 if __name__ == "__main__":
    ---> 12     test()
    

    <ipython-input-86-b44ed136a219> in test()
          1 def test():
          2     datafile = os.path.join(DATADIR, DATAFILE)
    ----> 3     name, data = parse_file(datafile)
          4 
          5     assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    

    <ipython-input-85-159a8f3047e9> in parse_file(datafile)
         11     with open(datafile,'rb') as f:
         12         r = csv.reader(f)
    ---> 13         name = r.next()[1]
         14         header = f.readline().split(",")
         15         for line in reader:
    

    AttributeError: '_csv.reader' object has no attribute 'next'

