<h1>Traceroute Finder</h1>

<h2> Introduction </h2>

This script is to help guide findings for Part C of CM10195 (Systems Architecture 2 - Operating Systems and Networking)
Coursework 2.

In this, we were asked to find routes across the Internet that are:

1.  As many hops
2. Take the largest amount of time
3. Are as geographically seperate

as we could find.

<h2> Implementation </h2>
To do this, I decided to implement a Python script that essentially takes 4 steps. These are as follows:

1. Using the Google Maps API, the script scans any given area for a given type of establishment (these are defined by 
Google Maps, please see the link below). 

2. Using the results from Step 1, it then requests each place's website from it's Place ID.
 
3. Using the results from Step 2, it then then executes a traceroute command, which alters based on the OS you're using
(and also stops if there were too many unknown hops in the traceroute).

4. After finding all the traceroute, it then finds the website that used the most hops to get to it.

<h3> Libraries </h3>

To do this, I used the following libraries: 

Regex - Format the websites into a format that the traceroute command can use (ie. remove any http://, https://, etc.)

Requests - Make HTTP GET Requests to the Google API. 

JSON - Mainly for debugging requests made by Google
 
Platform - Find out the operating system the user is using.
 
Subprocess - Execute the traceroute command and get all output from the console from this command.

<h2> Links </h2>

https://developers.google.com/places/web-service/search
https://developers.google.com/places/web-service/details
https://developers.google.com/places/web-service/supported_types


