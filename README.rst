Thoughts on a bitcoin autotrader based on scikit-learn.

The only exchange I could find with a streaming websockets api was bitstamp.
The only client libraries it has for its special websockets gig are for
javascript and iOS.  Therefore, we have this stupid nodejs daemon sitting in
the front, getting live orders from bitstamp.  We then just republish those
locally over zeromq to a whole bunch of independent python processes.

We store every order that happens in mongo, to use for training our
market model later.

We also grab the current price and associate it with orders from a couple
seconds/minutes ago in the database.

We also train a model periodically on the data.  It looks at what series of
orders were coming along, and then what the price *became* a few
seconds/minutes from then.

Hopefully, then, this model can predict what the price will be in a few
seconds/minutes based on whatever buy/sell activity is happening right now.

Profit.

::

   |    +---------------+
   |    | nodejs        |
   |    +---------------+
   |--->| pusher-client |
   |    |       |       |
   |    |       V       |   +-----------------------+
   |    |   zeromq-pub  |-+>| python                |
   |    +---------------+ | +-----------------------+
   |                      | | store orders in mongo |
   |                      | +-----------------------+
   |                      |
   |                      | +---------------------------+
   |                      +>| python                    |
   |                      | +---------------------------+
   |                      | | associate current price   |
   |                      | | with previous orders      |
   |                      | | store in mongo            |
   |                      | +---------------------------+
   |                      |
   |                      | +---------------------------+
   |                      +>| python                    |
   |                      | | periodically re-train     |
   |                      | | sklearn model based on    |
   |                      | | new data                  |
   |                      | +---------------------------+
   |                      |
   |                      | +---------------------------+
   |                      +>| python                    |
   |                        +---------------------------+
   |                        | buy/sell based on model   |
   |                        | price predictions         |
   |                        | sklearn model based on    |
   |                        | new data                  |
   |                        +---------------------------+
