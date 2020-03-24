import requests 
from openpyxl import Workbook, load_workbook
from bs4 import BeautifulSoup 
import json
import time
import xlsxwriter
start_time = time.time()

number_ref = json.loads("""{ "9d001":"7", "9d002":"1", "9d003":"2", "9d004":"3", "9d005":"4", "9d006":"5", "9d007":"6", "9d008":"7", "9d009":"8", "9d010":"9", "9d011":"+", "9d012":"-", "9d013":")", "9d014":"("}""")
array = []
title_array = []
city_array = []
number_array = []
rating_array = []
vote_array = []
services_array = []
address_array = []
website_array = []

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

# city_list = ["Ahmedabad","Surat","Vadodara","Rajkot","Bhavnagar","Jamnagar","Mehsana","Porbandar","Bhuj","Morbi","Junagadh","Veraval","Amreli","Surendra-Nagar-Gujarat","Patan-Gujarat","Palanpur","Himatnagar","Idar","Vijapur","Visnagar","Modasa","Godhra","Dahod","Daang","Rajpipla","Halol","Bharuch","Nadiad","Ankleshwar","Vapi","Valsad","Diu","Daman","Botad","Gandhidham","Gandhinagar-Gujarat","Navsari","Viramgam","Tapi","Narmada"];
city_list = ["Ahmedabad"]
for i in range(len(city_list)):
	city = str(city_list[i])
	for i in range(1,100):
		URL = "https://www.justdial.com/"+city+"/Doctors/nct-10892680/page-"+str(i)
		r = requests.get(URL, headers=agent)
		soup = BeautifulSoup(r.content, 'html5lib') 
		rows = soup.findAll('li', attrs = {'class':'cntanr'})
		print(len(rows))
		if(len(rows) == 0):
			break
		for row in rows:
			print(row["data-href"])
			r = requests.get(row["data-href"], headers=agent)
			soup = BeautifulSoup(r.content, 'html5lib')
			#(1)select css block from header and make an json for icon=>number link
			style = soup.findAll('style')
			number_ref_temp_list = str(style[1]).split('}')
			number_ref_list = {}
			#(1)iterate loop for icon list
			for i in range(2,16):
				temp = number_ref_temp_list[i].split(':');
				# number_ref_list[temp[0][1:]] = number_ref[temp[2][2:-1]]#number_ref assign value for number like 9d001 to 0
				if i < 12:
					number_ref_list[temp[0][1:]] = i-2#number_ref assign value for number like wich ever icon list come first assign 1, second 2
				else:
					number_ref_list[temp[0][1:]] = ' '
			#(2)contact box with detail like number, address, website url, ets.
			content = soup.find('ul',attrs = {'class':'comp-contact'})
			#(2)(1)mobile number list
			print(number_ref_list)
			try:
				number_icon_list = str(content.find('span',attrs={'class':'telnowpr'})).split(',')
				mobile_number = []
				#(2)(1)iterate loop for mobile number generation
				for icon_list in number_icon_list:
					temp = icon_list.split('mobilesv ')
					number_temp = ''
					for te in temp:
						if te[0:4] == 'icon':
							number_temp+= str(number_ref_list[te.split('"')[0]])
					mobile_number.append(number_temp.strip())
			except:
				print('hffg')
			try:
				website_domain = content.findAll('span',attrs={'class':'mreinfp comp-text'})[1].a['href']
			except:
				website_domain = ''
			services = []
			try:
				services_list = content.find('span',attrs={'class':'comp-text also-list showmore'})
				for link in services_list.findAll('a'):
					services.append(link.text.strip())
			except:
				services = []
			try:
				ratings = soup.find('span',attrs={'class':'value-titles'}).text
			except:
				ratings = ''
			try:
				votes = soup.find('span',attrs={'class':'votes'}).text
			except:
				votes = ''
			try:
				address = content.find('span',attrs={'class':'lng_add'}).text
			except:
				address = ''
			try:
				title = soup.find('span',attrs={'class':'fn'}).text
			except:
				title = ''
			title_array.append(title)
			number_array.append("||".join(str(x) for x in mobile_number))
			services_array.append(",".join(str(x) for x in services))
			rating_array.append(ratings)
			vote_array.append(votes)
			address_array.append(address)
			website_array.append(website_domain)
			city_array.append(city)
			print("number = "+str(mobile_number))
			print("services = "+str(services))
			print("address"+address)
			print("www = "+website_domain)
			print("ratings ="+ratings)
			print("votes ="+votes)
			print(title)
			print(city)

array.append(title_array)
array.append(number_array)
array.append(rating_array)
array.append(city_array)
array.append(address_array)
array.append(website_array)

workbook = xlsxwriter.Workbook('JD_Ahmedabad_Doctorsṭ_Data.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(array):
    worksheet.write_column(row, col, data)
workbook.close()
print (array)
