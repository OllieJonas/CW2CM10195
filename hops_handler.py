from subprocess import Popen, PIPE
import re

test_websites = ["google.co.uk", "yahoo.co.uk"]
UNKNOWN_COUNT_THRESHOLD = 8


def traceroute_command(website):
    website_formatted = format_website(website)
    print("Executing Traceroute Command for " + website_formatted)
    result = []
    process = Popen(["traceroute", "-m", "255", website_formatted], stdout=PIPE)
    unknown_count = 0

    for line in iter(process.stdout.readline, ''):
        if line == b'' and process.poll() is not None:  # If stream has finished
            break
        else:
            line_str = "".join(chr(x) for x in bytearray(line)).strip("\n")  # Convert byte stream to string
            print(line_str)

            # Ensures we don't end up with too many unknown hops
            if "* * *" in line_str:
                unknown_count += 1
                if unknown_count > UNKNOWN_COUNT_THRESHOLD:
                    process.kill()
                    print("Error: Traceroute for " + website_formatted + " has been killed - too many unknown hops\n")
                    return None
            elif line_str.split()[0].isnumeric():  # ie. this is a hop
                result.append(line_str)
            else:
                pass

    print("Completed traceroute for " + website_formatted)
    return result


def format_website(website):
    return re.split("[/?]", website)[2]


def sort(results):
    return sorted(results, reverse=True)


def minsec(time):
    return str(int(time / 60)) + "m " + str(time % 60) + "s"


if __name__ == "__main__":
    formatted = format_website("https://www.google.co.uk?test")
    print(formatted)
    formatted = format_website("http://www.google.co.uk")
    print(formatted)


