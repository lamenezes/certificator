import os.path

from prettyconf import config

PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_PATH = os.path.join(PATH, 'templates')
MEETUP_API_KEY = config('MEETUP_API_KEY', default='')
