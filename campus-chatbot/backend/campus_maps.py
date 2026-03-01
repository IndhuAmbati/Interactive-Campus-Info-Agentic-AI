import googlemaps
from geopy.geocoders import Nominatim

class CampusMapService:
    def __init__(self, api_key=None):
        self.gmaps = googlemaps.Client(key=api_key) if api_key else None
        self.geolocator = Nominatim(user_agent="campus_chatbot")
        
    def get_building_location(self, building_name):
        """Get coordinates and map link for building"""
        location = self.geolocator.geocode(f"{building_name}, [Your College Name]")
        if location:
            return {
                'name': building_name,
                'address': location.address,
                'lat': location.latitude,
                'lng': location.longitude,
                'map_url': f"https://www.google.com/maps?q={location.latitude},{location.longitude}"
            }
        return None