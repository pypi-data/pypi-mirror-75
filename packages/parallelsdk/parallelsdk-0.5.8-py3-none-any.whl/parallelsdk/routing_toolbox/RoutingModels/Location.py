import json
import urllib.request
import numpy as np


class Location:
    def __init__(self, position=None, address='', demand=0.0, location_id=-1):
        self.unique_id = id(self)
        self.location_id = location_id
        self.position = position
        self.address = address
        self.demand = demand

        if self.position is not None:
            self.transform_list_coords_into_array()

    def get_unique_id(self):
        return self.unique_id

    def get_id(self):
        return self.location_id

    def set_address(self, address):
        self.address = address

    def get_address_for_geocoding(self):
        address = self.address
        address = address.replace(",", "")
        address = address.replace(" ", "+")
        return address

    def get_address(self, API_key):
        if self.address:
            return self.address

        # Get actual address with reverse geocoding
        request = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(self.position[0]) + \
                  ',' + str(self.position[1]) + '&key=' + API_key
        with urllib.request.urlopen(request) as url:
            json_result = url.read()
            response = json.loads(json_result)
            status = response['status']
            if status != 'OK':
                raise Exception('Error while retrieving reverse geocoding coordinates for coordinates ' +
                                str(self.position[0]) + ',' + str(self.position[1]))
            self.address = response['results'][0]['formatted_address']
        return self.address

    def transform_list_coords_into_array(self):
        if not isinstance(self.position, list):
            return
        if len(self.position) == 2:
            self.position = np.ndarray((2,), buffer=np.array([self.position[0], self.position[1]]), dtype=float)

    def set_coordinates(self, position):
        self.position = position
        self.transform_list_coords_into_array()

    def get_coordinates(self, API_key):
        """Returns latitude/longitude of the location's address"""
        if self.position is not None and self.position.size == 2:
            return self.position

        address = self.get_address_for_geocoding()
        request = 'https://maps.googleapis.com/maps/api/geocode/json' + '?address=' + address + '&key=' + API_key
        with urllib.request.urlopen(request) as url:
            json_result = url.read()
            response = json.loads(json_result)
            status = response['status']
            if status != 'OK':
                raise Exception('Error while retrieving geocoding coordinates for address ' + self.address)
            lat = response['results'][0]['geometry']['location']['lat']
            lng = response['results'][0]['geometry']['location']['lng']
            self.position = np.ndarray((2,), buffer=np.array([lat, lng]), dtype=float)
            return self.position


class Depot(Location):
    def __init__(self, position=None, address=''):
        super().__init__(position=position, address=address, location_id=0)
