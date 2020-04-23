import google_api
import hops_handler

coordinates = [
    (-43.539930, 172.625851),
]

types = ["cafe", "church", "hindu_temple", "hospital", "mosque",
         "museum", "pet_store", "restaurant", "synagogue"]

COMMON_WEBSITES = ["www.facebook.com", "www.youtube.com"]


# Main method
def main():
    places_of_interest = []
    websites = []
    results = []

    for coord in coordinates:
        for place_type in types:
            place_results = execute_place_request(coord[0], coord[1], place_type)  # Gets all areas of type in the lat,long
            print("Found " + str(len(place_results)) + " results for " + place_type + "!")

            places_of_interest += generate_places_of_interest(place_results)  # Get places of interest from places in area

    print("Found " + str(len(places_of_interest)) + " total places of interest!")

    for place in places_of_interest:  # Fetch details from places of interest
        website = get_website_from_place_id(place)

        if website is not None:  # ie. Website exists and is not in common websites
            websites.append(website)

    print("Found " + str(len(websites)) + " websites!")
    print("Websites: " + str(websites))

    for website in websites:
        result = hops_handler.execute_traceroute_command(website)  # Execute traceroute for each website

        if result is not None:  # ie. the process hasn't been killed due to too many unknown hops
            results += result  # Append list

    if len(results) > 0:
        print(hops_handler.sort(results))  # Sort results by the one with the most hops (reversed)
        print("The most amount of hops found was " + str(hops_handler.sort(results)[0]))  # First = most hops
    else:
        print("Error: No routes found! :(")  # No results found from parsing hops


# Finds website from the given Place ID.

# Returns a string containing the website, if this can be found.
# Returns None if unable to find website
def get_website_from_place_id(place_id):
    print("Executing details request for " + place_id)

    details_request = google_api.build_details_request(place_id)
    details_json = details_request.json()
    details_request.close()

    if "result" in details_json and "website" in details_json["result"]:  # Parsing Google API JSON Response
        website = hops_handler.format_website(details_json['result']['website'])

        if website in COMMON_WEBSITES:
            print("Found a website for this ID, but it is a common one")
            return None
        else:
            print("Found website " + website)
            return website
    else:
        print("No website found for this ID")
        return None


# Executes place request with given latitude, longitude and type of place.
#
# Types are defined by Google API and can be found here:
# https://developers.google.com/places/web-service/supported_types
#
# Returns a dictionary
def execute_place_request(latitude, longitude, type):
    print("Finding all of type " + type + " in local area of " + str(latitude) + ", " + str(longitude))
    place_request = google_api.build_place_request(latitude, longitude, type)
    place_json = place_request.json()
    place_request.close()

    return place_json["results"]


# Uses all results to get the places of interest. (filters out the user ratings to be under 30).
#
# NOTE: This is entirely arbitrary; it just helps to remove any larger companies that may have come from abroad, and
# therefore their website would be based somewhere else. There is no scientific data to support this assumption;
# I made to help narrow down the results to minimise requests to the Google API. It could potentially be worth testing
# this hypothesis.

# Returns a list
def generate_places_of_interest(results):
    places_of_interest = []

    print("Finding places of interest...")

    for result in results:
        place_id = result["place_id"]

        if "user_ratings_total" in result:
            user_ratings_total = result["user_ratings_total"]
            if user_ratings_total < 30:
                places_of_interest.append(place_id)
    return places_of_interest


if __name__ == "__main__":
    main()
