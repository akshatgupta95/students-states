
# coding: utf-8

# In[132]:

import xlrd as xl
import requests
import sys
from bs4 import BeautifulSoup


# In[135]:

out1 = open("out1.txt", "w")
out1.write("hello world")
out1.close()

output_file = open("output.txt", "w")
wb = xl.open_workbook('./app/static/zipcodes-fa15.xlsx')


# In[136]:

all_values = []
for sheet in wb.sheets():
    for row in range(sheet.nrows):
        values = []
        for col in range(sheet.ncols):
            values.append(sheet.cell(row, col).value)
        all_values.append(values)
all_values = all_values[5:]


# In[137]:

def get_state (zipcode):
    zipcode = str(zipcode)
    url = "http://www.city-data.com/zips/" + zipcode + ".html"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    success_div = soup.findAll(attrs={"class":"alert alert-success"})
    if (success_div is not None):
        a = success_div[0].find('a')
        state = str(a.text.split(',')[1].strip())
    else:
        state = None
    return state


# In[146]:

table = {}

midwest = "Midwest, 41.9653087, -91.8031071"
pacific = "Pacific, 39.8638751, -123.742465"
rocky = "Rocky Mountain, 41.2567792, -111.002006"
southwest = "Southwest, 41.2567792, -111.002006"
southeast = "Southeast, 32.0292207, -102.262669"
northeast = "Northeast, 42.3677199, -72.5757032"
noncontig = "Noncontiguous, 24.1755886, -98.5275888"

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

count = {}

# In[ ]:

for value in all_values:
    curr_zip = str(value[0])
    num_students = value[1]
    try:
        ret_val = table[get_state(curr_zip)]
        if ret_val in count:
            count[ret_val] += 1
        else:
            count[ret_val] = 0
        print("succeded on " + curr_zip)
        output_file.write(ret_val)
    except:
        print("failed on " + curr_zip)
        pass


# In[ ]:

output_file.close()


output_file2 = open("output2.txt", "w")
for key in count:
    output_file2.write(key)
    output_file2.write(str(count[key]))

output_file2.close()
