from datetime import datetime as dt

from . import client as MeetupClient
from ..certificator import BaseCertificator
from .models import Event


class MeetupCertificator(BaseCertificator):
    def __init__(self, urlname, event_id, api_key, **kwargs):
        super().__init__(**kwargs)
        self.urlname = urlname
        self.event_id = event_id
        self.client = MeetupClient(api_key=api_key)

    def get_certificate_data(self):
        attendances = self.client.get_attendances(self.urlname, self.event_id)
        return ({'name': attendance['member']['name']} for attendance in attendances)

    def get_meta(self):
        event_data = self.client.get_event(self.urlname, self.event_id)
        event = Event(**event_data)
        event.clean()
        return {
            'city': event.venue['city'],
            'date': dt.strftime(event.date, '%d/%m/%Y'),
            'full_date': event.full_date,
            'organizer': event.group['name'],
            'place': event.venue['name'],
            'title': event.name,
            'workload': event.duration,
        }
