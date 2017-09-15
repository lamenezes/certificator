from datetime import datetime as dt

from . import client as meetup_client
from ..certificator import BaseCertificator
from .models import Event


class MeetupCertificator(BaseCertificator):
    def __init__(self, urlname, event_id, **kwargs):
        self.urlname = urlname
        self.event_id = event_id
        super().__init__(**kwargs)

    def get_certificate_data(self):
        attendances = meetup_client.get_attendances(self.urlname, self.event_id)
        return ({'name': attendance['member']['name']} for attendance in attendances)

    def get_meta(self):
        event_data = meetup_client.get_event(self.urlname, self.event_id)
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
