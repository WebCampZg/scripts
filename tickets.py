#!/usr/bin/env python
import json
import logging
import os
import re
import sys

from urllib.request import urlopen
from urllib.error import HTTPError


def abspath(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

# Setup logging
LOG_FORMAT = '%(asctime)s %(levelname)-7s %(message)s'
LOG_FILE = abspath(__file__ + '.log')

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
logging.info("---- Running ----")

# Load API key from environment
api_key = os.environ.get('WCZG_ENTRIO_API_KEY')
if not api_key:
    msg = "Environment variable WCZG_ENTRIO_API_KEY not set"
    logging.error(msg)
    print(msg, file=sys.stderr)
    sys.exit(1)

# File where processed codes are saved
STATE_FILE = abspath(__file__ + '.dat')

# Create state file if it doesn't exist
if not os.path.isfile(STATE_FILE):
    open(STATE_FILE, 'a').close()

# Read processed ticket codes
with open(STATE_FILE, 'r') as f:
    codes = f.read().split('\n')
    if '' in codes:
        codes.remove('')

# Read from API
logging.info("Reading from API...")

try:
    url = 'https://www.entrio.hr/api/get_visitors?key=%s&format=json' % api_key
    response = urlopen(url)
except HTTPError as e:
    logging.error(e)
    print(e)

js = response.read()
data = json.loads(js.decode('utf-8'))


def get_custom_field(record, name):
    fields = [
        f for k, f in record['custom_fields'].items()
        if name.lower() in f['name'].lower() ]
    if fields:
        return fields[0]['value']


# Iterate over dataset, collect new names
names = []
for record in data:
    code = record['ticket_code']
    category = record['ticket_category']
    if code not in codes:
        category = re.sub(r"\(.+", "", record["ticket_category"]).strip()
        first_name = get_custom_field(record, 'First name')
        last_name = get_custom_field(record, 'Last name')
        company_name = get_custom_field(record, 'Company name')
        name = f'{first_name} {last_name}, {company_name} ({category})'
        names.append(name)
        codes.append(code)

# Stop in no new names found
if not names:
    logging.info("No new tickets found")
    sys.exit(0)
else:
    logging.info("Found %d new tickets" % len(names))

# Compose notification
text = "New tickets sold:"
for name in names:
    text += "\n * %s" % name
text += "\n\n Total sold: %d" % len(codes)

# Write to stdout
print(text.strip())

# Save processed codes
with open(STATE_FILE, 'w') as f:
    f.write('\n'.join(codes))
