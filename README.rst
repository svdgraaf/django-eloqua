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

And here are some optional settings::
    ELOQUA_PROFILE_TIMEOUT = 60 * 60 * 24  # the default amount of time, a profile data is cached in the database
    ELOQUA_BASE_URL = 'https://secure.eloqua.com/API/REST/1.0'  # you might want to override the default base url (eg: local reverse proxy, etc)

Usage
=====

You can access the functionality through the EloquaClient, eg, sending a mail::
    
    from eloqua.clients import EloquaClient
    e = EloquaClient()
    e.emails.create('foobar-name', 'foobar-subject', 'my-body')
    # etc. See the docstrings

By default, the user models gets extended with a eloqua_profile property. The matching is done by email address. If the user is found in Eloqua, the contact id is stored locally for future reference::
    
    from django.contrib.auth.models import User
    u = User.objects.get(pk=1)
    print u.eloqua_profile.first_name, u.eloqua_profile.last_name
    # prints 'foo bar' (or whatever is stored in Eloqua)

You can also get an arbitrary contact field for this user::

    from django.contrib.auth.models import User
    u = User.objects.get(pk=1)
    u.eloqua_profile.value_for_field(100171)  # this is the default Eloqua domain field
    # prints 'example.com' (or whatever is stored in Eloqua)

You can also use the commandline tool, eg::
    
    $ ./application/manage.py send_mail_from_url --url=http://www.example.com/
    # this will fetch the url, and create a mail in Eloqua with the body of that url
    # the default subject/name will be the title of the page (via BeautifulSoup), you
    # can pass extra variables for the subject and reply-to etc

Roadmap
=======

- Landingpages (to be able to include them)
- Coupling/syncing with a django user model?
- Using Eloqua as a standard smtp django backend, perhaps?
- ...
- Moar... I mainly focussed on the Contacts, Email and Landingpage sections, as that was the stuff we needed the most. Implementing the other features would be fairly trivial, so get cracking and send in a pull request :)