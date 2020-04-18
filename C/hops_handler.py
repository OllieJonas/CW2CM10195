from subprocess import Popen, PIPE
import re
import platform

UNKNOWN_COUNT_THRESHOLD = 8


# Executes traceroute command for the website given
def execute_traceroute_command(website):
    website_formatted = format_website(website)  # Remove any unnecessary http stuff in string
    result = []
    unknown_count = 0

    process = Popen(get_traceroute_command_syntax(website), stdout=PIPE)  # 255 hops
    print("Executing Traceroute Command for " + website_formatted)

    for line in iter(process.stdout.readline, ''):
        if line == b'' and process.poll() is not None:  # If stream has finished
            break
        else:
            line_str = "".join(chr(x) for x in bytearray(line)).strip("\n")  # Convert byte stream to string

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


# Returns the syntax for the traceroute command based on OS (Windows has a slightly different format to UNIX-based
# operating systems.
def get_traceroute_command_syntax(website):
    if is_windows():
        return ["tracert", "-h", 255, website]
    else:
        return ["traceroute", "-m", "255", website]


# Removes any http business or anything at the end (eg. https://, http://, .nz?, .nz/)
def format_website(website):
    return re.split("[/?]", website)[2]


# Reverses list
def sort(results):
    return sorted(results, reverse=True)


# Returns a boolean for whether the platform running this script is Windows or not.
# (Included this because I use both Linux and Windows)
def is_windows():
    return "Windows" in platform.system()







