#!/usr/bin/env python
""" Grab best ask/bid and associate with older order books """

import json
import time

from common import setup_zeromq, setup_mongo


delta = 60 * 60 # one hour


def main():
    s = setup_zeromq()
    db, client = setup_mongo()

    try:
        while True:
            msg = s.recv()
            msg = json.loads(msg)
            msg['timestamp'] = time.time()
            topic = msg.pop('topic')

            if 'asks' not in msg:
                continue

            best_ask = msg['asks'][0]
            best_bid = msg['bids'][0]

            # Fine all the books in the last bit
            end = now = time.time()
            start = end - delta

            old_books = db.order_book.find({
                "timestamp": {
                    "$gte": start,
                    "$lte": end,
                }
            });

            old_books = list(old_books)
            print "Processing %i old books" % len(old_books)

            for book in old_books:
                if 'future_spreads' not in book:
                    book['future_spreads'] = {}

                relative = now - book['timestamp']
                # Convert from seconds to ms, stringified int
                key = unicode(int(relative * 1000))
                book['future_spreads'][key] = {
                    'ask': best_ask,
                    'bid': best_bid,
                }
                result = db.order_book.save(book)

            print "Done."

    except KeyboardInterrupt:
        pass
    print "Exiting."


if __name__ == "__main__":
    main()
