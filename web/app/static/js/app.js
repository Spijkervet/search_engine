/*
    Boilerplate Python 3 SocketIO Flask app
*/

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    // socket.emit('connected', {data: 'Still connected'});
});

socket.on('pong', function() {
    socket.emit('ping', {data: 'Still connected'});
});


socket.on('update', function(data) {
    update(JSON.parse(data));
});


function update(data) {
    $("#version").text(data.version);
    $("#time").text(data.time);
}
