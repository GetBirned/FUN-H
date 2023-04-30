import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime



create_url = 'https://testfunctionappcs518.azurewebsites.net/api/createrecord'
delete_url = 'https://testfunctionappcs518.azurewebsites.net/api/deleterecord'
read_url = 'https://testfunctionappcs518.azurewebsites.net/api/readrecords'

def deleteMealItems(month, day, year):
	#print(response.text)
	#print(response)
	response = requests.get(delete_url, params={"query": '{"date": "'
					     f'{month}-{day}-{year}'
	       '"}'})
	#print(response.text)
	#print(response)
	#response = requests.get(delete_url, params={"query": '{"location": "philly"}'})
	#print(response.text)
	#print(response)	

#&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=5%2F1%2F2023

def getMealFromDateAndLocation(month, day, year):
	#philly_date_url = 'http://foodpro.unh.edu/shortmenu.asp?sName=University+Of+New+Hampshire'
	#'+Hospitality+Services&locationNum=30&locationName=Philbrook+Dining+Hall&naFlag=1&WeeksMe'
	#f'nus=This+Week%27s+Menus&myaction=read&dtdate={month}%2F{day}%2F{year}'
	philly_date_url = f'http://foodpro.unh.edu/shortmenu.asp?sName=%3Cbr+%2F%3E%3Ca+href%3D%22http%3A%2F%2Fwww%2Eunh%2Eedu%2Fdining%22%3E%3Ch2%3EUNH+Dining+%3C%2Fh2%3E%3C%2Fa%3E%3Cp%3E%3Ch2%3EMenus%3C%2Fh2%3E%3C%2Fp%3E&locationNum=30&locationName=Phillbrook+Dining+Hall&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate={month}%2F{day}%2F{year}'
	hoco_date_url = f'http://foodpro.unh.edu/shortmenu.asp?sName=%3Cbr+%2F%3E%3Ca+href%3D%22http%3A%2F%2Fwww%2Eunh%2Eedu%2Fdining%22%3E%3Ch2%3EUNH+Dining+%3C%2Fh2%3E%3C%2Fa%3E%3Cp%3E%3Ch2%3EMenus%3C%2Fh2%3E%3C%2Fp%3E&locationNum=80&locationName=Holloway+Commons&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate={month}%2F{day}%2F{year}'
	location_names = ['hoco', 'philly']
	locations = [hoco_date_url, philly_date_url]
	meals = ['Breakfast', 'Lunch', 'Dinner']
	# Send a GET request to the URL and get the HTML content
	for i, location in enumerate(locations):
		response = requests.get(location)
		content = response.content
		# Use Beautiful Soup to parse the HTML content
		soup = BeautifulSoup(content, 'html.parser')
		location_name = location_names[i]
		for meal in meals:
			# Find the table that contains the menu
			menu_table = soup.find('table', {'id': meal})
			if menu_table is None:
				continue

			# Find all the tr elements in the table
			menu_rows = menu_table.find_all('div', {'class': 'shortmenurecipes'})

			# Create a list to store the menu items
			items = []
			item_list = []
			# Loop through the tr elements and extract the menu item text
			for row in menu_rows:
				item_text = row.text.strip()
				items.append(item_text)
			# Append the dictionary to the JSON file
			for item in items:
				item_dict = {'location': location_name, 'meal': meal, 'item': item, 'date': ("%s-%s-%s" % (month, day, year))}
				item_list.append(item_dict)
			requests.post(create_url, json=item_list)

def getMealItems():
	# Get the time
	current_time = datetime.now()

	# Define the URLs for Holloway Commons and Philbrook Dining Hall
	hoco = 'http://foodpro.unh.edu/shortmenu.asp?sName=%3Cbr+%2F%3E%3Ca+href%3D%22http%3A%2F%2Fwww%2Eunh%2Eedu%2Fdining%22%3E%3Ch2%3EUNH+Dining+%3C%2Fh2%3E%3C%2Fa%3E%3Cp%3E%3Ch2%3EMenus%3C%2Fh2%3E%3C%2Fp%3E&locationNum=80&locationName=Holloway+Commons&naFlag=1'
	philly = 'http://foodpro.unh.edu/shortmenu.asp?sName=University%20Of%20New%20Hampshire%20Hospitality%20Services&locationNum=30&locationName=Philbrook%20Dining%20Hall&naFlag=1'
	location_names = ['hoco', 'philly']
	locations = [hoco, philly]
	meals = ['Breakfast', 'Lunch', 'Dinner']
	# Send a GET request to the URL and get the HTML content
	for i, location in enumerate(locations):
		response = requests.get(location)
		content = response.content
		# Use Beautiful Soup to parse the HTML content
		soup = BeautifulSoup(content, 'html.parser')
		location_name = location_names[i]
		for meal in meals:
			# Find the table that contains the menu
			menu_table = soup.find('table', {'id': meal})
			if menu_table is None:
				continue

			# Find all the tr elements in the table
			menu_rows = menu_table.find_all('div', {'class': 'shortmenurecipes'})

			# Create a list to store the menu items
			items = []
			item_list = []
			# Loop through the tr elements and extract the menu item text
			for row in menu_rows:
				item_text = row.text.strip()
				items.append(item_text)
			# Append the dictionary to the JSON file
			for item in items:
				item_dict = {'location': location_name, 'meal': meal, 'item': item, 'date': ("%s-%s-%s" % (current_time.month, current_time.day, current_time.year))}
				item_list.append(item_dict)
			requests.post(create_url, json=item_list)
				


#deleteMealItems()
deleteMealItems(4,29,2023)
getMealFromDateAndLocation(4,29,2023)
#getMealItems()
#getMealFromDateAndLocation(4,29,2023)
#getMealFromDateAndLocation(4,30,2023)



#USE THIS TO FETCH MENUS FOR AN ENTIRE MONTH
#From what i can gather, the menus are only stored for 2 weeks
#The earliest date I could fetch food for was April 15, 2023
for i in range(1, 32):
	#deleteMealItems(4,i,2023)
	getMealFromDateAndLocation(5,i,2023)