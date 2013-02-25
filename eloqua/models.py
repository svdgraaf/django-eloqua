from django.db import models
from eloqua.exceptions import ContactFieldNotFound
from eloqua import settings
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
        # only fetch the profile data once, is this enough?
        # perhaps depend on memcache, and store it there
        if self._profile == None:
            from eloqua.clients import EloquaClient
            e = EloquaClient()

            # fetch by eloqua id if present, otherwise,
            # search by email via the active user
            if self.contact_id == None:
                results = e.contacts.search(self.user.email)
                if len(results) > 0:
                    self._profile = results['elements'][0]
            else:
                results = e.contacts.get(self.contact_id)
                self._profile = results

            fields = {}
            for field in self._profile['fieldValues']:
                if 'value' in field:
                    fields[int(field['id'])] = field['value']
            self._contact_fields = fields

        # check if eloqua id is present, if not, store it
        if self.contact_id == None:
            self.contact_id = self._profile['id']
            self.save()

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
