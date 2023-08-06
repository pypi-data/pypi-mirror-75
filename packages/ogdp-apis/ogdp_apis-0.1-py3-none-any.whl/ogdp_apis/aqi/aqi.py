import requests
import json

class aqiData:

	def __init__(self, apiKey, *args):
		self.apiPath = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
		self.session = requests.Session()
		self.session.params = {
			"api-key": apiKey,
			"format": "json",
			"limit": 10000,
			"fields": ""
		}
		self.states = {
			"AP": "Andhra_Pradesh",
			"AS": "Assam",
			"BR": "Bihar",
			"CH": "Chandigarh",
			"CT": "Chhattisgarh",
			"DL": "Delhi",
			"GA": "Goa",
			"GJ": "Gujarat",
			"HR": "Haryana",
			"JH": "Jharkhand",
			"KA": "Karnataka",
			"KL": "Kerala",
			"LK": "Lakshadweep",
			"MP": "Madhya Pradesh",
			"MH": "Maharashtra",
			"MN": "Manipur",
			"ML": "Meghalaya",
			"MZ": "Mizoram",
			"OR": "Odisha",
			"PY": "Puducherry",
			"PB": "Punjab",
			"RJ": "Rajasthan",
			"SK": "Sikkim",
			"TN": "TamilNadu",
			"TG": "Telangana",
			"TP": "Tripura",
			"UP": "Uttar_Pradesh",
			"UK": "Uttarakhand",
			"WB": "West_Bengal"
		}


	def get_data(self, fields=['state','city','station','last_update','pollutant_id','pollutant_min','pollutant_max','pollutant_avg']):
		"""
		Query API for data in raw form
		"""
		self.session.params["fields"] = ','.join(fields)
		request = self.session.get(self.apiPath)
		return json.loads(request.content)


	def filter_data(self, data, filter={}):
		"""
		Fetch data that matches the values specified in the dict 'filter'
		filter={'city': 'Mumbai', 'pollutant': 'NO'}
		"""
		data = data['records']
		filteredData = []
		for x in range(len(data)):
			for key in filter:
				if data[x][key] == filter[key]:
					filteredData.append(data[x])
		return filteredData


	def format_data(self, data):
		"""
		Condense data for each station into one list item in the
		following format:

		{'city': 'Aurangabad',
		'last_update': '29-07-2020 09:00:00',
		'pollutants': {'CO': {'avg': '38', 'max': '80', 'min': '3'},
						'NH3': {'avg': '3', 'max': '3', 'min': '3'},
						'NO2': {'avg': '30', 'max': '33', 'min': '27'},
						'OZONE': {'avg': '10', 'max': '33', 'min': '7'},
						'PM10': {'avg': '36', 'max': '49', 'min': '31'},
						'SO2': {'avg': '15', 'max': '23', 'min': '8'}},
		'state': 'Maharashtra',
		'station': 'More Chowk Waluj, Aurangabad - MPCB'}
		"""
		# Create list of stations and organize pollutant values
		station_list = []
		for x in range(len(data)):
			data[x][data[x]["pollutant_id"]] = {
				"min": data[x].pop('pollutant_min'),
				"max": data[x].pop('pollutant_max'),
				"avg": data[x].pop('pollutant_avg')
			}	
			if station_list.count(data[x]['station']) == 0:
				station_list.append(data[x]['station'])
		# Count number of pollutants listed under each station
		station_map = {}
		for x in range(len(station_list)):
			station_map[station_list[x]] = 0
		for x in range(len(data)):
			if data[x]['station'] in station_list:
				station_map[data[x]['station']] += 1
		# Format to final form
		formatted_data = []
		pollutants = {}
		for key in station_map:
			for x in range(station_map[key]):
				for pollutant in data[x]:
					if pollutant in ['PM2.5', 'PM10', 'NO2', 'NH3', 'SO2', 'CO', 'OZONE']:
						pollutants[pollutant] = data[x][pollutant]
			data[0]['pollutants'] = pollutants
			pollutants = {}
			formatted_data.append(data[0])
			for x in range(station_map[key]):
				data.pop(0)
		for x in range(len(station_list)):
			formatted_data[x].pop(formatted_data[x]['pollutant_id'])
			formatted_data[x].pop('pollutant_id')
		# Fix state names
		for x in range(len(formatted_data)):
			formatted_data[x]['state'] = formatted_data[x]['state'].replace("_", " ")
			formatted_data[x]['state'] = formatted_data[x]['state'].replace("TamilNadu", "Tamil Nadu")
		# Return formatted data
		return formatted_data


	def state(self, state):
		"""
		Fetch a formatted list of data from stations in the specified state
		"""
		data = self.get_data()
		data = self.filter_data(data, filter={'state': self.states[state]})
		data = self.format_data(data)
		return data


	def city(self, city):
		"""
		Fetch a formatted list of data from stations in the specified city  
		"""
		data = self.get_data()
		data = self.filter_data(data, filter={'city': city})
		data = self.format_data(data)
		return data
	
	def station(self, station):
		"""
		Fetch a formatted list of data from stations in the specified city  
		"""
		data = self.get_data()
		data = self.filter_data(data, filter={'station': station})
		data = self.format_data(data)
		return data