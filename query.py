#!/usr/bin/env python

import requests
import time
import twilio
import logging
import sys

from twilioConfig import account_sid
from twilioConfig import auth_token
from twilioConfig import recp
from twilioConfig import twilio_number

logging.basicConfig(filename="query.log",
                    level=logging.INFO,
                    format="%(levelname)s %(asctime)s %(message)s",
                    datefmt="%Y/%m/%d-%H:%M")
logger = logging.getLogger(__name__)


def sendMessage(msg="Error connecting to server"):

    to = recp
    from_ = twilio_number

    try:
        client = twilio.rest.TwilioRestClient(account_sid, auth_token)
        client.messages.create(body=msg, to=to, from_=from_)
        logger.info("Sent twilio message with content {}".format(msg))

    except twilio.TwilioRestException as e:
        logger.error("Could not send twilio message: {}".format(e))

domain = "https://api.btcmarkets.net/"
uri = "market/BTC/AUD/tick"
url = domain + uri

try:
    r = requests.get(url, verify=True)
except requests.exceptions.RequestException as e:
    logger.error(e)
    sys.exit(1)

ask = str(r.json()["bestAsk"])
last = str(r.json()["lastPrice"])
tstamp = r.json()["timestamp"]
ltime = time.ctime(tstamp)
utime = time.asctime(time.gmtime(tstamp))

msg = """
    BTCMarkets has BTC for ${0} accurate at {1}. Last trade price was ${2}.
    """.format(ask, ltime, last)

if float(ask) > 680 or float(ask) < 450:
    sendMessage(msg)
else:
    logger.info("Msg not sent due to price range: {}".format(ask))
