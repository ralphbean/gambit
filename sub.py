#!/usr/bin/env python

import json
import pprint
import zmq


def main():
    connect_to = 'ipc:///var/tmp/wtf-node.zmq_socket'
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)

    s.setsockopt(zmq.SUBSCRIBE,'')

    try:
        while True:
            msg = s.recv()
            msg = json.loads(msg)
            pprint.pprint(msg)
    except KeyboardInterrupt:
        pass
    print "Done."


if __name__ == "__main__":
    main()
