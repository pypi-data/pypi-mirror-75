from django.conf import settings
from dateutil import tz

PROTOCOL = getattr(settings, 'ELASTIC_PROTOCOL', 'http')
HOST = getattr(settings, 'ELASTIC_HOST', 'localhost')
PORT = getattr(settings, 'ELASTIC_PORT', 9200)
USE_SSL = getattr(settings, 'ELASTIC_USE_SSL', False)
CURRENT_TIME_ZONE = tz.gettz(getattr(settings, 'TIME_ZONE', 'UTC'))
