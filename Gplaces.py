import googlemaps

class Gplaces:
    def __init__(self, API_KEY):

        self.gmaps = googlemaps.Client(key=API_KEY)

        self.b_name = None
        self.b_types = None

        self.lat = None
        self.lng = None

        self.target_place = None
        self.nearby_places = None

    def get_place(self, name, lat = None, lng = None):
        results = None
        
        if lat == None or lng == None:
            results = self.gmaps.places(query=name)

        else:
            results = self.gmaps.places(query=name, location=(lat,lng))
       
        if results["status"] != "OK":
            return None
            
        target_place = results["results"][0]

        self.b_name = target_place['name']
        self.b_types = target_place['types']

        self.lat = target_place["geometry"]["location"]["lat"]
        self.lng = target_place["geometry"]["location"]["lng"]

        self.target_place = target_place

        return target_place
  
    def get_similar_places(self, b_types = None, lat = None, lng= None, radius = 3000, type_tolerance = 1):

        if b_types == None:
            b_types = self.b_types
        
        if lat == None and lng == None:
            lat = self.lat
            lng = self.lng

        b_types = b_types[:type_tolerance]
        print(b_types)

        results = self.gmaps.places_nearby(location=(lat, lng), radius=radius, type = b_types)

        if results['status'] != "OK":
            return None
        
        self.nearby_places = results["results"]

        return results["results"]
    
    def get_detailed_info(self, place_id):
            result = self.gmaps.place(place_id=place_id)

            if result['status'] != "OK":
                return None
            
            return result['result']