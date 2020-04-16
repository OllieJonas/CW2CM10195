import requests
import json

# https://developers.google.com/places/web-service/supported_types

# NOTE: Can't have rankby distance and radius in the same request

API_KEY = "AIzaSyAtNORY9ab5WPNEpB8zSEYIeKVAXZFDl5w"
GOOGLE_MAPS = "https://maps.googleapis.com/maps/api"


def main():
    latitude, longitude = -41.28666552, 174.772996908  # Latitude and Longitude for Wellington, NZ
    #
    # request = place_request(latitude, longitude)
    # place_json = request.json()
    # next_page_token = place_json["next_page_token"]
    # results = place_json["results"]
    #
    # places_of_interest = generate_places_of_interest(results)
    #
    # print(json.dumps(place_json, indent=4, sort_keys=True))

    request = perform_place_request(latitude, longitude)
    request.close()
    return


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
    return requests.get(GOOGLE_MAPS + "/place/details/json", params={
        "key": API_KEY,
        "place_id": place_id,
        "fields": "name,website"
    })


def perform_place_request(latitude, longitude):
    return requests.get(GOOGLE_MAPS + "/place/nearbysearch/json", params={
        "key": API_KEY,
        "location": str(latitude) + "," + str(longitude),
        # "radius": 1500,
        "rankby": "distance",
        "type": "restaurant"})  # Don't want popular results; we want random ones


def print_formatted(result):
    print(json.dumps(result, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
