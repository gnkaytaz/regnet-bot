import json
import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

def check_location(lat, long):
    data = {}
    data['status'] = 'ok'
    data['zone_id'] = '2429809'
    data['message'] = 'first check-in'
    return data

def zone_info(zone_id):
    data = {}
    data['zone_id'] = zone_id
    data['open_status'] = 'ok'
    data['start_time'] = '5/12/2016 8:50'
    data['end_time'] = '5/12/2018 8:50'
    data['bonus'] = 5000 #satoshi
    data['interval'] = 300 #seconds
    return data

def reply(response, chat_id):
        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

def hello(event, context):
    try:
        logger.info('EVENT:{}'.format(event))

        data = json.loads(event["body"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        response = "Please /start, {}".format(first_name)

        if "text" in data["message"]:
            message = str(data["message"]["text"])
            if "start" in message:
                response = "Hello {}".format(first_name)

        if "location" in data["message"]:
            location = check_location(data["message"]["location"]["latitude"],
                                          data["message"]["location"]["longitude"])
            if location['status'] == 'ok':
                zone = zone_info(location['zone_id'])
                response = str(zone)
                logger.debug(zone)
                logger.debug(response)

        reply(response, chat_id)



    except Exception as e:
        logger.error("Exeption")
        logger.error(e)

    return {"statusCode": 200}
