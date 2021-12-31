#!/usr/bin/env python3
import requests
import json


#Global Veriables
global WEATHER_API_KEY
global LOCATIONS


def main():

    try:
        checkConfig()
    except Exception:
        print('config file not found')

    #Get the time data for the locations listed
    data = getWeather()

    #print(json.dumps(data, indent=4))

    with open('weatherData.txt', 'w') as outfile:
        json.dump(data, outfile, indent=2)


def getWeather():

    #initialize empty dictionary
    data = {}

    base_url = 'https://api.tomorrow.io/v4/timelines'
    for i in range(len(LOCATIONS)):
    #for i in range(1):
        payload = {
            'location' : '{},{}'.format(LOCATIONS[i][1],LOCATIONS[i][2]),  # Get real locations
            #'timezone': "America/Los_Angeles",
            'timezone': "America/Los_Angeles",
            'fields': ['temperature','precipitationProbability','precipitationType','precipitationIntensity' ,
                        'snowAccumulation', 'cloudCover', 'visibility', 'weatherCode'],
            'apikey': WEATHER_API_KEY,
            'units': "imperial",
            #'timesteps':['1d','1h'],
            'timesteps': '1h',
            }

        #Pull the weather data for the specificed location
        req = requests.get(base_url, params = payload)
        parsed_json = req.json()

        #print(json.dumps(parsed_json, indent=4))
        #print(len(parsed_json['data']['timelines'][0]['intervals']))
        #print(LOCATIONS[i][0])

        #initialize dict with location key as empty list
        data[LOCATIONS[i][0]] = []

        #take data from the tomorrow.io json file and reformat it
        for j in range(len(parsed_json['data']['timelines'][0]['intervals'])):
            data[LOCATIONS[i][0]].append({
                'date': parsed_json['data']['timelines'][0]['intervals'][j]['startTime'][0:10],
                'time': parsed_json['data']['timelines'][0]['intervals'][j]['startTime'][11:16],
                'temperature': parsed_json['data']['timelines'][0]['intervals'][j]['values']['temperature'],
                'precipitationProbability': parsed_json['data']['timelines'][0]['intervals'][j]['values']['precipitationProbability'],
                'precipitationType': parsed_json['data']['timelines'][0]['intervals'][j]['values']['precipitationType'],
                'precipitationIntensity': parsed_json['data']['timelines'][0]['intervals'][j]['values']['precipitationIntensity'],
                'snowAccumulation': parsed_json['data']['timelines'][0]['intervals'][j]['values']['snowAccumulation'],
                'cloudCover': parsed_json['data']['timelines'][0]['intervals'][j]['values']['cloudCover'],
                'visibility': parsed_json['data']['timelines'][0]['intervals'][j]['values']['visibility'],
                'weatherCode': parsed_json['data']['timelines'][0]['intervals'][j]['values']['weatherCode'],
                })

    #print(json.dumps(data, indent=4))
    return(data)




def checkConfig():
    global WEATHER_API_KEY
    global LOCATIONS

    with open('config.json') as file:
        parsed_json = json.load(file)

    WEATHER_API_KEY = parsed_json['config']['weather_api_key']

    LOCATIONS = []
    i = 0
    for items in parsed_json['config']['locations']:
        LOCATIONS.append([parsed_json['config']['locations'][i]['name'],
                            parsed_json['config']['locations'][i]['latitude'],
                            parsed_json['config']['locations'][i]['longitude']])
        i = i + 1

    #print(parsed_json['config']['weather_api_key'])
    #print(parsed_json['config']['locations'][0])



if __name__== "__main__":
    main()
