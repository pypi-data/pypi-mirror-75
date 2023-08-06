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

import pandas as pd

from monopolion_evaluator import __version__ as monopolion_evaluator_version
from monopolion_evaluator.protobuf.parser import parse_delimited_file
from monopolion_evaluator.protobuf.parser import to_data_frame
from monopolion_evaluator.util import create_model_directory

LOGO = r"""                                      _ _
  /\/\   ___  _ __   ___  _ __   ___ | (_) ___  _ __
 /    \ / _ \| '_ \ / _ \| '_ \ / _ \| | |/ _ \| '_ \
/ /\/\ \ (_) | | | | (_) | |_) | (_) | | | (_) | | | |
\/    \/\___/|_| |_|\___/| .__/ \___/|_|_|\___/|_| |_|
                         |_|          Evaluator v""" + monopolion_evaluator_version


def print_logo(args=None):
    print(LOGO, "\n")


def train(args=None):
    model_path = create_model_directory(args.output) if args.output is not None else None

    training_df = to_data_frame(parse_delimited_file(args.training))
    validation_df = None
    if args.validation is not None:
        validation_df = to_data_frame(parse_delimited_file(args.validation))

    from monopolion_evaluator.classifier import Classifier

    classifier = Classifier(training_df, validation_df=validation_df, player_count=2)
    model = classifier.fit_model(
        epochs=args.epochs, layers=args.layers, learning_rate=args.learning_rate, dropout=args.dropout,
        batch_size=args.batch_size)
    if model_path is not None:
        model.save(model_path)


def predict(args=None):
    import tensorflow as tf

    df = pd.read_csv(args.csv)
    ds = tf.data.Dataset.from_tensor_slices(dict(df)).batch(32)

    model = tf.keras.models.load_model(args.model)
    predictions = model.predict(ds)
    print(predictions)


parser = argparse.ArgumentParser(description=str(LOGO), formatter_class=argparse.RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(help='Choose whether to train or load a model')

# version sub-command
version_parser = subparsers.add_parser('version')
version_parser.set_defaults(sub_command=print_logo)

# train sub-command
train_parser = subparsers.add_parser('train')
train_parser.set_defaults(sub_command=train)
train_parser.add_argument('--training', metavar='TRAINING_DATA', type=str, required=True,
                          help="Path to training data file, encoded using ProtoBuf")
train_parser.add_argument('--validation', metavar='VALIDATION_DATA', type=str,
                          help="Path to validation data file, encoded using ProtoBuf")
train_parser.add_argument('--output', metavar='MODEL_DIR', type=str,
                          help="File or directory path to save the TensorFlow model")
train_parser.add_argument('--layers', '-l', metavar='UNITS', type=int, nargs='*', default=[256, 128],
                          help="Neural net layers, where each integer corresponds to the number of units in a layer")
train_parser.add_argument('--epochs', metavar='EPOCHS', type=int, default=10,
                          help="Number of epochs to train the model")
train_parser.add_argument('--batch-size', '-b', metavar='BATCH_SIZE', type=int, default=100,
                          help="A typical batch size is between 10 and 1000")
train_parser.add_argument('--learning-rate', '-a', metavar='LEARNING_RATE', type=float, default=0.001,
                          help="Learning rate (alpha)")
train_parser.add_argument('--dropout', '-d', metavar='DROPOUT', type=float, default=0.2,
                          help="Dropout rate")

# load sub-command
load_parser = subparsers.add_parser('predict')
load_parser.set_defaults(sub_command=predict)
load_parser.add_argument('--model', '-m', metavar='MODEL_DIR', type=str,
                         help="Tensorflow model directory")
load_parser.add_argument('--csv', metavar='CSV', type=argparse.FileType('r'),
                         help="Tensorflow model directory")


def main(args=None):
    args = parser.parse_args(args=args)
    args.sub_command(args)
