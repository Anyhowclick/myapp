import json
import requests
import datetime

money = {"BKK":"THB", "DMK":"THB", "KBV":"THB",
         "CNX":"THB", "HDY":"THB", "HKT":"THB",
         "CEI":"THB", "UTP":"THB", "URT":"THB",
         "UTH":"THB", "BWN":"BND"}

for key in ["HAN", "SGN", "DAD", "HUI", "CXR"]:
    money[key] = "VND"
for key in ["PNH", "REP"]:
    money[key] = "KHR"
for key in ["UPG", "MDC", "LOP", "KNO", "PDG", "PLM", "PKU", "SRG", "SOC", "JOG","CGK", "DPS", "BDO", "BPN"]:
    money[key] = "IDR"
for key in ["LPQ", "VTE"]:
    money[key] = "LAK"
for key in ["JHB", "BKI", "KUL", "KCH", "LGK", "PEN"]:
    money[key] = "MYR"
for key in ["MDL", "RGN", "NYT"]:
    money[key] = "MMK"
for key in ["ZAM", "CEB", "DVO", "MNL", "ILO"]:
    money[key] = "PHP"

def currency(destination):
    return money[destination]

### GETTING THE DATA ###

def get_data(coming,going,destination):
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
    response = requests.post(url, data=json.dumps(params), headers=headers)
    flights = response.json()
    keys = flights.keys()
    for key in keys:
        if key == "error":
            return "Ran out of quota!"

### END OF GETTING DATA ###

### HELPER FUNCTION(S) ###
    def helper(code, supporting):
        for support in supporting:
            if code == support['code']:
                return support['name']

### Data manipulation ###
    final = []
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
            carrier_name = helper(carrier, carriers)
            number = legs[leg]['flight']['number']
            bookingCode = legs[leg]['bookingCode']
            stuff = legs[leg]['leg'][0]
            arrival = stuff['arrivalTime']
            arrivalTZ = arrival[-6:]
            arrival = datetime.datetime.strptime(arrival[:-6], "%Y-%m-%dT%H:%M")
            departure = stuff['departureTime']
            departureTZ = departure[-6:]
            departure = datetime.datetime.strptime(departure[:-6], "%Y-%m-%dT%H:%M")
            destination = stuff['destination']
            dest_name = helper(destination, cities)
            dest_airport = helper(destination, airports)
            origin = stuff['origin']
            origin_name = helper(origin, cities)
            origin_airport = helper(origin, airports)
            flight_info[leg]={'carrier':carrier, 'carrier_num':number,
                              'arrival':arrival, 'arrivalTZ':arrivalTZ,
                              'departure':departure, 'departureTZ':departureTZ,
                              'origin':origin, 'destination':destination,
                              'carrier_name':carrier_name, 'dest_name':dest_name,
                              'dest_airport':dest_airport, 'origin_name':origin_name,
                              'origin_airport':origin_airport}
        total_flight_info.append(flight_info)
        final.append((total_price,holder,total_flight_info))
    return final

