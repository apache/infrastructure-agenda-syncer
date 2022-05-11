#!/usr/bin/env python

import asfpy.pubsub
import asfpy.syslog

PUBSUB_URL = 'https://pubsub.apache.org:2070'
PUBSUB_TOPICS = '/svn/commit'
logger = asfpy.syslog.Printer(identity='agenda-syncer')


def process_event(payload):
    if 'stillalive' not in payload:
        print(payload['pubsub_path'])

def main():
    listener = asfpy.pubsub.Listener(PUBSUB_URL + PUBSUB_TOPICS)
    listener.attach(process_event, raw=True)

if __name__ == '__main__':
    main()