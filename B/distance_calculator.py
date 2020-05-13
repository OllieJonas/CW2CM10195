import math

# Using https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python

DESTINATIONS = [
    (51.4502, -2.6503),  # Bristol
    (52.2242, 0.1315),  # Cambridge
    (51.7778, -1.26537),  # Oxford
    (55.9489, -3.1632),  # Edinburgh
    (51.0605, -114.1102),  # Calgary
    (29.508, -98.3942),  # Vancouver Island
    (0, 0),  # City of Uni of NY - Undefined
    (40.7608, -111.891),  # Utah
    (34.4265, -119.8631),  # UC Santa Barbara
    (21.3133, -157.823),  # Hawaii
    (-43.5321, 172.636),  # Uni of Canterbury NZ
    (37.4043, -122.0748),  # Google US
    (37.4043, -122.0748),  # Google UK
    (34.0522, -118.244),  # lax17s15-in-f78.1e100.net
    (51.514, -0.128349),  # Yahoo UK
    (51.4959, -0.132962),  # Channel 4
    (45.5235, -122.676),  # Twitch
    (29.8135, -95.4641),  # To
    (51.5074, -0.127758),  # BBC UK
    (40.7399, -73.9905),  # BBC In
]

BATH = (51.3782, 2.3264)

R = 6373.0  # Radius of Earth

distances = []


# Main logic, calculates distance between 2 lat/long coords using Haversine formula
def main():
    count = 1
    bath_lat, bath_long = math.radians(BATH[0]), math.radians(BATH[1])

    for coordinate in DESTINATIONS:
        lat, long = math.radians(coordinate[0]), math.radians(coordinate[1])
        dlat, dlong = bath_lat - lat, bath_long - long

        a = math.sin(dlat / 2) ** 2 + math.cos(lat) * math.cos(bath_lat) * math.sin(dlong / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distances.append((count, round(R * c)))
        count += 1

    print_list(distances)


def print_list(items):
    for item in items:
        print(item)


if __name__ == "__main__":
    main()


