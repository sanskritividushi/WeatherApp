from datetime import datetime
from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=66d0699daa1771d5a140c199c74fa89a&units=metric').read()
        json_data = json.loads(res)

        #forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid=e7c2ab0f4038e880486eb3b2a25c1be9&units=metric'
        forecast_res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=66d0699daa1771d5a140c199c74fa89a&units=metric').read()
        forecast_data = json.loads(forecast_res)

        # Process forecast data (example: extracting first 5 days)
        # forecast_list = forecast_data.get('list', [])
        # daily_forecast = []
        # for item in forecast_list[:5]:  # Consider the first 5 days for simplicity
        #     date_str = item['dt_txt']
        #     date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        #     formatted_date = date_obj.strftime('%A, %B %d')
            
        #     daily_forecast.append({
        #         "date": formatted_date,
        #         "temp": item['main']['temp'],
        #         "weather": item['weather'][0]['main'],
        #         "description": item['weather'][0]['description']
        #     })

        forecast_list = forecast_data.get('list', [])
        daily_forecast = []
        today = datetime.now().date()

        for item in forecast_list:
            date_str = item['dt_txt']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%A, %B %d')

            # Check if it's a new day
            if date_obj.date() != today:
                today = date_obj.date()
                daily_forecast.append({
                    "date": formatted_date,
                    "temp": item['main']['temp'],
                    "weather": item['weather'][0]['main'],
                    "description": item['weather'][0]['description']
                })

        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
            "temp": str(json_data['main']['temp'])+' C',
            "pressure": str(json_data['main']['pressure']) + ' hPa',
            "humidity": str(json_data['main']['humidity'])+ ' %',
            "feels_like": str(json_data['main']['feels_like'])+ ' C',
            "weather": str(json_data['weather'][0]['main']),
            "daily_forecast": daily_forecast,
        }


    else:
        city = ''
        data = {}
    return render(request, 'weat.html', {'city': city, 'data': data})