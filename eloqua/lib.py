from eloqua import settings
import requests
import base64
import json


class EloquaBaseClient(object):
    headers = ''
    base_url = settings.BASE_URL

    def __init__(self):
        key = '{site}\\{username}:{password}'.format(site=settings.SITE, username=settings.USERNAME, password=settings.PASSWORD)
        authKey = base64.b64encode(key)
        self.headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}

    def get(self, identifier):
        """Return the asset by the given id"""
        return self._get_by_id(identifier)

    def _get_by_id(self, identifier):
        # primary url base seems out of whack
        url = self.base_url + '/' + str(identifier)
        response = requests.get(url, headers=self.headers)
        return response.json()

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


class EloquaClient(EloquaBaseClient):
    headers = ''
    base_url = settings.BASE_URL

    @property
    def emails(self):
        return EloquaEmailClient()

    @property
    def contacts(self):
        return EloquaContactsClient()


class EloquaEmailClient(EloquaBaseClient):
    # only get/search need the slash
    base_url = settings.BASE_URL + '/assets/email'

    def create(self, name, subject, body, body_plaintext=None, is_tracked=False, folder_id=None, sender_name=None, sender_email=None, reply_to_email=None, reply_to_name=None):
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

        if sender_email and sender_email:
            payload['senderEmail'] = sender_email
            payload['senderName'] = sender_name

        if reply_to_email and reply_to_name:
            payload['replyToEmail'] = reply_to_email
            payload['replyToName'] = reply_to_name            

        # make the call
        # TODO: logging?
        r = requests.post(self.base_url, data=json.dumps(payload), headers=self.headers)
        if r.response_code == 200:
            return r.json()
        else:
            raise Exception('error!')  # TODO: be more verbose


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
        return r.json()

