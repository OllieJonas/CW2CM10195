import google_api
import hops_handler

# https://developers.google.com/places/web-service/supported_types


def main():
    latitude, longitude = -45.095234, 170.969653  # Latitude and Longitude for Wellington, NZ
    type = "church"
    websites = []
    results = []

    place_request = google_api.perform_place_request(latitude, longitude, type)
    place_json = place_request.json()
    place_request.close()

    place_results = place_json["results"]

    print("Found " + str(len(place_results)) + " results!")
    print("Finding places of interest...")

    places_of_interest = google_api.generate_places_of_interest(place_results)

    print("Found " + str(len(places_of_interest)) + " places of interest!")

    for place in places_of_interest:
        details_request = google_api.perform_details_request(place)
        details_json = details_request.json()
        details_request.close()

        if "result" in details_json and "website" in details_json["result"]:
            website = details_json['result']['website']
            websites.append(website)

    print("Found " + str(len(websites)) + " websites!")

    for i in range(0, len(websites)):
        website = websites[i]
        command = hops_handler.traceroute_command(website)

        if command is not None:
            results += command

    if len(results) > 0:
        print(hops_handler.sort(results))
        print("The most amount of hops found was " + str(hops_handler.sort(results)[0]))
    else:
        print("Error: No routes found! :(")
    pass


if __name__ == "__main__":
    main()
