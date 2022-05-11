#!/usr/bin/env python

import os

from dotenv import load_dotenv
load_dotenv()

import asfpy.pubsub
import asfpy.syslog

PUBSUB_URL = 'https://pubsub.apache.org:2070/'
WATCHED_REPOS = 'svn/commit'
AUTH = (os.environ.get('AGENDA_SYNCER_USER'), os.environ.get('AGENDA_SYNCER_PASS'))
logger = asfpy.syslog.Printer(identity='agenda-syncer')


def process_event(payload):
    if 'stillalive' not in payload:
        print(f"{payload['pubsub_path']}->{payload['commit']['id']}")

def main():
    listener = asfpy.pubsub.Listener(PUBSUB_URL + WATCHED_REPOS)
    listener.attach(process_event, raw=True, debug=True, auth=AUTH)

if __name__ == '__main__':
    main()