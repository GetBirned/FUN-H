import requests
from bs4 import BeautifulSoup
import json


def getMealItems():
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
				raise ValueError('Could not find menu table on page')

			# Find all the tr elements in the table
			menu_rows = menu_table.find_all('div', {'class': 'shortmenurecipes'})

			# Create a list to store the menu items
			items = []

			# Loop through the tr elements and extract the menu item text
			for row in menu_rows:
				item_text = row.text.strip()
				items.append(item_text)
			# Append the dictionary to the JSON file
			for item in items:
				item_dict = {'location': location_name, 'meal': meal, 'item': item}
				requests.post('https://testfunctionappcs518.azurewebsites.net/api/createrecord', json=item_dict)
				
getMealItems()