=============
django-eloqua
=============

Eloqua implementation for Django, WIP!

Requirements
============
django >= 1.4
requests >= X

Installation
============
Installation is easiest done via pip::

    $ pip install django-eloqua

Setup
=====

Add this to your settings.py::

    ELOQUA_SITE_ = 'ACME.Inc'
    ELOQUA_USERNAME = 'my-api-user'
    ELOQUA_PASSWORD = 'my-api-user-password'

Todo
====

Lot's, I mainly focussed on the Contacts, Email and Landingpage sections, as that was the stuff we needed the most. Implementing the other features would be fairly trivial, so get cracking and send in a pull request :)