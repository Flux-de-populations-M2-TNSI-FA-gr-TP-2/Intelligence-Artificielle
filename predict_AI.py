# Import libraries
import argparse, datetime, json, pandas as pd, pickle, math, requests
from keras.models import Sequential
from keras.layers import Dense
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler


TOKEN = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijk3ODk4ZWU1LWM1MzAtNGFmZC1iODM2LWEwNWQ5YjNlZGI0YyJ9.eyJjbGllbnRfaWQiOiJsb2NhbC10b2tlbiIsInJvbGUiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZSI6Ii90aGluZ3M6cmVhZHdyaXRlIiwiaWF0IjoxNTc2MTY5MTI1LCJpc3MiOiJodHRwczovL3BpLXNlbnNvcnMubW96aWxsYS1pb3Qub3JnIn0.KolFPDYOWutwMh4qth4DccBasTi3zVd1cMh4_kKAnJRS1JZmpfRW52HXcok8NubpOu-hqM5qEOxYkXkRxMfjCQ'
WEATHER_API = '2f17ac3d47a723b7c853326f600e9786'
DEFAULT_TEMPERATURE = 18


def get_actual_temperature(default):
    try:
        temperature = default
        res = requests.get('https://pi-sensors.mozilla-iot.org/things', headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + TOKEN
        })
        #print(res.status_code)
        #print(res.text)
        if res.status_code == 200:
            data = json.loads(res.text)
            for p in data:
                link_device = p['id']
                #print(link_device)
                res2 = requests.get(link_device + '/properties', headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + TOKEN
                })
                #print(res2.status_code)
                #print(res2.text)
                data2 = json.loads(res2.text)
                if 'temperature' in data2:
                    temperature = float(data2['temperature'])
        return round(temperature)
    except requests.exceptions.RequestException as e:
        return default


def get_meteo_temperature(default, timestamp):
    try: 
        temperature = default
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=50.326255&lon=3.515010&APPID=' + WEATHER_API, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        #print(res.status_code)
        #print(res.text)
        if res.status_code == 200:
            data = json.loads(res.text)
            dates = [i['dt'] for i in data['list']]
            closest_timestamp_index = dates.index(min(dates, key=lambda x:abs(x-timestamp)))
            temperature_kelvin = data['list'][closest_timestamp_index]['main']['temp']
            temperature = temperature_kelvin - 273.15
        return round(temperature)
    except requests.exceptions.RequestException as e:
        return default


def main():
    #timestamp = 1576757400 # exemple
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('timestamp')
    args = parser.parse_args()

    timestamp = int(args.timestamp)

    # Compute arg to fit predict
    hour = math.floor((timestamp % 86400) / 3600)
    minute = math.floor(((timestamp % 86400) % 3600)/ 60)
    day = datetime.datetime.fromtimestamp(timestamp).weekday()
    
    # Get temperature if near future
    now = int(datetime.datetime.now(tz=None).timestamp())
    # 2 hours max between now and required timestamp to detect temperature (raspberry)
    if timestamp - now > 0 and timestamp - now < 7200:
        temperature = get_actual_temperature(DEFAULT_TEMPERATURE)
    # 5 days max between now and required timestamp to forecast meteo temperature
    elif timestamp - now > 0 and timestamp - now < 432000:
        temperature = get_meteo_temperature(DEFAULT_TEMPERATURE, timestamp)
    else:
        temperature = DEFAULT_TEMPERATURE

    # Load models from disk
    filename_fit = 'trained_model.sav'
    classifier = pickle.load(open(filename_fit, 'rb'))
    filename_preprocess = 'preprocess_model.sav'
    preprocess = pickle.load(open(filename_preprocess, 'rb'))

    X_test = pd.DataFrame(data={'Hour': [hour],
                            'Minute': [minute], 
                            'Day' : [day], 
                            'Temperature' : [temperature]})
    X_test = preprocess.transform(X_test)

    y_pred = classifier.predict(X_test)

    #print("\n===== Entrées =====")
    #print(hour)
    #print(minute)
    #print(day)
    #print(temperature)
    #print(X_test)
    #print("\n===== Résultats =====")
    #print(y_pred[0][0])
    #print(y_pred[0][0] > 0.5)
    #if y_pred[0][0] > 0.5:
    #    print("Tu peux aller au RU.")
    #else:
    #    print("Ne va pas au RU.")
    if y_pred[0][0] > 0.5:
        print(1)
    else:
        print(0)



if __name__ == '__main__':
    main()