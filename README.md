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

Now just hook up some POST requests to `http://localhost:6060/muxnect/nice_app:

Let's try using Python
```
import requests

url = 'http://localhost:6060/muxnect/nice_app'
requests.post(url, data={'keys': 'wonderful keystrokes'})
```

That's it, our web server just sent `wonderful keystrokes` to `<some_interactive_tool>`.

## Examples

Okay, that probably left you confused.

Here are some cool examples:

### Python Hello World

Here we'll print hello world in python through muxnect.

Let's call muxnect:
```bash
$ muxnect -w hello_world -c python
```

Now let's send a POST request using python to our newly created web-server:
```python
import requests

url = 'http://localhost:6060/muxnect/hello_world'
requests.post(url, data={'keys': 'print("Hello World!")'})
```

There's our `Hello World!` on the python console we just launched.
