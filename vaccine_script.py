import requests
import sys
import re
import threading
import datetime
from time import sleep, time
import aiohttp
import asyncio
import json
import smtplib
from email.message import EmailMessage
from playsound import playsound

def prepare_url(base_url, district_id):
    today = datetime.date.today().strftime('%d-%m-%Y')
    url = f'{base_url}?district_id={district_id}&date={today}'
    return url

def isSlotAvailableInX(x, age_limit):
    valid_ages = []
    if age_limit == '18' or age_limit == '45':
        valid_ages = [int(age_limit)]
    else:
        valid_ages = [18, 45]
    sessions = x['sessions']
    available_sessions = [y for y in sessions if (y['available_capacity'] > 0 and y['min_age_limit'] in valid_ages)]
    if len(available_sessions) > 0:
        return x

def getCenterDetails(center):
    center_detail = f'Center Id: {center["center_id"]}\nName: {center["name"]}\nAddress: {center["address"]}\nBlock Name: {center["block_name"]}\nPincode: {center["pincode"]}'
    return center_detail

def send_email(user_email, user_password, centers):
    msg = EmailMessage()
    msg['Subject'] = 'Available Slots'
    msg['From'] = user_email
    msg['To'] = user_email
    message_str = '\n\n'.join([getCenterDetails(c) for c in centers])
    #print(message_str)
    msg.set_content(message_str)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    #s.set_debuglevel(True)
    s.ehlo()
    s.starttls()
    s.login(user_email, user_password)
    s.sendmail(user_email, user_email, msg.as_string())
    s.quit()

def play_victory():
    end = time() + 180
    while time() < end:
        music_file = './notification.mp3'
        playsound(music_file, False)
        sleep(2)

def start_notification_service(url, age_limit, pincodes, user_email, user_password):
    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    today = datetime.datetime.now()
    s = requests.Session()
    while today < tomorrow:
        resp = s.get(url, headers={'cache-control': 'no-cache', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
        if resp.status_code == 200:
            centers = resp.json()
            centers = centers['centers']
            available_centers = [slot for slot in [isSlotAvailableInX(x, age_limit) for x in centers if str(x['pincode']) in pincodes] if slot]
            if len(available_centers) > 0:
                print(f'Centers: ',available_centers,'\n')
                if send_email == 'y':
                    send_email(user_email, user_password, available_centers)
                play_victory()
            else:
                print('No centers available :-(\n')
        else:
            print(f'Request for pin {url["district_id"]} failed: ',resp.status_code)
        sleep(3)
        

def main():
    base_api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    valid_age_limits = ['ALL','18','45']
    pincode_regex= "[0-9]+"
    c=0

    user_email = input("Enter your email: ")
    user_password = input("Enter your gmail password so you get notifications from your own email: ")
    district_id = input("Enter district id you are looking in: ")
    pincodes = input("Enter pin codes to filter in districts separated by spaces: ").split(" ")
    age_limit = input("Enter age limit. For all ages, enter all else enter 18 or 45: ")
    send_email = input("Do you want to receive email notifications of available slots? [y/n]")

    
    for pin in pincodes:
        if len(pin) == 6 and re.match(pincode_regex, pin):
            c = c + 1
        else:
            print(f'District id {pin} is invalid')
            exit()

    if c == len(pincodes):
        print('All inputs are valid\n')
        print('District:', district_id)
        print('All pincodes:',pincodes)
        print('Age limit', age_limit)
        print('\nSahi district id check karke dalna tera responsibility hai. Yede log ki tarah mumbai ka district ka badle delhi ka mat dalna. :-D\n')
        final_url = prepare_url(base_api_url, district_id)
        start_notification_service(final_url, age_limit, pincodes, user_email, user_password, send_email)

main()