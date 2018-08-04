

```python
#Parse a CSV file (first 10 lines)
def parse_file(datafile):
    data =[]
    with open(datafile, "rb") as f:
        header = f.readline().split(",")
        counter = 0
        for line in f:
            # only parse first 10 lines
            if counter == 0:
                break
            
            fields = line.split(",")
            entry = {}
            
            for i, value in enumerate(fields):
                # strip is used to remove excess white space
                entry[header[i].strip()] = value.strip()
                
            data.append(entry)
            counter +=1
    
    return data
```


```python
# DictReader stores values in a data dictionary
import csv

def parse_csv(datafile):
    data = []
    n = 0
    with open(datafile, 'rb') as sd:
        r = csv.DictReader(sd)
        for line in r:
            data.append(line)
    return data
```


```python
# xlrd allows for processing excel files
import xlrd

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workboot.sheet_by_index(0)
    
    # loading the excel sheet into a list
    data = [[sheet.cell_value(r,col)
            for col in range(sheet.ncols)]
                for r in range(sheet.nrows)]
    
    print ("\nList Comprehension")
    print ("data[3][2]:"),
    print (data[3][2])
    
# number of rows in sheet
sheet.nrows
    
#type of data in a cell
sheet.cell_type(row, col)
    
#cell value
sheet.cell_value(row,col)
    
#convert date in excel to python date time
xlrd.xldate_as_tuple(sheet.cell_value(row,col),0)
```


```python
# load a file and find the date where the max value of 'COAST' appears
import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    data = [[sheet.cell_value(r,col)
            for col in range(sheet.ncols)]
            for r in range (sheet.nrows)]
    
    # pull all values from column 1 'Coast'
    cv = sheet.col_values(1, start_rowx=1, end_rowx_none)
    
    # find min and max values of 'Coast'
    maxval = max(cv)
    minva = min(cv)
    
    # use index on lists to find the maxval in the cv list
    maxpos = cv.index(maxval) + 1
    minpos = cv.index(minval) + 1
    
    # find the time for max/min values and convert it from excel to python formatting
    maxtime = sheet.cell_value(maxpos, 0)
    realtime = xlrd.xldate_as_tuple(maxtime,0)
    mintime = sheet.cell_value(minpos, 0)
    realmintime = xlrd.xldate_as_tuple(mintime,0)    

    ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:", 
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):", 
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):", 
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)

    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):", 
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)
    
    # return max/min value/times and average for the coast column
    data = {
            'maxtime': realtime,
            'maxvalue': maxval,
            'mintime': realmintime,
            'minvalue': minval,
            'avgcoast': sum(cv) / float(len(cv))
    }
    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()
```


```python
# JSON data format
# Items can have different fields
# Can have nested objects
# Can have nexted arrays

# JSONS are used commonly in web services
# JSON object = Python dictionary
```
