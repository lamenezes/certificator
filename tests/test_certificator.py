import csv
import io
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
    return [{'name': faker.name(), 'company': faker.company()} for _ in range(5)]


@pytest.fixture
def mock_certificator(fake_context, certificate_data):
    class MockCertificator(BaseCertificator):
        @property
        def meta(self):
            return fake_context

        @property
        def certificate_data(self):
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
def csv_certificate_file(certificate_data):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=['name', 'company'])
    writer.writeheader()
    for row in certificate_data:
        writer.writerow(row)
    stream.seek(0)
    return stream


@pytest.fixture
def semicolon_csv_certificate_file(certificate_data):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=['name', 'company'],
                            delimiter=';')
    writer.writeheader()
    for row in certificate_data:
        writer.writerow(row)
    stream.seek(0)
    return stream


def test_base_certificator_certificator(certificator):
    assert certificator.template_path is None
    assert certificator.destination_path
    with pytest.raises(NotImplementedError):
        certificator.meta
    with pytest.raises(NotImplementedError):
        certificator.certificate_data


def test_base_certificator_template_path_set_invalid(certificator):
    path = 'foo/bar'
    with pytest.raises(AssertionError):
        certificator.template_path = path


def test_base_certificator_template_path_set_valid(certificator):
    path = os.path.abspath(__file__)
    certificator.template_path = path

    assert certificator.template_path == path


def test_base_certificator_get_template_paths(certificator):
    assert len(certificator.get_template_paths()) == 3


def test_base_certificator_get_template_paths_custom_template_path(certificator):
    path = os.path.abspath(__file__)
    certificator.template_path = path

    paths = certificator.get_template_paths()
    assert len(paths) == 4
    assert path in paths


def test_base_certificator_certificator_get_context(mock_certificator, fake_context):
    context = mock_certificator.get_context(foo='bar')

    assert context['foo'] == 'bar'
    assert not fake_context.keys() - context.keys()


@mock.patch('certificator.certificator.FileSystemLoader')
@mock.patch('certificator.certificator.Environment')
def test_base_certificator_certificator_template(mock_env, mock_loader, certificator):
    assert certificator.template
    assert mock_loader.called
    assert mock_env.called
    assert mock_env.return_value.get_template.called


@mock.patch('certificator.certificator.HTML')
def test_base_certificator_render(mock_html, certificator, fake_context):
    with mock.patch('certificator.certificator.FileSystemLoader'), \
            mock.patch('certificator.certificator.Environment') as mock_env:
        mock_env.return_value.get_template.return_value.filename = __file__
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


def test_csv_certificator_meta(csv_certificator, fake_context):
    with mock.patch('builtins.open', mock.mock_open(read_data=json.dumps(fake_context))):
        meta = csv_certificator.meta

    assert meta == fake_context


def test_csv_certificator_certificate_data(csv_certificator, csv_certificate_file, certificate_data):
    with mock.patch('builtins.open', mock.Mock(return_value=csv_certificate_file)):
        data = csv_certificator.certificate_data

    assert data == certificate_data


def test_csv_certificator_certificate_data_with_custom_delimiter(csv_certificator, semicolon_csv_certificate_file, certificate_data):
    csv_certificator.delimiter = ';'
    with mock.patch('builtins.open', mock.Mock(return_value=semicolon_csv_certificate_file)):
        data = csv_certificator.certificate_data

    assert data == certificate_data
