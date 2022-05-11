#!/usr/bin/env python

import sys
import os
import argparse

import dotenv
dotenv.load_dotenv()
import yaml

import asfpy.pubsub
import asfpy.syslog

PUBSUB_URL = 'https://pubsub.apache.org:2070/'
WATCHED_REPOS = 'svn/commit'
logger = asfpy.syslog.Printer(identity='agenda-syncer')


def process_event(payload):
    if 'stillalive' not in payload:
        print(f"{payload['pubsub_path']}->{payload['commit']['id']}")

def main(argv):
    parser = argparse.ArgumentParser(description='ASF Agenda Syncer')
    parser.add_argument('--debug', action='store_true',
                        help='Run in "debug" mode')
    parser.add_argument('--config', action='store',
                        help='Specify config file')
    args = parser.parse_args(argv)
    config = yaml.safe_load(open(args.config))

    listener = asfpy.pubsub.Listener(PUBSUB_URL + WATCHED_REPOS)
    if 'auth' in config:
        auth_tuple = (config.auth.user, config.auth.password)
    elif 'AGENDA_SYNCER_USER' in os.environ:
        auth_tuple = (os.environ.get('AGENDA_SYNCER_USER'), os.environ.get('AGENDA_SYNCER_PASS'))
    else:
        auth_tuple = None

    listener.attach(process_event, raw=True, debug=args.debug, auth=auth_tuple)

if __name__ == '__main__':
    main(sys.argv[1:])