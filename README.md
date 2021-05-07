# Vaccine Pinger

## Installation
1. Install python 3 and pip in your machine
2. Clone this repo
3. cd into the directory where this repo is cloned and first run the following command
```
pip install -r requirements.txt
```

## Steps to run the script
1. Run this script with the following command and provide the arguments in the exact order they appear
```
    python vaccine_script.py <your_email_id> <pincode 1> <pincode 2> <pincode 3> <age_limit>
```
2. In the above command the required parameters are your email id and pincodes. You can provide any number of pincodes
3. Followed by all the pincodes comes age_limit which is option. If you do not provide age_limit it will list out centers for 18+ and 45+ as well. If you need centers for specific age limits, the accepted values are 18 or 45
4. Given below is a sample run
```
python .\vaccine_script.py vinitramk@gmail.com 400601 400607 400083 400086 400079 421301 18
```

## Notes
- The above code will run till 23:59 everyday unless you stop it
- Start the code and keep it running in the background in your machine. Closing or shutting down machine will ofcourse stop the script
- On getting a hit the attached mp3 file will played.
- This script is looking for slots available from the current day to next 7 days. It won't list out slots for the next month, just the very next week.
- Currently the email functionality is buggy and will update the functionality for it later once it's completely stable