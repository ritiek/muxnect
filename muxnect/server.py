from flask import Flask, request
import libtmux
from libtmux.exc import *

from distutils import util
import threading
import argparse


app = Flask(__name__)

def get_arguments():
    parser = argparse.ArgumentParser(
        description='Send input to just about any interactive command-line tool',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '-c', '--cmd',
        required=True,
        type=str,
        help='interactive command to send input to')

    parser.add_argument(
        '-d', '--detach',
        action='store_true',
        help='detach from ongoing session')
    parser.add_argument(
        '-s', '--session-name', default='muxnect',
        type=str,
        help='tmux\'s session name')
    parser.add_argument(
        '-w', '--window-name', default='mpsyt',
        type=str,
        help='tmux\'s window name')
    parser.add_argument(
        '-b', '--bind-address', default='127.0.0.1',
        type=str,
        help='address to bind on, local network: 0.0.0.0')
    parser.add_argument(
        '-p', '--port', default=6060,
        type=int,
        help='port number to listen on')

    return parser.parse_args()


def query_exists(query, data):
    if query in data:
        return util.strtobool(data[query])
    else:
        return False


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


def command_line():
    args = get_arguments()
    session_name = args.session_name
    window_name = args.window_name
    detach = args.detach
    cmd = args.cmd

    print(window_name)

    try:
        server = libtmux.Server()
        session = server.new_session(session_name)
        window = session.new_window(window_name)
        session.kill_window('@0')
        pane = window.attached_pane
        pane.send_keys(cmd)

    except TmuxSessionExists:
        pass

    web_app_args = {'host':'0.0.0.0', 'threaded':True, 'port':6060}
    web_app = threading.Thread(target=app.run, kwargs=web_app_args)
    web_app.start()
    if not detach:
        session.attach_session()

    try:
        window.kill_window()
    except LibTmuxException:
        pass


if __name__ == '__main__':

    command_line()
