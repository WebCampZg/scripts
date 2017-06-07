#!/usr/bin/env python
from __future__ import print_function

import fileinput
import json
import logging
import os
import sys

from urllib.request import urlopen, Request
from urllib.error import HTTPError


def abspath(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))


def error_exit(msg):
    logging.error(msg)
    print(msg, file=sys.stderr)
    sys.exit(1)

# Setup logging
LOG_FORMAT = '%(asctime)s %(levelname)-7s %(message)s'
LOG_FILE = abspath(__file__ + '.log')

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
logging.info("---- Running ----")

# Load webhook URL from environment
slack_url = os.environ.get('WCZG_SLACK_HOOK')
if not slack_url:
    error_exit("Environment variable WCZG_SLACK_HOOK not set")

# Check stdin has some text
if sys.stdin.isatty():
    error_exit("Not text given in stdin")

# Load text from stdin
text = "".join([l for l in fileinput.input()])
if text == "":
    logging.info("No payload given. Exiting.")
    sys.exit()

# Form payload and send to slack
payload = json.dumps({
    "text": text
})

# Send to slack
logging.info("Sending data to Slack")

try:
    request = Request(slack_url, payload.encode('utf-8'))
    response = urlopen(request).read()
except HTTPError as e:
    error_exit("HTTP %d %s: %s" % (e.code, e.reason, e.read()))

logging.info("Done")
