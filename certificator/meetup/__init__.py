from datetime import datetime as dt

from ..base import Certificate
from .client import get_attendances, get_event
from .models import Event


class MeetupCertificate(Certificate):
    def __init__(self, urlname, event_id, **kwargs):
        self.urlname = urlname
        self.event_id = event_id
        super().__init__(**kwargs)

    def get_rows(self):
        attendances = get_attendances(self.urlname, self.event_id)
        return ({'name': attendance['member']['name']} for attendance in attendances)

    def get_meta(self):
        event_data = get_event(self.urlname, self.event_id)
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
