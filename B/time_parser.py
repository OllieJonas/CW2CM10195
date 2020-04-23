import re

file = open("routes.txt", "r").readlines()

all_averages = []


def main():
    total_list = do_recursion()

    count = 1

    for traceroute in total_list:
        if len(traceroute) > 0:
            total_time = 0

            size = len(traceroute)
            final_hop = traceroute[size - 1].split("  ")

            for word in final_hop:
                if " ms" in word:
                    num = get_ping_from_text(word)
                    total_time += num

            all_averages.append((count, round(total_time / 3, 3)))
            count += 1

    print_list(all_averages)


def recursion(current_list, index):
    if index >= len(file):  # Final check
        return current_list, index

    line = file[index].rstrip()

    if re.match("^[0-9]{0,2}$", line) and len(current_list) > 0 and line != "":
        return current_list, index  # Returns the list and the terminating index

    elif re.match("^[0-9]{0,2}[ ]", line):
        current_list.append(line)

    return recursion(current_list, index + 1)


# I now realise I could have just split this by multiple new lines but hey that's no fun right? :D
def do_recursion():
    current_index = 0
    size = len(file)
    total_list = [[]]

    while current_index <= size:
        current_list, index = recursion([], current_index + 1)
        total_list.append(current_list)
        current_index = index

    return total_list


def get_ping_from_text(string):
    return float(string.split()[0])


def print_list(items):
    for item in items:
        print(item)


if __name__ == "__main__":
    main()
