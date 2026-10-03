from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('OWM_KEY', 'eb4aef3a7bc85c912c1ac4c47d61ab7d')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    city = request.form.get('city', 'Berdsk')

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': city,
            'temp': round(data['main']['temp']),
            'feels': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'desc': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }
    else:
        weather = {'error': f"Город не найден (код {response.status_code})"}

    return render_template('index.html', weather=weather, city=city)

if __name__ == '__main__':
    app.run(debug=True)