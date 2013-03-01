class ObjectNotFound(Exception):
    def __init__(self, key=None):
        msg = "Object could not be found by the given key: %s" % (key)
        super(ObjectNotFound, self).__init__(msg)
