import csv
import json

from .base import Certificate


class CSVCertificate(Certificate):
    def __init__(self, template_path=None):
        self.template_path = template_path

    def get_meta(self):
        with open('meta.json', 'r') as f:
            return json.loads(f.readall())

    def get_rows(self):
        with open('rows.csv', 'r') as f:
            return csv.DictReader(f, delimiter=',')
