from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "KlrnNrBdipA7L9DwvbwLgPYvrziVBHA1"
BASE_URL = 'http://dataservice.accuweather.com/'


@app.route('/weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    if not latitude or not longitude:
        return jsonify({'error': 'Укажите широту и долготу'}), 400

    location_key_url = f"{BASE_URL}locations/v1/cities/geoposition/search?apikey={API_KEY}&q={latitude},{longitude}"
    location_response = requests.get(location_key_url)

    if not location_response:
        return jsonify({'error': 'Ошибка получения данных о местоположении'}), 500

    location_data = location_response.json()
    location_key = location_data['Key']

    weather_url = f"{BASE_URL}forecasts/v1/daily/1day/{location_key}?apikey={API_KEY}&metric=true"
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        return jsonify({'error': 'Ошибка получения данных о погоде'}), 500

    weather_data = weather_response.json()
    forecast = weather_data['DailyForecasts'][0]

    result = {
        'temperature': forecast['Temperature']['Maximum']['Value'],
        'humidity': forecast['Day']['Humidity'],
        'wind_speed': forecast['Day']['Wind']['Speed']['Value'],
        'precipitation_probability': forecast['Day']['RainProbability']
    }

    return jsonify(result)


def check_bad_weather(conds):
    result = True

    if float(conds['temperature']) < -15 or float(conds['temperature']) > 35:
        result = False
    # if conds['humidity'] > 85:
    #     result = False
    # if conds['wind_speed'] > 50:
    #     result = False
    # if conds['precipitation_probability'] > 70:
    #     result = False

    return result


def simple_get_weather(city):
    location_key_url = f"{BASE_URL}locations/v1/cities/search?apikey={API_KEY}&q={city}"
    location_response = requests.get(location_key_url)

    location_data = location_response.json()
    location_key = location_data[0]['Key']

    weather_url = f"{BASE_URL}forecasts/v1/daily/1day/{location_key}?apikey={API_KEY}&metric=true"
    weather_response = requests.get(weather_url)

    forecast = weather_response.json()['DailyForecasts'][0]

    try:
        result = {
            'temperature': forecast['Temperature']['Maximum']['Value'],
            # 'humidity': forecast['Day']['Humidity'],
            #'wind_speed': forecast['Day']['Wind']['Speed']['Value'],
            #'precipitation_probability': forecast['Day']['RainProbability']
        }
        return result
    except KeyError:
        return


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_point = request.form.get("start_point")
        end_point = request.form.get("end_point")

        start_weather = simple_get_weather(start_point)
        start_weather_text = f"Температура: {start_weather["temperature"]}"
        # if start_weather is None:
        #     start_weather = "Ошибка получения данных"
        #     start_weather_conds = ""
        # else:
        #     start_weather_conds = check_bad_weather(start_weather)
        start_weather_conds = check_bad_weather(start_weather)
        start_weather_conds = "Погода хорошая" if start_weather_conds else "Погода плохая"

        end_weather = simple_get_weather(end_point)
        end_weather_text = f"Температура: {end_weather["temperature"]}"
        if end_weather is None:
            end_weather = "Ошибка получения данных"
            end_weather_conds = ""
        else:
            end_weather_conds = check_bad_weather(end_weather)

        end_weather_conds = "Погода хорошая" if end_weather_conds else "Погода плохая"
        return render_template("result.html", start_point=start_point, end_point=end_point, start_weather=start_weather_text,
                               end_weather=end_weather_text, start_weather_conds=start_weather_conds,
                               end_weather_conds=end_weather_conds)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=4003)

