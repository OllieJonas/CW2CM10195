import requests
import json

# https://developers.google.com/places/web-service/supported_types

# NOTE: Can't have rankby distance and radius in the same request

API_KEY = open("google_api_key.txt", "r").read()  # For obvious reasons, I haven't pushed my Google API key
MAPS_URL = "https://maps.googleapis.com/maps/api"


# Uses all results to get the places of interest. (filters out the user ratings to be under 30).
#
# NOTE: This is entirely arbitrary; it just helps to remove any larger companies that may have come from abroad, and
# therefore their website would be based somewhere else. There is no scientific data to support this assumption;
# I made to help narrow down the results to minimise requests to the Google API. It could potentially be worth testing
# this hypothesis.
def generate_places_of_interest(results):
    places_of_interest = []

    for result in results:
        place_id = result["place_id"]

        if "user_ratings_total" in result:
            user_ratings_total = result["user_ratings_total"]
            if user_ratings_total < 30:
                places_of_interest.append(place_id)

    return places_of_interest


# Executes the details request to the Google API. Only fetches the website.
def execute_details_request(place_id):
    print("Executing request for details on " + place_id)
    return requests.get(MAPS_URL + "/place/details/json", params={
        "key": API_KEY,
        "place_id": place_id,
        "fields": "website"
    })


# Executes the place request to the Google API. Either can find by radius or rankby distance.
def perform_place_request(latitude, longitude, type):
    print("Finding all " + type + "(e)s in local area of " + str(latitude) + ", " + str(longitude))
    return requests.get(MAPS_URL + "/place/nearbysearch/json", params={
        "key": API_KEY,
        "location": str(latitude) + "," + str(longitude),
        # "radius": 1500,
        "rankby": "distance",  # Don't want popular results; we want random ones
        "type": type
    })


def print_formatted(result):
    print(json.dumps(result, indent=4, sort_keys=True))


