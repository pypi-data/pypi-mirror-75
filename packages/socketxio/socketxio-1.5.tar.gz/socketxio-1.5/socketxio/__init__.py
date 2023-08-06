from socketxio.socketxio import socketxio

sockets = socketxio()

sockets.send_request('https://google.com', '{"Hello": "World"}')