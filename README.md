WebCamp helper scripts
======================

Quick and dirty scripts to provide Slack notifications for sold tickets and
CFP applications.

applications.py
---------------

Writes new CFP applications to stdout.

Requires that it's possible to connect to Postgres. You can use
[environment variables](http://www.postgresql.org/docs/9.1/static/libpq-envars.html)
to setup the user/password and other settings.

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

Sample setup
------------

In your crontab, have something like:

```
PGUSER=webcamp
PGPASSWORD=secret
WCZG_ENTRIO_API_KEY=0123456789ABCDEF
WCZG_SLACK_HOOK=https://hooks.slack.com/services/ABCD/EFGH/foobar

2-59/5 * * * * (cd /home/webcamp/scripts && (./tickets.py | ./slack-notify.py))
4-59/5 * * * * (cd /home/webcamp/scripts && (./applications.py | ./slack-notify.py))
```