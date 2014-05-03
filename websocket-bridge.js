var zmq = require('zmq'),
    pusher = require('pusher-client');

var zmq_endpoint = 'ipc:///var/tmp/wtf-node.zmq_socket';
var zmq_socket = zmq.socket('pub');

// Post up to send stuff
zmq_socket.bind(zmq_endpoint, function(err) {
    if (err) throw err;
    console.log('bound to zmq ' + zmq_endpoint);

    // If we can do that, then subscribe to the exchange
    var bitstamp_key = 'de504dc5763aeef9ff52';
    var pusher_socket = new pusher(bitstamp_key);

    pusher_socket.connection.bind('connected', function(data) {
        console.log('connected to pusher ' + bitstamp_key);
    });

    pusher_socket.connection.bind('disconnected', function(data) {
        console.log('disconnected from pusher');
    });

    var channels = {
        live_trades: 'trade',
        order_book: 'data',
    };

    // And just forward stuff all day
    for (var topic in channels) {
        var channel_obj = pusher_socket.subscribe(topic);
        channel_obj.bind(channels[topic], function (data) {
            console.log("living the dream " + topic)
            data.topic = topic;
            zmq_socket.send(JSON.stringify(data));
        });
    }

    pusher_socket.connection.connect();
});
