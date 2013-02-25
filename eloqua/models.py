from django.db import models
from eloqua.exceptions import ContactFieldNotFound
from eloqua import settings
from datetime import datetime, timedelta
import json

try:
    from django.contrib.auth import get_user_model
    user_model = django.contrib.auth.get_user_model()
except:
    # backwards compatibility for < django 1.5
    from django.contrib.auth.models import User
    user_model = User


class Contact(models.Model):
    user = models.OneToOneField(user_model, related_name='eloqua_profile')
    contact_id = models.PositiveIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.TextField(null=True)

    _profile = None
    _contact_fields = {}

    def _fetch_profile(self):
        # check if we need to update the local data
        timeout = settings.PROFILE_TIMEOUT
        delta = timedelta(minutes=timeout)

        if self.data == None or (datetime.now() - delta) > self.updated_at:
            from eloqua.clients import EloquaClient
            e = EloquaClient()

            # fetch by eloqua id if present, otherwise,
            # search by email via the active user
            if self.contact_id == None:
                results = e.contacts.search(self.user.email)
                if len(results) > 0:
                    data = results['elements'][0]
            else:
                results = e.contacts.get(self.contact_id)
                data = results

            # json-ify the data
            self.data = json.dumps(data)
            if 'contact_id' in data:
                self.contact_id = data['content_id']
            self.save()

        # load the json data
        data = json.loads(self.data)
        self._profile = data

        # store all the contact fields seperately
        fields = {}
        for field in data['fieldValues']:
            if 'value' in field:
                fields[int(field['id'])] = field['value']
        self._contact_fields = fields

        return self._profile

    @property
    def first_name(self):
        profile = self._fetch_profile()
        return profile['firstName']

    @property
    def last_name(self):
        profile = self._fetch_profile()
        return profile['lastName']

    def value_for_field(self, pk):
        # make sure the profile is fetched
        self._fetch_profile()
        if pk in self._contact_fields:
            return self._contact_fields[pk]
        else:
            raise ContactFieldNotFound(pk)

# there must be a better way to do this, monkeypatching is ugly
user_model.eloqua_profile = property(lambda u: Contact.objects.get_or_create(user=u)[0])
