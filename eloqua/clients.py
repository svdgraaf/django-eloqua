from eloqua import settings
from eloqua.exceptions import ObjectNotFound
import requests
import base64
import json


class EloquaBaseClient(object):
    headers = ''
    base_url = settings.BASE_URL

    def __init__(self):
        key = '{site}\\{username}:{password}'.format(site=settings.SITE, username=settings.USERNAME, password=settings.PASSWORD)
        authKey = base64.b64encode(key)
        self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + authKey}

    def get(self, identifier):
        """Return the asset by the given id"""
        return self._get_by_id(identifier)

    def _get_by_id(self, identifier):
        url = self.base_url + '/' + str(identifier)
        print url
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ObjectNotFound(identifier)

    # Delete asset by id, return True or False when succesful
    def _delete_by_id(self, identifier):
        url = self.base_url + '/' + str(identifier)
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            return False

    def delete(self, identifier):
        """Deletes the asset by the given id"""
        return self._delete_by_id(identifier)

    def search(self, query, page=1, count=100, depth='complete'):
        url = self.base_url + 's'
        payload = {
            'search': query,
            'page': page,
            'count': count,
            'depth': depth,
        }

        r = requests.get(url, params=payload, headers=self.headers)
        return r.json()


class EloquaClient(EloquaBaseClient):
    headers = ''
    base_url = settings.BASE_URL

    @property
    def emails(self):
        return EloquaEmailClient()

    @property
    def email_groups(self):
        return EloquaEmailGroupsClient()

    @property
    def contacts(self):
        return EloquaContactsClient()

    @property
    def contact_fields(self):
        return EloquaContactFieldsClient()

    @property
    def landingpages(self):
        return EloquaLandingPagesClient()


class EloquaEmailClient(EloquaBaseClient):
    # only get/search need the slash
    base_url = settings.BASE_URL + '/assets/email'

    def create(self, name, subject, body, body_plaintext=None, group_id=None, is_tracked=False, folder_id=None, sender_name=None, sender_email=None, reply_to_email=None, reply_to_name=None):
        """Creates an email with the given parameters, returns a json representation"""
        payload = {
            'htmlContent': {
                'html': body,
                'type': 'RawHtmlContent',
            },
            'sendPlainTextOnly': False,
            'name': name,
            'subject': subject,
            'id': None,
            'isTracked': is_tracked,
        }

        if folder_id:
            payload['folderId'] = folder_id

        # only add, if provided, otherwise, let the system generate one
        if body_plaintext:
            payload['body_plaintext'] = body_plaintext

        if group_id:
            payload['emailGroupId'] = group_id

        if sender_email:
            payload['senderEmail'] = sender_email
        if sender_name:
            payload['senderName'] = sender_name

        if reply_to_email:
            payload['replyToEmail'] = reply_to_email
        if reply_to_name:
            payload['replyToName'] = reply_to_name

        # make the call
        # TODO: logging?
        r = requests.post(self.base_url, data=json.dumps(payload), headers=self.headers)
        if r.status_code == 201:
            return r.json()
        else:
            raise Exception('error: %s' % r)  # TODO: be more verbose


class EloquaContactsClient(EloquaBaseClient):
    # only get/search need the slash
    base_url = settings.BASE_URL + '/data/contact'

    def search(self, query, page=1, count=100, depth='complete'):
        """Search all contacts for given email query, eg:

            from eloqua.lib import *
            e = EloquaClient()
            e.contacts.search('foobar@example.com')
                {u'elements': [{u'createdAt': u'1327661283',
                u'currentStatus': u'Awaiting action',
                u'depth': u'complete',
                u'emailAddress': u'foobar@example.com',
                ...

        """
        url = self.base_url + 's'
        payload = {
            'search': query,
            'page': page,
            'count': count,
            'depth': depth,
        }

        r = requests.get(url, params=payload, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise ObjectNotFound(None)


class EloquaContactFieldsClient(EloquaBaseClient):
    base_url = settings.BASE_URL + '/assets/contact/field'

    def search(self, query, page=1, count=100, depth='complete'):
        url = self.base_url + 's'
        payload = {
            'search': query,
            'page': page,
            'count': count,
            'depth': depth,
        }

        r = requests.get(url, params=payload, headers=self.headers)
        return r.json()


class EloquaEmailGroupsClient(EloquaBaseClient):
    base_url = settings.BASE_URL + '/assets/email/group'

    def search(self, query, page=1, count=100, depth='complete'):
        url = self.base_url + 's'
        payload = {
            'search': query,
            'page': page,
            'count': count,
            'depth': depth,
        }

        r = requests.get(url, params=payload, headers=self.headers)
        return r.json()


class EloquaLandingPagesClient(EloquaBaseClient):
    base_url = settings.BASE_URL + '/assets/landingPage'
