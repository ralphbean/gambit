#!/usr/bin/env python
""" Store messages from the exchange in a mongodb.. db. """

import json
import pymongo
import time
import zmq


def setup_zeromq():
    connect_to = 'ipc:///var/tmp/wtf-node.zmq_socket'
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)
    s.setsockopt(zmq.SUBSCRIBE, '')
    return s


def setup_mongo():
    client = pymongo.MongoClient("localhost", 27017)
    return client.bitcoin, client


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
    except KeyboardInterrupt:
        pass
    print "Exiting."


if __name__ == "__main__":
    main()
