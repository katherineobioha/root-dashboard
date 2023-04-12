import googlemaps







def getgeocode(farmloc):
    gmaps = googlemaps.Client(key='AIzaSyB7iE5c1R8Sg-O73sSAXz5DWfdmea8Bg4g')

    # Geocoding an address
    # print(farmloc+', delta')
    geocode_result = gmaps.geocode(farmloc+', delta')
    # print(geocode_result[0]["geometry"]["location"]["lat"])
    return geocode_result

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# farmer={'NAME': 'Kat', 'AGE': '46', 'FARM LOCATION': 'Udu', 'PHONE NO': '987887', 'LGA': 'Udu', 'SEX': 'F', 'PRODUCT TYPE': 'Cassava', 'FARM SIZE': '2 hec'}
#x=getgeocode("Udu")
#print(farmer)
# farmer.update({"LOCATION":{"lat":x[0]["geometry"]["location"]["lat"],
#                           "lng":x[0]["geometry"]["location"]["lng"]}})
# farmer["LOCATION"]["lat"] =x[0]["geometry"]["location"]["lat"]
# farmer["LOCATION"]["lon"] = x[0]["geometry"]["location"]["lon"]
#print(farmer)