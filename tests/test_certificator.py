import os
from unittest import mock

import pytest
from faker import Faker
from json_encoder import json

from certificator.certificator import BaseCertificator, CSVCertificator

faker = Faker()
PATH = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def certificator():
    return BaseCertificator()


@pytest.fixture()
def fake_context():
    return {
        'city': faker.city(),
        'date': faker.date(pattern='%d/%m/%Y'),
        'full_date': faker.date(pattern='%d %B %Y'),
        'organizer': faker.company(),
        'title': faker.sentence(),
        'workload': faker.random_int(min=4, max=300),
    }


@pytest.fixture()
def certificate_data():
    return [{'name': faker.name()} for _ in range(5)]


@pytest.fixture
def mock_certificator(fake_context, certificate_data):
    class MockCertificator(BaseCertificator):
        def get_meta(self):
            return fake_context

        def get_certificate_data(self):
            return certificate_data

        @property
        def template(self):
            return mock.Mock()

        render = mock.Mock()

    return MockCertificator()


@pytest.fixture
def csv_certificator():
    return CSVCertificator()


@pytest.fixture
def csv_certificate_data(certificate_data):
    return '\n'.join(d['name'] for d in certificate_data)


def test_base_certificator_certificator(certificator):
    assert certificator.template_path is None
    assert certificator.destination_path
    with pytest.raises(NotImplementedError):
        certificator.get_meta()
    with pytest.raises(NotImplementedError):
        certificator.get_certificate_data()


def test_base_certificator_get_template_path(certificator):
    path = 'foo/bar'
    certificator.template_path = path

    assert certificator.get_template_path() == path


def test_base_certificator_certificator_get_context(mock_certificator, fake_context):
    context = mock_certificator.get_context(foo='bar')

    assert context['foo'] == 'bar'
    assert not fake_context.keys() - context.keys()


@mock.patch('certificator.certificator.PackageLoader')
@mock.patch('certificator.certificator.Environment')
def test_base_certificator_certificator_template(mock_env, mock_loader, certificator):
    assert certificator.template
    assert mock_loader.called
    assert mock_env.called
    assert mock_env.return_value.get_template.called


@mock.patch('certificator.certificator.HTML')
def test_base_certificator_render(mock_html, certificator, fake_context):
    with mock.patch('certificator.certificator.PackageLoader'), \
            mock.patch('certificator.certificator.Environment'):
        assert certificator.render(fake_context)
        assert mock_html.called_once_with(**fake_context)


def test_base_certificator_get_filepath(mock_certificator):
    filepath = mock_certificator.get_filepath(id=10)
    assert '10' in filepath
    assert mock_certificator.destination_path in filepath


def test_base_certificator_generate_one(mock_certificator, fake_context):
    fake_context['id'] = 1
    assert mock_certificator.generate_one(fake_context) is None

    assert mock_certificator.render.return_value.write_pdf.called


def test_base_certificator_generate(mock_certificator, certificate_data):
    mock_certificator.generate_one = mock.Mock()

    mock_certificator.generate()

    assert mock_certificator.generate_one.called
    assert mock_certificator.generate_one.call_count == len(certificate_data)


def test_csv_certificator(csv_certificator, fake_context):
    assert isinstance(csv_certificator, (BaseCertificator, CSVCertificator))
    assert csv_certificator.delimiter
    assert csv_certificator.meta_path
    assert csv_certificator.data_path


def test_csv_certificator_get_meta(csv_certificator, fake_context):
    with mock.patch('builtins.open', mock.mock_open(read_data=json.dumps(fake_context))):
        meta = csv_certificator.get_meta()

    assert meta == fake_context
