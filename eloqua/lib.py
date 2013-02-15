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

class EloquaClient(object):
    headers = ''
    base_url = settings.BASE_URL

    @property
    def emails(self):
        return EloquaEmailClient()


class EloquaEmailClient(EloquaBaseClient):
    # only get/search need the slash
    base_url = settings.BASE_URL + '/assets/email'

    def get(self, identifier):
        return self._get_by_id(identifier)

    def create(self, name, subject, body, body_plaintext=None, is_tracked=False, folder_id=None, sender_name=None, sender_email=None, reply_to_email=None, reply_to_name=None):

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

    def delete(self, identifier):
        return self._delete_by_id(identifier)

