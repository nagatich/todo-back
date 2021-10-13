import os

import json

DEBUG = False

ALLOWED_HOSTS = json.loads(os.getenv('ALLOWED_HOSTS'))
