import os
import pprint
import sys
import time
from random import randint
from sys import platform as _platform

import requests


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

CONCERTS = {
    'roskilde': 1,
    'northside': 2,
    'tinderbox': 3,
    'nibe': 4,
    'vig': 5,
    'samsoe': 6,
    'groen_koncert': 7,
    'langeland': 8,
}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'

def enter_lottery(phone_number, selected_concert):

    headers = {
        'User-Agent': USER_AGENT,
        'Referer': 'http://www.tuborgmusik.dk/skruop/?e=1'
    }
    r = requests.post(
        'http://tuborg-skruop-production.herokuapp.com/api/v2/tickets',
        headers=headers,
        data = {
            'data[lottery_id]': selected_concert,
            'data[msisdn]': phone_number
        }
    )
    result = r.json()

    data = {
        'data[permission]': False,
        'data[lottery_id]': selected_concert,
        'data[msisdn]': phone_number,
        'data[id]': result["data"]["id"],
        'data[key]': random_with_N_digits(8),
    }

    time.sleep(randint(3, 7))
    next_r = requests.patch(
        'http://tuborg-skruop-production.herokuapp.com/api/v2/tickets/'+str(result["data"]["id"]),
        headers=headers,
        data=data
    )
    json = next_r.json()

    if json["data"]["win"]:
        if _platform == "darwin":
            os.system('say "there is a winner"')
        print("############################")
        print("########## WINNER ########## ")
        print("############################")



if __name__ == "__main__":
    if len(sys.argv) == 3:
        while True:
            enter_lottery(sys.argv[1], CONCERTS[sys.argv[2]]);
    else:
        print("missing arguments")
