from datetime import datetime
from django.shortcuts import render
import json
import urllib.request

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=66d0699daa1771d5a140c199c74fa89a&units=metric').read()
        json_data = json.loads(res)

        forecast_res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=66d0699daa1771d5a140c199c74fa89a&units=metric').read()
        forecast_data = json.loads(forecast_res)

        forecast_list = forecast_data.get('list', [])
        daily_forecast = []
        today = datetime.now().date()

        for item in forecast_list:
            date_str = item['dt_txt']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%A, %B %d')

            if date_obj.date() != today:
                today = date_obj.date()
                daily_forecast.append({
                    "date": formatted_date,
                    "temp": item['main']['temp'],
                    "weather": item['weather'][0]['main'],
                    "description": item['weather'][0]['description']
                })

        data = {
            "country_code": "Country Code",  # Replace with actual country code if available
            "coordinate": "Longitude Latitude",  # Replace with actual coordinates if available
            "temp": "Temperature",  # Replace with actual temperature
            "pressure": "Pressure",  # Replace with actual pressure
            "humidity": "Humidity",  # Replace with actual humidity
            "feels_like": "Feels Like",  # Replace with actual feels like temperature
            "weather": "Weather",  # Replace with actual weather description
            "daily_forecast": daily_forecast,
        }
    else:
        city = ''
        data = {}

    return render(request, 'weat.html', {'city': city, 'data': data})
