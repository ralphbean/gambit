#!/usr/bin/env python
""" Store messages from the exchange in a mongodb.. db. """

import json
import pprint
import time

from common import setup_zeromq, setup_mongo


def main():
    s = setup_zeromq()
    db, client = setup_mongo()

    try:
        while True:
            msg = s.recv()
            msg = json.loads(msg)
            msg['timestamp'] = time.time()
            topic = msg.pop('topic')
            obj = getattr(db, topic).save(msg)
            print "Saved", obj
            pprint.pprint(msg)
    except KeyboardInterrupt:
        pass
    print "Exiting."


if __name__ == "__main__":
    main()
