#! /usr/bin/python

# Kyle Luce
# May 9, 2014
# weather-bot.py

# Importing Required Libraries.
import json
import requests
import sys

# Panic Error method.
def app_panic(status):
	print '\033[91mApplication ERROR: {0}\033[0m'.format(status)
	exit(1)

# Defining Weather-bot class.
class weather_bot:

	# Init will build API urls for us.
	def __init__(self):

		# Defining the two API Endpoints.
		self.WEATHER_API_ENDPOINT = 'http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=imperial'
		self.LOCATION_API_ENDPOINT = 'http://freegeoip.net/json'
		
		# Now the weather-bot needs to localize our current position.
		self.__localize__()

		# Now the weather-bot can get our weather data.
		self.__get_weather__()

	# Get_weather will lookup the current weather.
	def __get_weather__(self):

		# Get weather response.
		try:
			response = requests.get(self.WEATHER_API_ENDPOINT)

		except requests.ConnectionError:

			app_panic('Connection Error (Can\'t lookup weather).')

		# If there is an HTTP status error code.
		if response.status_code is not 200:

			app_panic('Connection Error (Can\'t lookup weather).')

		# Cool everything looks cool, move along.
		else:

			# Storing the whole weather hash into our class.
			self.weather_data = json.loads(response.text)

	# Localize will lookup the bot's location.
	def __localize__(self):
		
		# Try to make connection with requests.
		try:
			response = requests.get(self.LOCATION_API_ENDPOINT)

		except requests.ConnectionError:

			app_panic('Connection Error (Can\'t lookup Location).')


		# If there is an HTTP status error code.
		if response.status_code is not 200:

			app_panic('Bad HTTP Response (Can\'t lookup Location).')

		# Cool everything looks cool, move along.
		else:
			data = json.loads(response.text)

			self.lat = data['latitude']
			self.lon = data['longitude']
			
			# Format weather endoint with our coords.
			self.WEATHER_API_ENDPOINT = self.WEATHER_API_ENDPOINT.format(self.lat, self.lon)

	# Show_weather will format the weather_data and print it to screen.
	def show_weather(self):
		print '\033[94mweather-bot>\033[0m {0}, and it\'s {1} degrees at {2}% humidity.'.format(
								self.weather_data['weather'][0]['description'],
								self.weather_data['main']['temp'],
								self.weather_data['main']['humidity'],
								)

# Main routine.
if __name__ == '__main__':

	# Create our weather-bot.
	bot = weather_bot()

	# Check to see if debug option is set.
	if '--debug' in sys.argv:

		print 'Debug ON'
		print 'Lat -> {0}, Lon -> {1}'.format(bot.lat, bot.lon)

	# Print the current weather conditions.
	bot.show_weather()
