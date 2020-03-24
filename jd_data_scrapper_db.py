import requests 
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="jd"
)
mycursor = mydb.cursor(buffered=True)
from openpyxl import Workbook, load_workbook
from bs4 import BeautifulSoup 
import json
import time
import xlsxwriter
start_time = time.time()


proxies = {
 'http': 'http://120.138.117.102:59308',
 'https': 'http://120.138.117.102:59308',
}

number_ref = json.loads("""{ "9d001":"7", "9d002":"1", "9d003":"2", "9d004":"3", "9d005":"4", "9d006":"5", "9d007":"6", "9d008":"7", "9d009":"8", "9d010":"9", "9d011":"+", "9d012":"-", "9d013":")", "9d014":"("}""")

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
# 'Ahmedabad', 'Dholera','Dholka','Sanand','Viramgam','Amreli','Jafrabad','Savarkundla','Anand','Borsad','Khambhat','Modasa','Deesa','Dhanera','Palanpur','Bharuch','Ankleshwar','Jambusar','Bhavnagar','Palitana','Talaja','Vallabhipur','Botad','Barwala','Dahod','Kalyanpur','Khambhalia','Gandhinagar-Gujarat','Dehgam','Kalol-Gandhinagar-Gujarat',
#city_list = ['Mansa','Gir','Gir-Somnath','Una-Gujarat','Veraval','Jamnagar','Dhrol','Junagadh','Mangrol','Bhachau','Bhuj','Gandhidham','Mandvi','Mundra','Rapar','Kheda','Kapadvanj','Nadiad','Balasinor','Mehsana','Kadi','Unjha','Vijapur','Visnagar','Morbi','Wankaner','Navsari','Gandevi','Godhra','Halol','Kalol-Panchmahal-Gujarat','Patan-Gujarat','Sidhpur','Porbandar','Rajkot','Dhoraji','Gondal','Upleta','Himatnagar','Idar','Khedbrahma','Surat','Bardoli','Mandvi','Mangrol','Dhrangadhra','Wadhwan','Vyara','Vadodara','Dabhoi','Valsad','Dharampur','Vapi']
city_list = ['Jaipur','Udaipur-Rajasthan','Jodhpur','Mount-Abu','Abu-Road','Jaisalmer','Ajmer','Kota-Rajasthan']
for i in range(len(city_list)):
	city = str(city_list[i])
	j = 0;
	while 1:
		URL = "https://www.justdial.com/"+city+"/Taxi-Services/nct-10472932/page-"+str(j)
		j = j + 1
		r = requests.get(URL, headers=agent)#, proxies=proxies)
		soup = BeautifulSoup(r.content, 'html5lib') 
		rows = soup.findAll('li', attrs = {'class':'cntanr'})
		print(len(rows))
		if len(rows) == 0:
			break
		elif rows[0]["data-href"].split('/')[3] != city:
			break	
		else:
			for row in rows:
				r = requests.get(row["data-href"], headers=agent)#, proxies=proxies)
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
				# print(number_ref_list)
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
				# print("number = "+str(mobile_number))
				# print("services = "+str(services))
				# print("address"+address)
				# print("www = "+website_domain)
				# print("ratings ="+ratings)
				# print("votes ="+votes)
				# print(title)
				print(city)
				sql = 'SELECT * FROM `justdial` WHERE `title` = "'+title.strip()+'" AND `mobile_number` = "'+("||".join(str(x) for x in mobile_number)).strip()+'"'
				mycursor.execute(sql)
				# print(mycursor.fetchone())
				if mycursor.fetchone():
					print(mycursor.fetchone())
					print(1)
					pass
				else:
					sql = "INSERT INTO `justdial`(`title`, `mobile_number`, `services`, `ratings`, `votes`, `address`, `website_domain`, `city`, `keyword`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
					val = (title.strip(), ("||".join(str(x) for x in mobile_number)).strip(), ("||".join(str(x) for x in services)).strip(), ratings.strip(), votes.strip(), address.strip(), website_domain.strip(), city.strip(), 'Taxi-Services')
					mycursor.execute(sql,val)
					mydb.commit()
					print(2)