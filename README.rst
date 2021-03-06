muxnect
=======

|Pypi Version| |Build Status|

Send input to just about any interactive command-line tool through a local
web server.

muxnect is a tool that invokes tmux to create a session and then wraps
around its method of sending mouse-events or key-strokes to the terminal
through a local web server.

Security Note
-------------

Since there is no way to authenticate at the moment, please use this tool only on systems (and local networks) you completely trust. If an attacker somehow gets to know the URL muxnect is listening on, **nothing stops them from running arbitrary shell commands and completely mess you up.** Please take care!

Quick Introduction
------------------

A bare-bones method to muxnect any interactive CLI tool:

.. code:: bash

    $ muxnect -w <tmux_window_name> -c <some_interactive_tool>

Now just nail up some POST requests to
http://localhost:6060/muxnect/tmux_window_name

Let's try using Python:

.. code:: python

    >>> import requests
    >>> url = 'http://localhost:6060/muxnect/<tmux_window_name>'
    >>> requests.post(url, data={'keys': 'wonderful keystrokes'})
    <Response [200]>

That's it, our web server just sent ``wonderful keystrokes`` to
``<some_interactive_tool>``.

Examples
--------

Okay, that probably left you confused.

Here are some cool examples to cover up:

Hello World - Python
~~~~~~~~~~~~~~~~~~~~

Here we'll print hello world in Python through muxnect.

Let's call muxnect to launch a Python console where it is supposed to
print hello world:

.. code:: bash

    $ muxnect -w hello_world -c python

Now hook up another Python console and using it let's send a POST
request to muxnect's server:

.. code:: python

    >>> import requests
    >>> url = 'http://localhost:6060/muxnect/hello_world'
    >>> hello_world = 'print("Hello World!")'
    # send return key after it is done sending `keys`
    >>> requests.post(url, data={'keys':hello_world, 'enter':'true'})
    <Response [200]>

(of course, you can use any good way to make POST requests and not just
stay limited to Python requests)

There's our ``Hello World!`` on the Python console we launched through
muxnect.

Now, let's go through the ``separator`` parameter:

.. code:: python

    # send KeyboardInterrupt after sending keys
    >>> requests.post(url, data={'keys':'send Ctrl+c; C-c', 'separator':'; '})
    <Response [200]>
    # separator will split keys to preserve any special keys
    # here it will send "send Ctrl+c" and then immediately "C-c" (Ctrl+c, KBInterrupt)
    # you can use any number of separator blocks in `keys` param

    # try similar code without using separators
    >>> requests.post(url, data={'keys':'no Ctrl+c; C-c'})
    <Response [200]>
    # note how it sends raw keys directly

    # send return key and EOF (Ctrl+d) to end our python session
    >>> requests.post(url, data={'keys':'Enter; C-d', 'separator':'; '})
    <Response [200]>

Separators are helpful when we need to send a combination of
raw keys and special keys. Without it, the ``key`` param will be
interpreted rawly.

From the `tmux official docs <http://man.openbsd.org/OpenBSD-current/man1/tmux.1#KEY_BINDINGS>`__,
here are all the special keys that may be used:

    tmux allows a command to be bound to most keys, with or without a prefix key.
    When specifying keys, most represent themselves (for example ‘A’ to ‘Z’).
    Ctrl keys may be prefixed with ‘C-’ or ‘^’, and Alt (meta) with ‘M-’.
    In addition, the following special key names are accepted:
    Up, Down, Left, Right, BSpace, BTab, DC (Delete), End, Enter, Escape,
    F1 to F12, Home, IC (Insert), NPage/PageDown/PgDn, PPage/PageUp/PgUp, Space, and Tab.

We're done. Exit the running tmux session in muxnect with Ctrl+d.

Control Media Playback
~~~~~~~~~~~~~~~~~~~~~~

For a real-world example, let's try controlling media playback in
`mpv-player <https://github.com/mpv-player/mpv>`__.

You can install ``mpv`` from apt if you don't have it already.

Let's play some video though mpv using muxnect:

