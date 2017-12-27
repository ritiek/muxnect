# muxnect

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
```

That's it, our web server just sent `wonderful keystrokes`
to `<some_interactive_tool>`.

## Examples

Okay, that probably left you confused.

Here are some cool examples to cover up:

### Python Hello World

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
>>> requests.post(url, data={'keys':keys, 'enter':True})
```

(ofcourse, you can use any good way to make POST requests and not just stay
limited with using Python to do it)

There's our `Hello World!` on the Python console we launched through muxnect.
