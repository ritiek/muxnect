# muxnect

[![Build Status](https://travis-ci.org/ritiek/muxnect.svg?branch=master)](https://travis-ci.org/ritiek/muxnect)

Send input to just about any interactive command-line tool.

muxnect is a tool that invokes tmux to create a session and then
wraps around its method of sending mouse-events or key-strokes
to the terminal through a local web server.

## Quick Introduction

A bare-bones method to muxnect any interactive CLI tool:
```bash
$ muxnect -w nice_app -c <some_interactive_tool>
```

Now just nail up some POST requests to http://localhost:6060/muxnect/nice_app:

Let's try using Python:
```python
>>> import requests
>>> url = 'http://localhost:6060/muxnect/nice_app'
>>> requests.post(url, data={'keys': 'wonderful keystrokes'})
<Response [200]>
```

That's it, our web server just sent `wonderful keystrokes`
to `<some_interactive_tool>`.

## Examples

Okay, that probably left you confused.

Here are some cool examples to cover up:

### Hello World - Python

Here we'll print hello world in Python through muxnect.

Let's call muxnect to launch a Python console where it is
supposed to print hello world:
```bash
$ muxnect -w hello_world -c python
```

Now hook up another Python console and using it let's send a POST
request to muxnect's server:
```python
>>> import requests
>>> url = 'http://localhost:6060/muxnect/hello_world'
>>> keys = 'print("Hello World!")'
# send return key after it is done sending `keys`
>>> requests.post(url, data={'keys':keys, 'enter':'true'})
<Response [200]>
# send EOF (Ctrl+d) to session
>>> requests.post(url, data={'keys':'C-d'})
<Response [200]>
```

(of course, you can use any good way to make POST requests and not just stay
limited to Python requests)

There's our `Hello World!` on the Python console we launched through muxnect.

We're done. Exit the running tmux session in muxnect with <kbd>Ctrl</kbd>+<kbd>d</kbd>.

### Control Media Playback

For a real-world example, let's try controlling media playback in
[mpv-player](https://github.com/mpv-player/mpv).

You can install `mpv` from apt if you don't have it already.

Let's play some video though mpv using muxnect:

```bash
$ muxnect -w playback -c "mpv --loop-file https://github.com/mediaelement/mediaelement-files/raw/master/big_buck_bunny.mp4"
```

Hold for the video to show up and now then send input to this
running instance of mpv:
```python
>>> import requests
>>> url = 'http:'//localhost:6060/muxnect/playback'
# space key pauses the video in mpv by default
>>> requests.post(url, data={'keys':' '})
# kill this tmux session
>>> requests.post(url, data={'kill':'true'})
<Response [200]>
```

## Syntactic Sugar

muxnect also provides a simple API for Python to make POST requests:
```python
>>> import muxnect
>>> url = 'http://localhost:6060/muxnect/cute_cli'
>>> client = muxnect.Client(url, default_data={'enter':'true'})
>>> client.send('type this, press enter and kill session', data={'kill':'true'})
```

## Installation

Install the latest stable release from pip:
```
pip install muxnect
```

Install the latest development version:
```
git clone https://github.com/ritiek/muxnect
cd muxnect
python setup.py install
```

## Usage

```
usage: muxnect [-h] -c CMD -w WINDOW_NAME [-d] [-s SESSION_NAME]
                 [-b BIND_ADDRESS] [-p PORT]

Send input to just about any interactive command-line tool

optional arguments:
  -h, --help            show this help message and exit
  -d, --detach          detach from ongoing session (default: False)
  -s SESSION_NAME, --session-name SESSION_NAME
                        tmux's session name (default: muxnect)
  -b BIND_ADDRESS, --bind-address BIND_ADDRESS
                        address to bind on, local network: 0.0.0.0 (default:
                        127.0.0.1)
  -p PORT, --port PORT  port number to listen on (default: 6060)

required arguments:
  -c CMD, --cmd CMD     interactive command to send input to (default: None)
  -w WINDOW_NAME, --window-name WINDOW_NAME
                        tmux's window name (default: None)
```

#### Why `muxnect` though?

tmux + connect = muxnect :heart:

## License

[![License](https://img.shields.io/github/license/ritiek/muxnect.svg)](https://github.com/ritiek/muxnect/blob/master/LICENSE)