.. code:: bash

    $ muxnect -w playback -c "mpv --loop-file https://github.com/mediaelement/mediaelement-files/raw/master/big_buck_bunny.mp4"

Hold on for the video to show up and then we'll send input to this
running instance of mpv:

.. code:: python

    >>> import requests
    >>> url = 'http://localhost:6060/muxnect/playback'
    # space key pauses the video in mpv by default
    >>> requests.post(url, data={'keys':' '})
    <Response [200]>
    
    # capture all visible textual content from the tmux pane
    >>> response = requests.post(url, data={'capture-pane': True})
    >>> print(response.text)
    """
    me@hostname:~ $  mpv --loop-file https://github.com/mediaelement/mediaelement-files/raw/master/big_buck_bunny.mp4
    Playing: https://github.com/mediaelement/mediaelement-files/raw/master/big_buck_bunny.mp4
     (+) Video --vid=1 (*) (h264 640x360 23.962fps)
     (+) Audio --aid=1 --alang=eng (*) (aac 2ch 22050Hz)
    AO: [pulse] 22050Hz stereo 2ch float
    VO: [opengl] 640x360 yuv420p
    AV: 00:00:38 / 00:01:00 (64%) A-V:  0.000 Cache:  9s+1MB
    """
    
    # fetch this terminal session's window title
    >>> response = requests.post(url, data={'window-title': True})
    >>> response.text
    'me@hostname: ~'
    # this maybe nice depending if the tool you want to muxnect sets a
    # a custom title to the pane sesion which could be useful to us

    # kill this tmux window
    >>> requests.post(url, data={'kill':'true'})
    <Response [200]>

Syntactic Sugar
---------------

muxnect also provides a simple API for Python to make POST requests:

.. code:: python

    >>> import muxnect
    >>> url = 'http://localhost:6060/muxnect/cute_cli'
    >>> client = muxnect.Client(url, default_data={'enter':'true'})
    >>> client.send('type this, press enter and kill session', data={'kill':'true'})

Installation
------------

You must have `tmux <https://github.com/tmux/tmux>`__ installed to use
this. You may have to install it from source, if it ain't in
your `apt` repositories.

muxnect works best with Python 3.

Install the latest stable release from pypa:

::

    $ pip install muxnect

Or install the latest development version:

::

    $ git clone https://github.com/ritiek/muxnect
    $ cd muxnect
    $ python setup.py install

Usage
-----

::

    usage: muxnect [-h] -c CMD -w WINDOW_NAME [-d] [-s SESSION_NAME]
                     [-b BIND_ADDRESS] [-p PORT]

    Send input to just about any interactive command-line tool through a local web
    server

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

The URL is generated in the form:

::

    http://<hostaddress>:<port>/<session_name>/<window_name>

The POST request can take the following parameters:

::

    keys - mouse events/keystrokes to send (Default: None)
    separator - split `keys` parameter on a character or string (Default: None)
    enter - send enter key immediately after sending `keys` (Default: False)
    window-title - get current window title for the terminal session (Default: False)
    capture-pane - capture text visible in the current pane (Default: False)
    kill - kill tmux window after proceeding with any other params (Default: False)

Extending Further
-----------------

There are some other interesting things you could do, such as the ability to control videos running on your laptop
which is placed meters away from you - with an android app such as `HTTP-Shortcuts <https://github.com/Waboodoo/HTTP-Shortcuts>`_ (built by `@Waboodoo <https://github.com/Waboodoo>`_) which can be used to create custom HTTP requests.

License
-------

|License|

.. |Pypi Version| image:: https://img.shields.io/pypi/v/muxnect.svg
   :target: https://pypi.org/project/muxnect/
.. |Build Status| image:: https://travis-ci.org/ritiek/muxnect.svg?branch=master
   :target: https://travis-ci.org/ritiek/muxnect
.. |License| image:: https://img.shields.io/github/license/ritiek/muxnect.svg
   :target: https://github.com/ritiek/muxnect/blob/master/LICENSE
