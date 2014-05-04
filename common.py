""" Common stuff for all python processes. """

import pymongo
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
