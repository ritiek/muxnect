import libtmux
import flask
import sys

SESSION = 'muxnect'

app = sys.argv[1:]
parent, *_ = app[0].split()

server = libtmux.Server()
session = server.new_session(SESSION)
window = session.new_window(parent)
session.kill_window('@0')
pane = window.attached_pane

pane.send_keys(' '.join(app))
