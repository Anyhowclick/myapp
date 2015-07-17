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
        "solutions": 25,
        "refundable": False
      }
    }
    #response = requests.post(url, data=json.dumps(params), headers=headers)
    #flights = response.json()

### END OF GETTING DATA ###

### Data manipulation ###
    final = []
    #file = open("flight data.json","r")
    #flights = json.load(file)
    support = flights['trips']['data']
    carriers = support['carrier'] #<<< carrier details Eg. Jetstar, Air India
    aircraft = support['aircraft'] #<<< Eg. Airbus 320
    cities = support['city'] #<<< Eg. BKK = bangkok
    airports = support['airport']
    flight_details = flights['trips']['tripOption']
    for flight in flight_details:
        total_price = flight['saleTotal']
        prices = flight['pricing']
        for price in prices:
            holder = {}
            fare = price['saleFareTotal']
            tax = price['saleTaxTotal']
            holder = {"fare" : fare, "tax" : tax}
        parts = flight['slice'][0]
        legs = parts['segment']
        #duration = parts['duration']
        flight_info = {}
        total_flight_info = []
        for leg in range(0,len(legs)):
            carrier = legs[leg]['flight']['carrier']
            number = legs[leg]['flight']['number']
            bookingCode = legs[leg]['bookingCode']
            stuff = legs[leg]['leg'][0]
            arrival = stuff['arrivalTime']
            departure = stuff['departureTime']
            destination = stuff['destination']
            origin = stuff['origin']
            flight_info[leg]={}
            flight_info[leg]['bookingCode']=bookingCode
            flight_info[leg]['carrier']=carrier
            flight_info[leg]['carrier_num']=number
            flight_info[leg]['arrival']=arrival
            flight_info[leg]['departure']=departure
            flight_info[leg]['origin']=origin
            flight_info[leg]['destination']=destination
            total_flight_info.append(flight_info)
            final.append((total_price,holder,total_flight_info))
    return final

print(get_data("2015-07-25", "2015-07-26","BKK"))
    
