import json
import requests



def get_data(coming,going,destination):
### GETTING THE DATA ###
    api_key = "AIzaSyCU-jysQL2DB3xRO12rzs4PN7UNOlAiEKA"
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
    headers = {'content-type': 'application/json'}
    params = {
      "request": {
        "slice": [
          {
            "origin": "SIN",
            "destination": destination, #"BKK"
            "date": going #"2015-01-19"
          }
        ],
        "passengers": {
          "adultCount": 1
        },
        "solutions": 30,
        "refundable": False
      }
    }
    #response = requests.post(url, data=json.dumps(params), headers=headers)
    #data = response.json()
    #print(data)

### END OF GETTING DATA ###

### Data manipulation ###
    file = open("flight data.json","r")
    flights = json.load(file)
    flight_details = flights['trips']['tripOption']
    for flight in flight_details:
        total_price = flight['saleTotal']
        fare = flight['pricing'][0]['saleFareTotal']
        tax = flight['pricing'][0]['saleTaxTotal']
        print(flight['slice'][0]['segment'])

get_data("SIN", "BKK", "2015-01-19")
    
