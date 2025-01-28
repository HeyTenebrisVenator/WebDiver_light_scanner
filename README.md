# WebDiver_light_scanner

V1.2

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

![Captura de tela de 2025-01-28 12-05-21](https://github.com/user-attachments/assets/4418792b-26bc-47a1-bf24-e21af55f3ce8)

The site is quite simple, just a page with a input and a button

This is the report page, you'll se your reports there

A important thing to understand is that this script use a PROJECT system, so you can save your scans in different files

So, when your scan starts, the domains/subdomains will appear there

To start a scan, you need to go to the "Create Scan" anchor

![Captura de tela de 2025-01-28 12-05-26](https://github.com/user-attachments/assets/ad34d28c-2ed1-4fd2-948a-c2b59ffdac03)


The new update brought some new features in the report

Now, you can make notes, hidden them, and save

You can see the projects and delete them at the web site
