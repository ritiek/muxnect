import libtmux
from flask import Flask, request
import sys

SESSION = 'muxnect'

app = sys.argv[1:]
parent, *_ = app[0].split()
print(parent)

server = libtmux.Server()
session = server.new_session(SESSION)
window = session.new_window(parent)
session.kill_window('@0')
pane = window.attached_pane

pane.send_keys(' '.join(app))


app = Flask(__name__)

@app.route('/muxnect/<window_name>', methods=['POST'])
def handle_request(window_name):
    window = session.find_where({'window_name': window_name})

    if 'enter' in request.form:
        enter = int(request.form['enter'])
    else:
        enter = False

    if 'suppress_history' in request.form:
        suppress_history = int(request.form['suppress_history'])
    else:
        suppress_history = False

    pane = window.attached_pane
    pane.send_keys(request.form['keys'],
                   enter=enter,
                   suppress_history=suppress_history)

    if 'kill' in request.form:
        if int(request.form['kill']):
            window.kill_window()

    return '200'


if __name__ == '__main__':

    app.run(host='0.0.0.0', threaded=True, port=6060)
