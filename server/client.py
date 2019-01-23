import socketio

# standard Python
sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print("I'm connected!")

@sio.on('FRAME')
def on_message(data):
    print('I received FRAME!')
    print(data)

@sio.on('message')
def on_message(data):
    print('I received a custom message!')
    print(data)

@sio.on('disconnect')
def on_disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:8000')