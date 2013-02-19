=============
django-eloqua
=============

Eloqua implementation for Django, WIP!

Requirements
============
Django >= 1.4
Requests >= X

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

Usage
=====

You can access the functionality through the EloquaClient, eg, sending a mail::
    
    from eloqua import lib
    e = EloquaClient()
    e.emails.create('foobar-name', 'foobar-subject', 'my-body')
    # etc. See the docstrings

You can also use the commandline tool, eg::
    
    $ ./application/manage.py send_mail_from_url --url=http://www.example.com/
    # this will fetch the url, and create a mail in Eloqua with the body of that url
    # the default subject/name will be the title of the page (via BeautifulSoup), you
    # can pass extra variables for the subject and reply-to etc

Roadmap
=======

- Landingpages (to be able to include them)
- Coupling/syncing with a django user model?
- Using Eloqua as a default smtp django backend perhaps?
- ...
- Moar... I mainly focussed on the Contacts, Email and Landingpage sections, as that was the stuff we needed the most. Implementing the other features would be fairly trivial, so get cracking and send in a pull request :)