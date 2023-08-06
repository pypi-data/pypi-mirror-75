import pytest


@pytest.fixture
def toy_data_frame():
    from monopolion_evaluator.protobuf import parser
    game_outcomes = parser.parse_delimited_file('tests/fixtures/toy_data_2player.gz')
    return parser.to_data_frame(game_outcomes)


@pytest.fixture
def classifier(toy_data_frame):
    from monopolion_evaluator.classifier import Classifier
    return Classifier(toy_data_frame, toy_data_frame, 2)


@pytest.fixture
def classifier_no_validation(toy_data_frame):
    from monopolion_evaluator.classifier import Classifier
    return Classifier(toy_data_frame, validation_df=None, player_count=2)


def test_df_to_dataset(classifier, toy_data_frame):
    ds = classifier.df_to_dataset(toy_data_frame)
    features, labels = ds.element_spec


def test_df_to_dataset_no_shuffle(classifier, toy_data_frame):
    ds = classifier.df_to_dataset(toy_data_frame, shuffle=False)
    features, labels = ds.element_spec


def test_fit_model(classifier, toy_data_frame):
    classifier.fit_model(epochs=1)


def test_fit_model_layers(classifier, toy_data_frame):
    classifier.fit_model(epochs=1, layers=[8, 2])


def test_fit_model_no_validation(classifier_no_validation, toy_data_frame):
    classifier_no_validation.fit_model(epochs=1)
