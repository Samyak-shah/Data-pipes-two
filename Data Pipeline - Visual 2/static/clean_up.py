import pprint
from collections import namedtuple
from openpyxl import load_workbook
import csv
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

#Import workbook to manipulate
wb = load_workbook(filename = 'SlateGunDeaths.xlsx')
ws_source = wb.get_sheet_by_name('SlateGunDeaths')

#named tuple
country = namedtuple("country", ["name", "year"])

#custom dictionary with two keys
my_dict = {}

#Fetch all the rows from the source sheet
for rowOfCellObjects in ws_source['A1':'K12071']:
	my_list = list()
	for cellObj in rowOfCellObjects:
		my_list.append(cellObj.value)
	date = my_list[1]
	
	count = my_dict.get(date, None)
	
	if(count == None):
		count = 1
	else:
		count += 1
	my_dict[date] = count

dict_size = len (my_dict)

pp.pprint(dict_size)
#pp.pprint(my_dict)

writer = csv.writer(open('dict.csv', 'wb'))
for key, value in my_dict.iteritems():
	#print(key)
	format_time = key
	#print(format_time)
	writer.writerow([format_time, value])