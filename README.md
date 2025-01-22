# WebDiver_light_scanner
The WebDiver is a tool that takes a lot of other tools and put in a single one. It's mission is to make the process of selection of the subdomain much clear.

Keep in mind that this tool is under development, so it'll contain bugs

The script is writen with python, so make sure it's installed in our computer

INSTALLING:

To install, run the python script: 'dependences.py'


>>  *sudo python3 dependences.py*

This script will install all the features that the WebDiver requires to work properly

After that, you can run the script.

>>  *sudo python3 start_api.py*

The WebDiver make use of the FLASK (the link to the official site is below)

https://flask.palletsprojects.com/en/stable/


SCANNING:

This tool is developed specially for BugBounty, but it can be used for pentest or to protect your own site.

!BE SURE YOU HAVE THE PERMISSION OF THE SITE OWNER TO USE THIS TOOL, IT CAN CREATE A LOT OF TRAFFIC!

First, configure the 'start_api.py' file. Locate the savepath and configure it to your WebDiver file. If not properly configured, it'll not work

DETAIL: if you are using a computer to connect to the server that contains this script, modify the IP of the WebDiver and script.js files. The default IP ins 127.0.0.1. Make sure you change this to the server IP

After that, you can go to the site

![Captura de tela de 2025-01-22 17-26-26](https://github.com/user-attachments/assets/e79449e3-5069-4afd-af18-6c4538042a79)

The site is quite simple, just a page with a input and a button

This is the report page, you'll se your reports there

A important thing to understand is that this script use a PROJECT system, so you can save your scans in different files

So, when your scan starts, the domains/subdomains will appear there

To start a scan, you need to go to the "Create Scan" anchor

![Captura de tela de 2025-01-22 17-30-00](https://github.com/user-attachments/assets/2f72444e-242e-40ce-ba70-65d73781fc13)

There is two inputs and  a button to send the data.

A wildcard is a domain that you want to look for subdomains

For example, if the scope of a program is:
*google.com*
*youtube.com*
*facebook.com*

You'll need to put in the input:
*google.com,youtube.com,facebook.com*

And the other input you can put a name for the project

After that, you can press "Create new scan"

it'll scan the wildcards and look for simple vulnerabilitites, such as XSS, SQLI, LFI, and some CVEs
