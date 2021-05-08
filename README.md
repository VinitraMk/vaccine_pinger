# Vaccine Pinger

## Pre-requisites
1. Go to this link, to turn on access for your gmail account to send emails. This setting is to allow the python script to send email to yourself. [Click Here](https://myaccount.google.com/lesssecureapps)
2. Turn on the toggle of 'Allow less secure apps'.
3. Now when you provide your gmail username and password to the script, the script can login to your gmail account, compose the mail for available slots and send it yourself.
4. Without these steps, the script won't be able send email. If you don't want email notifications, you can skip this step entirely.

## Installation
1. Install python 3 and pip in your machine
2. Clone this repo
3. cd into the directory where this repo is cloned and first run the following command
```
pip install -r requirements.txt
```

## Steps to run the script
1. run the script with the following command
```
python vaccine_script.py
```
2. The script will ask for email, your gmail password, district id to search by, pin codes to filter on and if you want to receive email notifications
3. The above script will search by district and then filter out by pincodes provided and list the available slots in the centers. On getting a hit the attached mp3 file will played.

## Notes
- The above code will run till 23:59 everyday unless you stop it
- Start the code and keep it running in the background in your machine. Closing or shutting down machine will ofcourse stop the script
- On getting a hit the attached mp3 file will played.
- This script is looking for slots available from the current day to next 7 days. It won't list out slots for the next month, just the very next week.