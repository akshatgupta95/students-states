import xlrd as xl
import csv
import requests
import sys
from json import dumps, dump

table = {}

midwest = "Midwest, 41.9653087, -91.8031071"
southeast = "Southeast, 32.8382351, -85.5280498"
noncontig = "Noncontiguous, 24.1755886, -98.5275888"
pacific = "Pacific, 39.8638751, -123.742465"
rocky = "Rocky Mountain, 41.2567792, -111.002006"
southwest = "Southwest, 32.0292207, -102.262669"

northeast = "Northeast, 42.3677199, -72.5757032"


table["IL"] = midwest # illinois
table["WI"] = midwest # wisconsin
table["IN"] = midwest # indiana
table["OH"] = midwest # ohio
table["MI"] = midwest # michigan
table["MO"] = midwest # missouri
table["IA"] = midwest # iowa
table["MN"] = midwest # minnesota
table["ND"] = midwest # north dakota
table["SD"] = midwest # south dakota
table["NE"] = midwest # nebraska
table["KS"] = midwest # kansas

table["CA"] = pacific # california
table["OR"] = pacific # oregon
table["WA"] = pacific # washington

table["ID"] = rocky # idaho
table["NV"] = rocky #nevada
table["MT"] = rocky # montana
table["UT"] = rocky # utah
table["CO"] = rocky # colorado
table["WY"] = rocky #wyoming

table["AZ"] = southwest # arizona
table["TX"] = southwest # texas
table["NM"] = southwest # new mexico
table["OK"] = southwest #oklahoma

table["LA"] = southeast # louisiana
table["AR"] = southeast # arkansas
table["MS"] = southeast # mississippi
table["AL"] = southeast # alabama
table["TN"] = southeast # tennessee
table["KY"] = southeast # kentucky
table["GA"] = southeast # georgia
table["FL"] = southeast # florida
table["SC"] = southeast # south carolina
table["NC"] = southeast # north carolina
table["VA"] = southeast # virginia
table["WV"] = southeast # west virginia
table["MD"] = southeast # maryland
table["DE"] = southeast # delaware

table["CT"] = northeast # connecticut
table["NJ"] = northeast # new jersey
table["NY"] = northeast # new york
table["PA"] = northeast # pennsylvania
table["MA"] = northeast # massachusetts
table["VT"] = northeast # vermont
table["NH"] = northeast # new hampshire
table["ME"] = northeast # maine
table["RI"] = northeast # rhode island

table["HI"] = noncontig # hawaii
table["AK"] = noncontig # alaska


all_data = {}
workbooks = ['./app/static/zipcodes-fa15.xlsx', './app/static/zipcodes-fa14.xlsx', './app/static/zipcodes-fa13.xlsx', './app/static/zipcodes-fa09.xls']
for workbook in workbooks:
    wb = xl.open_workbook(workbook)
    all_values = []
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            values = []
            for col in range(sheet.ncols):
                values.append(sheet.cell(row, col).value)
            all_values.append(values)
    all_values = all_values[5:]
    all_data[workbook] = all_values

# get the data for the countries
workbooks = ['./app/static/countryfa15.xls','./app/static/countryfa14.xls','./app/static/countryfa13.xls','./app/static/countryfa09.xls']
for workbook in workbooks:
    wb = xl.open_workbook(workbook)
    all_values = []
    for sheet in wb.sheets():
        for row in range(sheet.nrows):
            all_values.append((sheet.cell(row, 0).value, sheet.cell(row, 10).value))
        # print(all_values)
    all_values = all_values[7:]
    all_data[workbook] = all_values

# construct the hash table that converts zipcode to state
state_from_zip = {}

with open("./app/static/free-zipcode-database-Primary.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if not row[0] in state_from_zip:
            state_from_zip[row[0]] = row[3]

# lol, using the same hash table for countries...
with open("./app/static/country_list.txt", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="\t")
    for row in csv_reader:
        table[row[3]] = row[3] + ", " + row[1] + ", " + row[2]

all_counts = {}
for year in all_data.keys():
    count = {}
    if("zipcodes" in year):
        for value in all_data[year]:
            curr_zip = str(value[0])
            num_students = value[1]
            if(curr_zip in state_from_zip):
                state = state_from_zip[curr_zip]
                if(state in table):
                    ret_val = table[state]
                else:
                    ret_val = "other"
                if ret_val in count:
                    count[ret_val] += num_students
                else:
                    count[ret_val] = num_students
        all_counts[year] = count
    else: # parsing countries
        for value in all_data[year]:
            country = str(value[0]).strip(' ')
            num_students = value[1]
            # print(num_students)
            if(country in table):
                ret_val = table[country]
            else:
                ret_val = "other"

            if ret_val in count:
                count[ret_val] += num_students
            else:
                count[ret_val] = num_students
        all_counts[year] = count

json_dict = {}
years = []
datas = []
counts = []
output_file = "./app/static/latest_json.json"
for year in all_counts.keys():
    # print (year + "-------")
    for data in all_counts[year]:
        if ('other' not in data):
            # print (data, all_counts[year][data])
            years.append(year)
            datas.append(data)
            counts.append(all_counts[year][data])
    # print

json_dict["years"] = years
json_dict["region_data"] = datas
json_dict["num_students"] = counts

with open(output_file, "w") as f:
    dump(json_dict, f, indent=4)
