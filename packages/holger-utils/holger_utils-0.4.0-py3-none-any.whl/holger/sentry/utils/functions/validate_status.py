from django.conf import settings

SENTRY_ALLOWED_ALL = getattr(settings, 'SENTRY_ALLOWED_ALL', False)
SENTRY_ALLOWED_STATUS = getattr(settings, 'SENTRY_ALLOWED_STATUS', [])


def validate_status(status_code):
    if SENTRY_ALLOWED_ALL:
        return True
    if status_code in SENTRY_ALLOWED_STATUS:
        return True
    return False
