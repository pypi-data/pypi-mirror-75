import logging
from typing import Union

import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from tensorflow import keras
from tensorflow.keras import Model

from . import training, noise_generator
from .preprocessing import InputPreprocessor, OutputPreprocessor
from ..data_generation.data_generator import ReflectivityGenerator
from ..data_generation.layers import MultilayerStructure

logging.basicConfig(level=logging.INFO)


class SimTester:
    def __init__(self):
        pass


def test_on_simulation(model: Union[str, Model], experiment_name: str, q: ndarray, sample: MultilayerStructure,
                       n_test: int, noise_type: str, input_preprocessor: InputPreprocessor,
                       output_preprocessor: OutputPreprocessor, noise_levels=None, background_levels=None,
                       noise_range=None, background_range=None, relative_background_spread=0.1):
    if type(model) is Model:
        pass
    elif type(model) is str:
        model = keras.models.load_model(model)
    else:
        raise ValueError('model must be keras model object or path to model')

    generator = ReflectivityGenerator(q, sample)

    test_refl, test_refl_pp, test_labels, test_labels_pp, removed_labels, noise_levels_array, bg_levels_array = make_testing_data(
        experiment_name, noise_type, q, sample, n_test, input_preprocessor, output_preprocessor,
        noise_levels, background_levels, noise_range, background_range, relative_background_spread)

    predicted_labels = model.predict(test_refl_pp)
    restored_predicted_labels = output_preprocessor.restore_labels(predicted_labels, removed_labels)
    predicted_reflectivity = generator.simulate_reflectivity(restored_predicted_labels)

    noise_df = pd.DataFrame()
    noise_df['noise_level'] = noise_levels_array
    noise_df['bg_level'] = bg_levels_array

    mae_df = make_mae_df_by_noise(test_labels, restored_predicted_labels, noise_levels, noise_levels_array,
                                  background_levels,
                                  bg_levels_array)

    return test_refl, test_labels, predicted_reflectivity, restored_predicted_labels, noise_df, mae_df


def make_testing_data(experiment_name: str, noise_type: str, q: ndarray, sample: MultilayerStructure, n_test: int,
                      input_preprocessor: InputPreprocessor, output_preprocessor: OutputPreprocessor, noise_levels=None,
                      background_levels=None, noise_range=None, background_range=None, relative_background_spread=0.1):
    logging.info('Generating training data ...')
    generator = ReflectivityGenerator(q, sample)

    n_layers = len(sample)

    if noise_type is 'continuous':
        test_labels = generator.generate_random_labels(n_test)
        test_refl, noise_levels, bg_levels = noise_generator.add_random_levels(
            f'testing_data/{experiment_name}.h5', test_labels, generator, n_layers, noise_range, background_range,
            relative_background_spread)
    elif noise_type is 'discrete':
        n_unique_labels = training.get_number_of_unique_labels(n_test, noise_levels, background_levels)

        test_labels = generator.generate_random_labels(n_unique_labels)
        test_refl, test_labels, noise_levels, bg_levels = noise_generator.add_discrete_levels(test_labels,
                                                                                              generator,
                                                                                              n_layers,
                                                                                              noise_levels,
                                                                                              background_levels,
                                                                                              relative_background_spread,
                                                                                              f'testing_data/{experiment_name}.h5')
    else:
        raise ValueError('Not a valid noise type (must be continuous or discrete)')

    test_refl_pp = input_preprocessor.standardize(test_refl)

    test_labels_pp, removed_labels = output_preprocessor.apply_preprocessing(test_labels)

    return test_refl, test_refl_pp, test_labels, test_labels_pp, removed_labels, noise_levels, bg_levels


def make_mae_df_by_noise(test_labels: DataFrame, pred_labels: DataFrame, noise_levels: tuple, noise_level_array:
ndarray, bg_levels: tuple, bg_level_array: ndarray):
    labels_ae = abs(pred_labels - test_labels)

    mean_absolute_error = np.empty((len(noise_levels) * len(bg_levels), labels_ae.shape[1] + 2))

    row = 0
    for noise in noise_levels:
        for bg in bg_levels:
            indexes = (noise_level_array == noise) & (bg_level_array == bg)
            mae = np.mean(labels_ae[indexes])
            mean_absolute_error[row, :labels_ae.shape[1]] = mae
            mean_absolute_error[row, labels_ae.shape[1]:labels_ae.shape[1] + 2] = np.array([noise, bg])
            row += 1

    headers = list(labels_ae.columns) + ['noise_level', 'bg_level']
    return pd.DataFrame(data=mean_absolute_error, columns=headers)
