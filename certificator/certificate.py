import os.path

from jinja2 import Environment, PackageLoader, select_autoescape
from weasyprint import HTML

PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_PATH = os.path.join(PATH, 'data')


class Certificate:
    def __init__(self, destination_path='.', template_path=None, **kwargs):
        self.template_path = template_path
        self.destination_path = destination_path

    def get_meta(self):
        raise NotImplementedError

    def get_rows(self):
        raise NotImplementedError

    def get_template_path(self):
        if self.template_path:
            return self.template_path

        return 'default.html'

    @property
    def template(self):
        # TODO: get templates from '.', from ./templates and then certifier/templates
        env = Environment(
            loader=PackageLoader('certifier', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        return env.get_template(self.get_template_path())

    def render(self, context):
        raw_html = self.template.render(**context)
        return HTML(string=raw_html, base_url=TEMPLATES_PATH)

    def get_context(self, **kwargs):
        context = {}
        meta = self.get_meta()

        context.update(meta)
        context.update(kwargs)

        return context

    def generate(self):
        for i, row in enumerate(self.get_rows()):
            context = self.get_context(**row)
            html = self.render(context)
            filename = 'Certificate - {}.pdf'.format(context.get('name', i))
            file_path = os.path.join(self.destination_path, filename)
            html.write_pdf(file_path)
