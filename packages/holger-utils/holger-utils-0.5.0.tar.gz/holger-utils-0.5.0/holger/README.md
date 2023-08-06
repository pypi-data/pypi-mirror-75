# Holger Utils


## Sentry
> settings.py
```python
from holger import sentry
...
SENTRY_KEY = '<your sentry key>'
SENTRY_ORGANIZATION = '<your sentry organization name>'
SENTRY_PROJECT = '<your sentry project name>'
SENTRY_ALLOWED_ALL = 'if true all status captured' # default False
SENTRY_ALLOWED_STATUS = 'list of status that should capture' # default []
sentry.init()
``` 

## Elastic search
> settings.py
```python
ELASTIC_PROTOCOL = '<http or https>' # default 'http'
ELASTIC_HOST = '<host that elastic run>' # default 'localhost'
ELASTIC_PORT = '<listen port>' # default 9200
ELASTIC_USE_SSL = '' # default False
TIME_ZONE = '<elastic timezone>' # default 'UTC' 
```

## Firebase
> settings.py
```python
FIREBASE_APP_OPTIONS = '<app dict options>' # default {}
FIREBASE_APP_NAME = 'your app name' # default 'FIRESTORE_DEFAULT'
```


## Log
> for use log, you must config elastic search and sentry before
