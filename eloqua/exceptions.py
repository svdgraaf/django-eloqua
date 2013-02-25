class ContactNotFound(Exception):
    def __init__(self, msg="Contact with this email address could not be found"):
        msg = msg
        super(ContactNotFound, self).__init__(msg)


class ContactFieldNotFound(Exception):
    def __init__(self, key=None):
        msg = "A contact field for the given key (%s) could not be found" % key
        super(ContactFieldNotFound, self).__init__(msg)
