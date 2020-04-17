from subprocess import Popen, PIPE
import re

test_websites = ["google.co.uk", "yahoo.co.uk"]
UNKNOWN_COUNT_THRESHOLD = 8


# Executes traceroute command for the website given
def execute_traceroute_command(website):
    website_formatted = format_website(website)  # Remove any unnecessary http stuff in string
    print("Executing Traceroute Command for " + website_formatted)
    result = []
    process = Popen(["traceroute", "-m", "255", website_formatted], stdout=PIPE)  # 255 hops
    unknown_count = 0

    for line in iter(process.stdout.readline, ''):
        if line == b'' and process.poll() is not None:  # If stream has finished
            break
        else:
            line_str = "".join(chr(x) for x in bytearray(line)).strip("\n")  # Convert byte stream to string
            print(line_str)

            if "* * *" in line_str:  # Ensures we don't end up with too many unknown hops
                unknown_count += 1
                if unknown_count > UNKNOWN_COUNT_THRESHOLD:
                    process.kill()
                    print("Error: Traceroute for " + website_formatted + " has been killed - too many unknown hops\n")
                    return None

            elif line_str.split()[0].isnumeric():  # ie. this is a hop
                result.append(line_str)

            else:  # ie. any other random stuff that the traceroute command prints (don't want this in the list)
                pass

    print("Completed traceroute for " + website_formatted)
    return result


# Removes any http business or anything at the end (eg. https://, http://, .nz?, .nz/)
def format_website(website):
    return re.split("[/?]", website)[2]


# Reverses list
def sort(results):
    return sorted(results, reverse=True)




