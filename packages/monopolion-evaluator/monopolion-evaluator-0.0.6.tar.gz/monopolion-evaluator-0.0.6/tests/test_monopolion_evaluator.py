import pytest

from monopolion_evaluator.classifier import Classifier
from monopolion_evaluator.cli import main


@pytest.fixture
def mock_classifier(monkeypatch):
    def mock_fit(*args, **kwargs):
        return None

    monkeypatch.setattr(Classifier, "fit_model", mock_fit)


def test_main(mock_classifier):
    main(['--training=tests/fixtures/toy_data_2player.gz', '--epochs=1'])


def test_main_validation(mock_classifier):
    main([
        '--training=tests/fixtures/toy_data_2player.gz',
        '--validation=tests/fixtures/toy_data_2player.gz',
        '--epochs=1'])


def test_main_layers(mock_classifier):
    main([
        '--training=tests/fixtures/toy_data_2player.gz',
        '-l', '1', '2', '4',
        '--epochs=1'])
