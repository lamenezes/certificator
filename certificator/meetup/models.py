from datetime import datetime as dt
from simple_model import Model


class Event(Model):
    fields = (
        'venue',
        'group',
        'duration',
        'time',
        'name',
    )

    MONTHS = (
        'janeiro',
        'fevereiro',
        'março',
        'abril',
        'maio',
        'junho',
        'julho',
        'agosto',
        'setembro',
        'outubro',
        'novembro',
        'dezembro',
    )

    def clean_duration(self, value):
        if not value:
            return 'não especificado'

        return value / (60 * 60 * 1000)

    def clean_time(self, value):
        return value / 1000

    @property
    def date(self):
        return dt.fromtimestamp(self.time)

    @property
    def full_date(self):
        full_date = dt.strftime(self.date, '%d de {} de %Y')
        full_month = self.MONTHS[self.date.month - 1].title()
        return full_date.format(full_month)
