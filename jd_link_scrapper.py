import requests 
from bs4 import BeautifulSoup 
import json
import xlsxwriter

array = []
city_array = ['CITY']
link = ['Link']

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

city_list = ["Ahmedabad","Surat","Vadodara","Rajkot","Bhavnagar","Jamnagar","Mehsana","Porbandar","Bhuj","Morbi","Junagadh","Veraval","Amreli","Surendra-Nagar-Gujarat","Patan-Gujarat","Palanpur","Himatnagar","Idar","Vijapur","Visnagar","Modasa","Godhra","Dahod","Daang","Rajpipla","Halol","Bharuch","Anand","Nadiad","Ankleshwar","Vapi","Valsad","Diu","Daman","Botad","Gandhidham","Gandhinagar-Gujarat","Navsari","Viramgam","Tapi","Narmada"];

for i in range(len(city_list)):
	city = str(city_list[i])
	for i in range(1,100):
		URL = "https://www.justdial.com/"+city+"/Cinema/page-"+str(i)
		r = requests.get(URL, headers=agent)
		soup = BeautifulSoup(r.content, 'html5lib') 
		rows = soup.findAll('li', attrs = {'class':'cntanr'})
		print(len(rows))
		if(len(rows) == 0):
			break
		for row in rows:
			city_array.append(city)
			link.append(row["data-href"])
			print(row["data-href"])

array.append(city_array)
array.append(link)
workbook = xlsxwriter.Workbook('scrapp_link.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(array):
    worksheet.write_column(row, col, data)
workbook.close()
print (array)
