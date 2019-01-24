import socketio, time
from flask import Flask

import threading

class My_server:

    sio = socketio.Server(async_mode='threading')

    def make_server(self):
        app = Flask(__name__)
        app.wsgi_app = socketio.Middleware(self.sio, app.wsgi_app)
        app.run()

    def run_server(self):
        threading.Thread(target=self.make_server).start()

    def send_data(self, key="FRAME", data = "DATA"):

        self.sio.emit(key, data)


