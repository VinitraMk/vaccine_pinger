import requests
import sys
import re
import threading
import datetime
from time import sleep
import aiohttp
import asyncio
import json
import smtplib
from email.message import EmailMessage
from playsound import playsound

def prepare_urls(base_url, pincodes, age_limit):
    today = datetime.date.today().strftime('%d-%m-%Y')
    urls = []
    for pin in pincodes:
        url = f'{base_url}?pincode={pin}&date={today}'
        urls.append({"url": url, "pincode": pin})
    return urls

def isSlotAvailableInX(x, age_limit):
    valid_ages = []
    if age_limit == '18' or age_limit == '45':
        valid_ages = [age_limit]
    else:
        valid_ages = ['18', '45']
    sessions = x['sessions']
    available_sessions = [y for y in sessions if (y['available_capacity'] > 0 and y['min_age_limit'] in valid_ages)]
    if len(available_sessions) > 0:
        return x

def getCenterDetails(center):
    center_detail = f'Center Id: {center["center_id"]}\nName: {center["name"]}\nAddress: {center["address"]}\nBlock Name: {center["block_name"]}\nPincode: {center["pincode"]}'
    return center_detail

def send_email(user_email, centers):
    msg = EmailMessage()
    msg['Subject'] = 'Available Slots'
    msg['From'] = 'vinitramk@gmail.com'
    msg['To'] = user_email
    message_str = '\n\n'.join([getCenterDetails(c) for c in centers])
    print(message_str)
    msg.set_content(message_str)

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

def play_victory():
    for i in range(3):
        music_file = './queen-we-are-the-champions.mp3'
        playsound(music_file, False)

async def start_notification_service(urls, age_limit, user_email):
    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    today = datetime.datetime.now()
    async with aiohttp.ClientSession() as session:
        while today < tomorrow:
            c = 0
            for url in urls:
                print(f'\nChecking for pincode {url["pincode"]}\n')
                async with session.get(url["url"], headers={'cache-control': 'no-cache', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}) as resp:
                    if resp.status == 200:
                        centers = await resp.json()
                        centers = centers['centers']
                        available_centers = [slot for slot in [isSlotAvailableInX(x, age_limit) for x in centers] if slot]
                        if len(available_centers) > 0:
                            print(f'Centers for pin {url["pincode"]}: ',available_centers,'\n')
                            #send_email(user_email, available_centers)
                            play_victory()
                            c = c + 1
                        else:
                            print('No centers available :-(\n')
                    else:
                        print(f'Request for pin {url["pincode"]} failed: ',resp.status)
                    await asyncio.sleep(3)
            if c == len(urls):
                exit()
        

def main():
    base_api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    valid_age_limits = ['ALL','18','45']
    pincode_regex = "[0-9]+"
    c=0
    
    if len(sys.argv)==1:
        print('\nNo pincodes provided or age limit provided! :-|\n')
    else:
        all_args_len = len(sys.argv[1:])
        age_limit = sys.argv[-1]
        user_email = sys.argv[1]
        all_pincodes = []
        if sys.argv[-1] in valid_age_limits:
            age_limit = sys.argv[-1]
            all_pincodes = sys.argv[2:all_args_len]
        else:
            age_limit = 'ALL'
            all_pincodes = sys.argv[2:]

        for pin in all_pincodes:
            if len(pin)==6 and re.match(pincode_regex, pin):
                c = c + 1
            else:
                print(f'Pin {pin} is invalid')
                exit()

        if c == len(all_pincodes):
            print('All inputs are valid\n')
            print('All pincodes:',all_pincodes)
            print('Age limit', age_limit)
            print('\nSahi pincode check karke dalna tera responsibility hai, code sirf 6 number ka string check karne wala hai. Yede log ki tarah mumbai ka pincode ka badle delhi ka mat dalna. :-D\n')
            final_urls = prepare_urls(base_api_url, all_pincodes, age_limit)
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(start_notification_service(final_urls, age_limit, user_email))

main()