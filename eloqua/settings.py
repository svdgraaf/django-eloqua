import logging
logger = logging.getLogger(__name__)

try:
    from django.conf import settings
except ImportError:
    # We do not need Django perse
    settings = {}

# Required settings
SITE = getattr(settings, 'ELOQUA_SITE', None)
USERNAME = getattr(settings, 'ELOQUA_USERNAME', None)
PASSWORD = getattr(settings, 'ELOQUA_PASSWORD', None)

BASE_URL = getattr(settings, 'ELOQUA_BASE_URL', 'https://secure.eloqua.com/API/REST/1.0')

# how long is old data valid, and should it be locally cached (default: 24 hours)
PROFILE_TIMEOUT = getattr(settings, 'ELOQUA_PROFILE_TIMEOUT', 60 * 60 * 24)
