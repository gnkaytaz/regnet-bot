import json
import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


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
            response = "Privet Likusa! :-)p"
            #response = "latitude:{} longitude:{}".format(data["location"]["latitude"], data["location"]["longitude"])
            logger.info(data)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        logger.info("post_url:{}".format(url))
        logger.info("post_data:{}".format(data))
        requests.post(url, data)

    except Exception as e:
        print("Exeption")
        print(e)

    return {"statusCode": 200}
