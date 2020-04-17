import requests
import json

# https://developers.google.com/places/web-service/supported_types

# NOTE: Can't have rankby distance and radius in the same request

API_KEY = open("google_api_key.txt", "r").read()
GOOGLE_MAPS = "https://maps.googleapis.com/maps/api"


def generate_places_of_interest(results):
    places_of_interest = []

    for result in results:
        place_id = result["place_id"]

        if "user_ratings_total" in result:
            user_ratings_total = result["user_ratings_total"]
            if user_ratings_total < 30:
                places_of_interest.append(place_id)

    return places_of_interest


def perform_details_request(place_id):
    print("Executing request for details on " + place_id)
    return requests.get(GOOGLE_MAPS + "/place/details/json", params={
        "key": API_KEY,
        "place_id": place_id,
        "fields": "name,website"
    })


def perform_place_request(latitude, longitude, type):
    print("Finding all " + type + "(e)s in local area of " + str(latitude) + ", " + str(longitude))
    return requests.get(GOOGLE_MAPS + "/place/nearbysearch/json", params={
        "key": API_KEY,
        "location": str(latitude) + "," + str(longitude),
        # "radius": 1500,
        "rankby": "distance",
        "type": type})  # Don't want popular results; we want random ones


def print_formatted(result):
    print(json.dumps(result, indent=4, sort_keys=True))


