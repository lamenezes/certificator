import requests

from certificator import config

params = {'key': config.MEETUP_API_KEY}


def get_attendances(urlname, event_id):
    url = 'https://api.meetup.com/{}/events/{}/attendance'.format(urlname, event_id)
    response = requests.get(url, params=params)
    return response.json()


def get_event(urlname, event_id):
    url = 'https://api.meetup.com/{}/events/{}'.format(urlname, event_id)
    response = requests.get(url, params)
    return response.json()


def get_member(urlname, member_id):
    url = 'https://api.meetup.com/{}/members/{}'.format(urlname, member_id)
    response = requests.get(url, params)
    return response.json()
