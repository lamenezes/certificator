import csv
import json
import os.path

from jinja2 import Environment, PackageLoader, select_autoescape
from weasyprint import HTML

from . import config


class BaseCertificator:
    def __init__(self, destination_path='.', template_path=None,
                 filename_format='certificate-{id:0>3}.pdf'):
        self.template_path = template_path
        self.destination_path = destination_path
        self.filename_format = filename_format

    def get_meta(self):
        raise NotImplementedError

    def get_certificate_data(self):
        raise NotImplementedError

    def get_template_path(self):
        if self.template_path:
            return self.template_path

        return 'default.html'

    @property
    def template(self):
        # TODO: get templates from '.', from ./templates and then certifier/templates
        env = Environment(
            loader=PackageLoader('certificator', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        return env.get_template(self.get_template_path())

    def get_context(self, **kwargs):
        context = {}
        meta = self.get_meta()

        context.update(meta)
        context.update(kwargs)

        return context

    def render(self, context):
        raw_html = self.template.render(**context)
        return HTML(string=raw_html, base_url=config.TEMPLATES_PATH)

    def get_filepath(self, **kwargs):
        filename = self.filename_format.format(**kwargs)
        return os.path.join(self.destination_path, filename)

    def generate_one(self, context):
        html = self.render(context)
        filepath = self.get_filepath(**context)
        html.write_pdf(filepath)

    def generate(self):
        data = self.get_certificate_data()
        for i, row in enumerate(data):
            context = self.get_context(id=i, **row)
            self.generate_one(context)


class CSVCertificator(BaseCertificator):
    def __init__(self, delimiter=',', meta_path='./meta.json', data_path='./data.csv', **kwargs):
        super().__init__(**kwargs)
        self.delimiter = delimiter
        self.meta_path = meta_path
        self.data_path = data_path

    def get_meta(self):
        with open(self.meta_path) as f:
            return json.loads(f.read())

    def get_certificate_data(self):
        with open(self.data_path) as f:
            return [row for row in csv.DictReader(f)]
