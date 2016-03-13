
# coding: utf-8

# In[59]:

import xlrd as xl
import requests
from bs4 import BeautifulSoup


# In[6]:

wb = xl.open_workbook('./zipcodes-fa15.xlsx')


# In[15]:

all_values = []
for sheet in wb.sheets():
    for row in range(sheet.nrows):
        values = []
        for col in range(sheet.ncols):
            values.append(sheet.cell(row, col).value)
        all_values.append(values)
all_values = all_values[5:]


# In[129]:

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

