"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mmonopolion_evaluator` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``monopolion_evaluator.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``monopolion_evaluator.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

from monopolion_evaluator.classifier import Classifier
from monopolion_evaluator.protobuf.parser import parse_delimited_file
from monopolion_evaluator.protobuf.parser import to_data_frame

parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument('--training', metavar='TRAINING_DATA', type=str, required=True,
                    help="Path to training data file, encoded using ProtoBuf")
parser.add_argument('--validation', metavar='VALIDATION_DATA', type=str,
                    help="Path to validation data file, encoded using ProtoBuf")
parser.add_argument('--epochs', metavar='EPOCHS', type=int, default=10,
                    help="Number of epochs to train the model")


def main(args=None):
    args = parser.parse_args(args=args)

    training_df = to_data_frame(parse_delimited_file(args.training))
    validation_df = None
    if args.validation is not None:
        validation_df = to_data_frame(parse_delimited_file(args.validation))
    classifier = Classifier(training_df, validation_df=validation_df, player_count=2)
    classifier.fit_model(epochs=args.epochs)
