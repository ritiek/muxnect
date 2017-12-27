import libtmux
from libtmux.exc import *
from flask import Flask, request
import sys
import threading
from distutils import util

SESSION = 'muxnect'

app = sys.argv[1:]
parent, *_ = app[0].split()
print(parent)

try:
    server = libtmux.Server()
    session = server.new_session(SESSION)
    window = session.new_window(parent)
    session.kill_window('@0')
    pane = window.attached_pane
    pane.send_keys(' '.join(app))

except TmuxSessionExists:
    pass


def query_exists(query, data):
    if query in data:
        return util.strtobool(data[query])
    else:
        return False


app = Flask(__name__)

@app.route('/muxnect/<window_name>', methods=['POST'])
def handle_request(window_name):
    window = session.find_where({'window_name': window_name})

    enter = query_exists('enter', request.form)
    suppress_history = query_exists('suppress_history', request.form)

    pane = window.attached_pane
    pane.send_keys(request.form['keys'],
                   enter=enter,
                   suppress_history=suppress_history)

    if query_exists('kill', request.form):
        window.kill_window()

    return '200'


if __name__ == '__main__':
    web_app_args = {'host':'0.0.0.0', 'threaded':True, 'port':6060}
    web_app = threading.Thread(target=app.run, kwargs=web_app_args)
    web_app.start()
    session.attach_session()
    try:
        window.kill_window()
    except LibTmuxException:
        pass
