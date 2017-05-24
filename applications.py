#!/usr/bin/env python
from __future__ import print_function

import os
import psycopg2
import sys


def abspath(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

# File where the last processed application ID is stored
STATE_FILE = abspath(__file__ + '.dat')

# PK of the currently active cfp
CFP_ID = 3


def get_last_id():
    # Create state file if it doesn't exist
    if not os.path.isfile(STATE_FILE):
        open(STATE_FILE, 'a').close()

    # Read processed ticket codes
    with open(STATE_FILE, 'r') as f:
        try:
            last_id = int(f.read())
        except ValueError:
            last_id = 0

    return last_id


def save_last_id(last_id):
    with open(STATE_FILE, "w") as f:
        f.write(str(last_id))


def get_applications(conn, last_id):
    query = """
        SELECT pa.id, pa.title, u.first_name, u.last_name
          FROM cfp_paperapplication pa
          JOIN cfp_applicant a ON a.id = pa.applicant_id
          JOIN people_user u ON u.id = a.user_id
         WHERE cfp_id = %d AND pa.id > %d
    """ % (CFP_ID, last_id)

    # Load data from database
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def get_application_count(conn):
    query = """
        SELECT COUNT(*)
          FROM cfp_paperapplication
         WHERE cfp_id = %d
    """ % CFP_ID

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()[0][0]

# Connect to database
conn = psycopg2.connect(database="webcampdb")

# Fetch applications
last_id = get_last_id()
apps = get_applications(conn, last_id)
app_count = get_application_count(conn)

if not apps:
    sys.exit(1)

# Print to stdout
print("New applications:")
for app in apps:
    print("* %s %s: %s" % (app[2], app[3], app[1]))
print("Application count: %d" % app_count)

#  Save the last processed ID
last_id = max([app[0] for app in apps])
save_last_id(last_id)
