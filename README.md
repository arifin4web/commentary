Commentary
========

A simple application to demonstrate WebSocket Broadcasting using Django Channels.

Anyone can add feeds to any events and all the connected users
will get live updates.

This is a very simple application to demonstrate the Broadcasting to websockets using Django Channels.
Quickly Prepared to show a demo on PyConDhaka'16. Inspired and primarily borrowed from [Andrew Godwin](https://github.com/andrewgodwin)'s official
[liveblog](https://github.com/andrewgodwin/channels-examples/tree/master/liveblog) example.


Installation
------------

Make a new virtualenv for the project, and run::

    pip install -r requirements.txt

You'll need Redis running locally; the settings are configured to
point to ``localhost``, port ``6379``, but you can change this in the
``CHANNEL_LAYERS`` setting in ``settings.py``.

Finally, run::

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver


Usages
------------
- From the admin dashboard create public events from.
- In the event page anyone can give/add commentary/feed.
- All connected users will get live update.


Further Reading
---------------

You can find the Channels documentation at http://channels.readthedocs.org
