# Importing Required Libraries.
import json
import requests

# Panic Error method.
def app_panic(status):
	print 'Application ERROR: {0}'.format(status)
	exit(1)

# Defining Weather-bot class.
class weather_bot:

	# Init will build API urls for us.
	def __init__(self):

		self.WEATHER_API_ENDPOINT = 'http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}'
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

			app_panic('Connection Error (weather).')

		# If there is an HTTP status error code.
		if response.status_code is not 200:

			app_panic('Connection Error (weather).')

		# Cool everything looks cool, move along.
		else:
			data = json.loads(response.text)
			
			# Storing the whole weather hash into our class.
			self.weather_data = data

	# Localize will lookup the bot's location.
	def __localize__(self):
		
		# Try to make connection with requests.
		try:
			response = requests.get(self.LOCATION_API_ENDPOINT)

		except requests.ConnectionError:

			app_panic('Connection Error (localize).')


		# If there is an HTTP status error code.
		if response.status_code is not 200:

			app_panic('Bad HTTP Response (localize).')

		# Cool everything looks cool, move along.
		else:
			data = json.loads(response.text)

			self.lat = data['latitude']
			self.lon = data['longitude']
			
			# Format weather endoint with our coords.
			self.WEATHER_API_ENDPOINT = self.WEATHER_API_ENDPOINT.format(self.lat, self.lon)

# Main routine.
if __name__ == '__main__':

	# Create our weather-bot.
	bot = weather_bot()
	print bot.WEATHER_API_ENDPOINT
