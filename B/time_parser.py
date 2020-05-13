import re

file = open("routes.txt", "r").readlines()

all_averages = []

# Main logic for script
def main():
    total_list = parse_routes()

    count = 1

    for traceroute in total_list:
        if len(traceroute) > 0:
            total_time = 0

            size = len(traceroute)
            final_hop = traceroute[size - 1].split("  ")  # Get final hop in traceroute

            for word in final_hop:
                if " ms" in word:  # ie. it's a ping reading
                    num = get_ping_from_text(word)
                    total_time += num

            all_averages.append((count, round(total_time / 3, 3)))
            count += 1

    print_list(all_averages)


# Parses the routes.txt file, grouping the lines into their respective traceroutes.
# (I now realise I could have just split this by multiple new lines but hey that's no fun right? :D)
def parse_routes():
    current_index = 0
    size = len(file)
    total_list = [[]]

    while current_index <= size:
        current_list, index = consume_hops([], current_index + 1)
        total_list.append(current_list)
        current_index = index

    return total_list


# Recursively parses through the file, consuming any hops it finds until it gets the next single number (ie. the start
# of the next traceroute.
def consume_hops(current_list, index):
    if index >= len(file):  # Final check, prevents searching more times than possible bug.
        return current_list, index

    line = file[index].rstrip()

    if re.match("^[0-9]{0,2}$", line) and len(current_list) > 0 and line != "":  # ie. Start of next traceroute
        return current_list, index  # Returns the list and the terminating index

    elif re.match("^[0-9]{0,2}[ ]", line):  # ie. It's a hop
        current_list.append(line)
    return consume_hops(current_list, index + 1)


# Gets the ping from text
def get_ping_from_text(string):
    return float(string.split()[0])


# Util to print list in a nice format
def print_list(items):
    for item in items:
        print(item)

# Called upon execution
if __name__ == "__main__":
    main()
