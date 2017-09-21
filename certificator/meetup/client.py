import requests


class MeetupClient:
    def __init__(self, api_key):
        self.params = {'key': api_key}

    def get_attendances(self, urlname, event_id):
        url = 'https://api.meetup.com/{}/events/{}/attendance'.format(urlname, event_id)
        response = requests.get(url, params=self.params)
        return response.json()

    def get_event(self, urlname, event_id):
        url = 'https://api.meetup.com/{}/events/{}'.format(urlname, event_id)
        response = requests.get(url, self.params)
        return response.json()

    def get_member(self, urlname, member_id):
        url = 'https://api.meetup.com/{}/members/{}'.format(urlname, member_id)
        response = requests.get(url, self.params)
        return response.json()
