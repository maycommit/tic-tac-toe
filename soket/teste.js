
const WebSocket = require('ws');
var socket = new WebSocket('ws://localhost:8096');

socket.onopen = function () {
    alert("alerting you");
    socket.send('Pingel');
};

