WebCamp helper scripts
======================

Quick and dirty scripts to provide Slack notifications for sold tickets and
CFP applications.

applications.py
---------------

Writes new CFP applications to stdout.

Requires that it's possible to connect to Postgres as current user without a
password.


tickets.py
----------

Writes new ticket notification to stdout.

Requires WCZG_ENTRIO_API_KEY environment variable populated with the Entrio API
key.


slack-notify.py
---------------

Sends the text recieved as standard input as a notification to slack.

Requires WCZG_SLACK_HOOK environemnt variable populated with the URL of a
Slack Webhook to which to post the notifications.

See Custom Integrations > Incoming WebHooks in Slack team settings.
