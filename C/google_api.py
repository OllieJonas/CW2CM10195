import requests
import json


API_KEY = "REDACTED"  # For obvious reasons, I haven't included my Google API key
MAPS_URL = "https://maps.googleapis.com/maps/api"


# Builds the details request to the Google API. Only fetches the website.
def build_details_request(place_id):
    return requests.get(MAPS_URL + "/place/details/json", params={
        "key": API_KEY,
        "place_id": place_id,
        "fields": "website"
    })


# Builds the place request to the Google API. Either can find by radius or rankby distance.
# NOTE: Can't have rankby distance and radius in the same request
# https://developers.google.com/places/web-service/supported_types
def build_place_request(latitude, longitude, type):
    return requests.get(MAPS_URL + "/place/nearbysearch/json", params={
        "key": API_KEY,
        "location": str(latitude) + "," + str(longitude),
        # "radius": 1500,
        "rankby": "distance",  # Don't want popular results - we want random ones
        "type": type
    })


def build_next_page_place_request(next_page_token):
    return requests.get(MAPS_URL + "/place/nearbysearch/json", params={
        "key": API_KEY,
        "next_page_token": next_page_token
    })


# Prints formatted JSON message. Used for debugging
def print_formatted(result):
    print(json.dumps(result, indent=4, sort_keys=True))