def temp_get_data():
    return [('SGD110.00', {'fare': 'SGD76.00', 'tax': 'SGD34.00'}, [{0: {'carrier_name': 'Jetstar Asia Airways Pte Ltd', 'departure': datetime.datetime(2015, 7, 28, 20, 30), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': '3K', 'carrier_num': '537', 'arrival': datetime.datetime(2015, 7, 28, 21, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD110.00', {'fare': 'SGD76.00', 'tax': 'SGD34.00'}, [{0: {'carrier_name': 'Jetstar Asia Airways Pte Ltd', 'departure': datetime.datetime(2015, 7, 28, 15, 0), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': '3K', 'carrier_num': '535', 'arrival': datetime.datetime(2015, 7, 28, 15, 50), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD120.00', {'fare': 'SGD86.00', 'tax': 'SGD34.00'}, [{0: {'carrier_name': 'Jetstar Asia Airways Pte Ltd', 'departure': datetime.datetime(2015, 7, 28, 8, 20), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': '3K', 'carrier_num': '533', 'arrival': datetime.datetime(2015, 7, 28, 9, 10), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD185.00', {'fare': 'SGD151.00', 'tax': 'SGD34.00'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 6, 40), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '602', 'arrival': datetime.datetime(2015, 7, 28, 7, 40), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 13, 5), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '794', 'arrival': datetime.datetime(2015, 7, 28, 13, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD185.00', {'fare': 'SGD151.00', 'tax': 'SGD34.00'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 11, 5), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '614', 'arrival': datetime.datetime(2015, 7, 28, 12, 5), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 13, 5), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '794', 'arrival': datetime.datetime(2015, 7, 28, 13, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD185.00', {'fare': 'SGD151.00', 'tax': 'SGD34.00'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 9, 50), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '604', 'arrival': datetime.datetime(2015, 7, 28, 10, 50), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 13, 5), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '794', 'arrival': datetime.datetime(2015, 7, 28, 13, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD473.30', {'fare': 'SGD390.00', 'tax': 'SGD83.30'}, [{0: {'carrier_name': 'Singapore Airlines Limited', 'departure': datetime.datetime(2015, 7, 28, 8, 40), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': 'SQ', 'carrier_num': '5052', 'arrival': datetime.datetime(2015, 7, 28, 9, 35), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD473.30', {'fare': 'SGD390.00', 'tax': 'SGD83.30'}, [{0: {'carrier_name': 'Singapore Airlines Limited', 'departure': datetime.datetime(2015, 7, 28, 13, 20), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': 'SQ', 'carrier_num': '5054', 'arrival': datetime.datetime(2015, 7, 28, 14, 10), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD473.30', {'fare': 'SGD390.00', 'tax': 'SGD83.30'}, [{0: {'carrier_name': 'Singapore Airlines Limited', 'departure': datetime.datetime(2015, 7, 28, 16, 25), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': 'SQ', 'carrier_num': '5056', 'arrival': datetime.datetime(2015, 7, 28, 17, 10), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD473.30', {'fare': 'SGD390.00', 'tax': 'SGD83.30'}, [{0: {'carrier_name': 'Singapore Airlines Limited', 'departure': datetime.datetime(2015, 7, 28, 18, 35), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': 'SQ', 'carrier_num': '5058', 'arrival': datetime.datetime(2015, 7, 28, 19, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD479.00', {'fare': 'SGD402.00', 'tax': 'SGD77.00'}, [{0: {'carrier_name': 'Air India Limited', 'departure': datetime.datetime(2015, 7, 28, 16, 0), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Bangkok', 'carrier': 'AI', 'carrier_num': '7242', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Bangkok Suvarnabhumi International', 'departureTZ': '+08:00', 'destination': 'BKK', 'arrivalTZ': '+07:00'}, 1: {'carrier_name': 'Thai Airways International Public', 'departure': datetime.datetime(2015, 7, 28, 22, 40), 'origin_airport': 'Bangkok Suvarnabhumi International', 'origin_name': 'Bangkok', 'origin': 'BKK', 'dest_name': 'Phuket', 'carrier': 'TG', 'carrier_num': '225', 'arrival': datetime.datetime(2015, 7, 28, 23, 59), 'dest_airport': 'Phuket International', 'departureTZ': '+07:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD488.00', {'fare': 'SGD411.00', 'tax': 'SGD77.00'}, [{0: {'carrier_name': 'Air India Limited', 'departure': datetime.datetime(2015, 7, 28, 16, 0), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Bangkok', 'carrier': 'AI', 'carrier_num': '7242', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Bangkok Suvarnabhumi International', 'departureTZ': '+08:00', 'destination': 'BKK', 'arrivalTZ': '+07:00'}, 1: {'carrier_name': 'Bangkok Airways Public Company Limited', 'departure': datetime.datetime(2015, 7, 28, 19, 45), 'origin_airport': 'Bangkok Suvarnabhumi International', 'origin_name': 'Bangkok', 'origin': 'BKK', 'dest_name': 'Phuket', 'carrier': 'PG', 'carrier_num': '279', 'arrival': datetime.datetime(2015, 7, 28, 21, 10), 'dest_airport': 'Phuket International', 'departureTZ': '+07:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD488.00', {'fare': 'SGD411.00', 'tax': 'SGD77.00'}, [{0: {'carrier_name': 'Air India Limited', 'departure': datetime.datetime(2015, 7, 28, 16, 0), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Bangkok', 'carrier': 'AI', 'carrier_num': '7242', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Bangkok Suvarnabhumi International', 'departureTZ': '+08:00', 'destination': 'BKK', 'arrivalTZ': '+07:00'}, 1: {'carrier_name': 'Bangkok Airways Public Company Limited', 'departure': datetime.datetime(2015, 7, 28, 21, 55), 'origin_airport': 'Bangkok Suvarnabhumi International', 'origin_name': 'Bangkok', 'origin': 'BKK', 'dest_name': 'Phuket', 'carrier': 'PG', 'carrier_num': '220', 'arrival': datetime.datetime(2015, 7, 28, 23, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+07:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD751.40', {'fare': 'SGD653.00', 'tax': 'SGD98.40'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 6, 40), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '602', 'arrival': datetime.datetime(2015, 7, 28, 7, 40), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 17, 10), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '790', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD751.40', {'fare': 'SGD653.00', 'tax': 'SGD98.40'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 11, 5), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '614', 'arrival': datetime.datetime(2015, 7, 28, 12, 5), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 17, 10), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '790', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD751.40', {'fare': 'SGD653.00', 'tax': 'SGD98.40'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 9, 50), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '604', 'arrival': datetime.datetime(2015, 7, 28, 10, 50), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 17, 10), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '790', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD751.40', {'fare': 'SGD653.00', 'tax': 'SGD98.40'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 13, 40), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '606', 'arrival': datetime.datetime(2015, 7, 28, 14, 40), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 17, 10), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '790', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD836.20', {'fare': 'SGD746.00', 'tax': 'SGD90.20'}, [{0: {'carrier_name': 'SilkAir (S) Pte. Ltd.', 'departure': datetime.datetime(2015, 7, 28, 8, 10), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Koh Samui', 'carrier': 'MI', 'carrier_num': '772', 'arrival': datetime.datetime(2015, 7, 28, 8, 55), 'dest_airport': 'Ko Samui', 'departureTZ': '+08:00', 'destination': 'USM', 'arrivalTZ': '+07:00'}, 1: {'carrier_name': 'SilkAir (S) Pte. Ltd.', 'departure': datetime.datetime(2015, 7, 28, 14, 30), 'origin_airport': 'Ko Samui', 'origin_name': 'Koh Samui', 'origin': 'USM', 'dest_name': 'Phuket', 'carrier': 'MI', 'carrier_num': '5655', 'arrival': datetime.datetime(2015, 7, 28, 15, 30), 'dest_airport': 'Phuket International', 'departureTZ': '+07:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD836.20', {'fare': 'SGD746.00', 'tax': 'SGD90.20'}, [{0: {'carrier_name': 'SilkAir (S) Pte. Ltd.', 'departure': datetime.datetime(2015, 7, 28, 8, 10), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Koh Samui', 'carrier': 'MI', 'carrier_num': '772', 'arrival': datetime.datetime(2015, 7, 28, 8, 55), 'dest_airport': 'Ko Samui', 'departureTZ': '+08:00', 'destination': 'USM', 'arrivalTZ': '+07:00'}, 1: {'carrier_name': 'SilkAir (S) Pte. Ltd.', 'departure': datetime.datetime(2015, 7, 28, 11, 25), 'origin_airport': 'Ko Samui', 'origin_name': 'Koh Samui', 'origin': 'USM', 'dest_name': 'Phuket', 'carrier': 'MI', 'carrier_num': '5653', 'arrival': datetime.datetime(2015, 7, 28, 12, 25), 'dest_airport': 'Phuket International', 'departureTZ': '+07:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD857.70', {'fare': 'SGD710.00', 'tax': 'SGD147.70'}, [{0: {'carrier_name': 'SilkAir (S) Pte. Ltd.', 'departure': datetime.datetime(2015, 7, 28, 9, 50), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MI', 'carrier_num': '5704', 'arrival': datetime.datetime(2015, 7, 28, 10, 50), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 13, 5), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '794', 'arrival': datetime.datetime(2015, 7, 28, 13, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD857.70', {'fare': 'SGD710.00', 'tax': 'SGD147.70'}, [{0: {'carrier_name': 'SilkAir (S) Pte. Ltd.', 'departure': datetime.datetime(2015, 7, 28, 11, 5), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MI', 'carrier_num': '5714', 'arrival': datetime.datetime(2015, 7, 28, 12, 5), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 13, 5), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '794', 'arrival': datetime.datetime(2015, 7, 28, 13, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD882.50', {'fare': 'SGD780.00', 'tax': 'SGD102.50'}, [{0: {'carrier_name': 'SilkAir (S) Pte. Ltd.', 'departure': datetime.datetime(2015, 7, 28, 8, 40), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Phuket', 'carrier': 'MI', 'carrier_num': '752', 'arrival': datetime.datetime(2015, 7, 28, 9, 35), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD898.70', {'fare': 'SGD751.00', 'tax': 'SGD147.70'}, [{0: {'carrier_name': 'Singapore Airlines Limited', 'departure': datetime.datetime(2015, 7, 28, 11, 5), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'SQ', 'carrier_num': '5614', 'arrival': datetime.datetime(2015, 7, 28, 12, 5), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 13, 5), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '794', 'arrival': datetime.datetime(2015, 7, 28, 13, 20), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD925.00', {'fare': 'SGD891.00', 'tax': 'SGD34.00'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 6, 40), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '602', 'arrival': datetime.datetime(2015, 7, 28, 7, 40), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 9, 30), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '786', 'arrival': datetime.datetime(2015, 7, 28, 9, 45), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}]),
    ('SGD969.90', {'fare': 'SGD803.00', 'tax': 'SGD166.90'}, [{0: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 12, 45), 'origin_airport': 'Singapore Changi', 'origin_name': 'Singapore', 'origin': 'SIN', 'dest_name': 'Kuala Lumpur', 'carrier': 'MH', 'carrier_num': '5728', 'arrival': datetime.datetime(2015, 7, 28, 13, 45), 'dest_airport': 'Kuala Lumpur International', 'departureTZ': '+08:00', 'destination': 'KUL', 'arrivalTZ': '+08:00'}, 1: {'carrier_name': 'Malaysia Airlines', 'departure': datetime.datetime(2015, 7, 28, 17, 10), 'origin_airport': 'Kuala Lumpur International', 'origin_name': 'Kuala Lumpur', 'origin': 'KUL', 'dest_name': 'Phuket', 'carrier': 'MH', 'carrier_num': '790', 'arrival': datetime.datetime(2015, 7, 28, 17, 25), 'dest_airport': 'Phuket International', 'departureTZ': '+08:00', 'destination': 'HKT', 'arrivalTZ': '+07:00'}}])]
