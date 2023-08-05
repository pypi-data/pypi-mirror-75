# The model code in  this file is derived from the TensorFlow feature_columns example:
# @see https://github.com/tensorflow/docs/blob/master/site/en/tutorials/structured_data/feature_columns.ipynb
#
# Copyright 2019 The TensorFlow Authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers


class Classifier:
    NUMERIC_COLUMN_SUFFIXES = ['cash']
    TARGET_COLUMN = 'winningPlayer'

    def __init__(self, train_df: pd.DataFrame, validation_df: pd.DataFrame, player_count: int):
        self.train_df = train_df
        self.validation_df = validation_df
        self.headers = train_df.columns.values
        self.player_count = player_count
        self.__category_vocabulary_lists = {
            'die1': range(1, 7),
            'die2': range(1, 7),
            'position': range(40),
            'isInJail': range(2),
            'remainingTurnsInJail': range(4),
            'isOwned': range(2),
            'owner': range(-1, player_count),
            'buildingCount': range(5),
        }

    def fit_model(self, epochs: int = 10):
        train_ds = self.df_to_dataset(self.train_df)
        validation_ds = None
        if self.validation_df is not None:
            validation_ds = self.df_to_dataset(self.validation_df)

        feature_layer = tf.keras.layers.DenseFeatures(self.get_feature_columns())

        model = tf.keras.Sequential([
            feature_layer,
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dropout(.1),
            layers.Dense(1)
        ])

        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy'])

        model.fit(
            train_ds,
            validation_data=validation_ds,
            epochs=epochs)

        return model

    def get_feature_columns(self):
        cols = []
        for header in self.headers:
            if header == self.TARGET_COLUMN:
                continue
            elif any(header.endswith(s) for s in self.NUMERIC_COLUMN_SUFFIXES):
                cols.append(feature_column.numeric_column(header))
            else:
                vocab = self.__get_category_vocabulary_list(header)
                categorical_column = feature_column.categorical_column_with_vocabulary_list(header, vocab)
                cols.append(feature_column.indicator_column(categorical_column))

        return cols

    def df_to_dataset(self, data_frame: pd.DataFrame, shuffle: bool = True, batch_size: int = 32) -> tf.data.Dataset:
        """
        A utility method to create a tf.data dataset from a Pandas Dataframe
        :param data_frame:
        :param shuffle:
        :param batch_size:
        :return:
        """
        df = data_frame.copy()
        labels = df.pop(self.TARGET_COLUMN)
        ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(df))
        ds = ds.batch(batch_size)
        return ds

    def __get_category_vocabulary_list(self, header):
        try:
            suffix = header.split('_')[-1]
            return self.__category_vocabulary_lists[suffix]
        except KeyError:
            return self.train_df[header].unique()
