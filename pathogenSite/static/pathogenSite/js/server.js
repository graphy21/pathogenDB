var express = require('express');
var http = require('http');

app = express();

app.use(express.static('documentation'));
app.get('/', function (req, res) {
	res.sendFile('./documentation/index.html');
});

http.createServer(app).listen(9000, '147.46.65.202');
