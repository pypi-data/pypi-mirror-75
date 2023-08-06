import logging
from typing import Union

import numpy as np
from numpy import ndarray
from pandas import DataFrame
from tensorflow import keras

from . import noise_generator
from .preprocessing import InputPreprocessor, OutputPreprocessor
from ..data_generation.data_generator import ReflectivityGenerator
from ..data_generation.layers import MultilayerStructure
from ..utils.naming import make_timestamp

logging.basicConfig(level=logging.INFO)


def train(experiment_name: str, epochs: int, q: ndarray, sample: MultilayerStructure, n_train: int, n_val: int,
          noise_type: str, noise_levels=None, background_levels=None, noise_range=None, background_range=None,
          relative_background_spread=0.1):
    time_stamp = make_timestamp()
    experiment_id = experiment_name + '_' + time_stamp

    lr_reduction = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, verbose=1)

    checkpoint = keras.callbacks.ModelCheckpoint(filepath='models/' + experiment_id + '_model.h5', monitor='val_loss',
                                                 verbose=1, save_best_only=True)

    tb_callback = keras.callbacks.TensorBoard(log_dir='tensorboard/' + experiment_id, histogram_freq=0,
                                              write_graph=True, write_images=False)

    refl_train, refl_val, labels_train, labels_val, input_preprocessor, output_preprocessor = make_training_data(
        experiment_name, noise_type, q,
        sample, n_train, n_val, noise_levels,
        background_levels, noise_range,
        background_range,
        relative_background_spread)

    model = make_model(refl_train.shape[1], labels_train.shape[1])

    out = model.fit(refl_train, np.array(labels_train), batch_size=512, epochs=epochs, verbose=0,
                    validation_data=(refl_val, np.array(labels_val)),
                    callbacks=[tb_callback, lr_reduction, checkpoint]
                    )

    save_loss(experiment_id, out)

    return out, input_preprocessor, output_preprocessor


def save_loss(experiment_id: str, out):
    path = 'loss/' + experiment_id
    np.savetxt(path + '_loss.dat', out.history['loss'])
    np.savetxt(path + '_val_loss.dat', out.history['val_loss'])


def make_training_data(experiment_name: str, noise_type: str, q: ndarray, sample: MultilayerStructure, n_train: int,
                       n_val: int, noise_levels=None, background_levels=None, noise_range=None, background_range=None,
                       relative_background_spread=0.1):
    logging.info('Generating training data ...')
    generator = ReflectivityGenerator(q, sample)

    n_total = n_train + n_val
    n_layers = len(sample)

    if noise_type is 'continuous':
        labels = generator.generate_random_labels(n_total)
        refl, noise_levels, bg_levels = noise_generator.add_random_levels(
            f'training_data/{experiment_name}.h5', labels, generator, n_layers, noise_range, background_range,
            relative_background_spread)
    elif noise_type is 'discrete':
        n_unique_labels = get_number_of_unique_labels(n_total, noise_levels, background_levels)

        labels = generator.generate_random_labels(n_unique_labels)
        refl, labels, noise_levels, bg_levels = noise_generator.add_discrete_levels(labels, generator,
                                                                                    n_layers, noise_levels,
                                                                                    background_levels,
                                                                                    relative_background_spread,
                                                                                    f'training_data/{experiment_name}.h5')
        refl, labels = shuffle(refl, labels)
    else:
        raise ValueError('Not a valid noise type (must be continuous or discrete)')

    refl_train, refl_val, input_preprocessor = get_preprocessed_input(refl, n_val)

    labels_train, labels_val, output_preprocessor = get_preprocessed_output(labels, n_val, sample)

    return refl_train, refl_val, labels_train, labels_val, input_preprocessor, output_preprocessor


def shuffle(reflectivity: ndarray, labels: DataFrame):
    logging.info('Shuffling data ...')
    random_idx = np.arange(len(reflectivity))
    np.random.shuffle(random_idx)
    reflectivity = reflectivity[random_idx]
    labels = labels.reindex(index=random_idx).reset_index(drop=True)

    return reflectivity, labels


def get_number_of_unique_labels(n_total: int, noise_levels: Union[int, float, tuple],
                                background_levels: Union[int, float, tuple]):
    if type(noise_levels) in (int, float):
        num_noise_levels = 1
    else:
        num_noise_levels = len(noise_levels)
    if type(background_levels) in (int, float):
        num_background_levels = 1
    else:
        num_background_levels = len(noise_levels)

    number_of_combinations = num_noise_levels * num_background_levels
    n_unique_labels = int(n_total / number_of_combinations)
    if n_total % number_of_combinations is not 0:
        logging.info(f'{n_total} not divisible by {number_of_combinations}. Generating {n_unique_labels} unique '
                     f'labels')

    return n_unique_labels


def make_model(n_input: int, n_output: int):
    logging.info('Making model ...')
    model = keras.models.Sequential()

    model.add(keras.layers.Dense(1000, input_dim=n_input))
    model.add(keras.layers.Activation('relu'))

    for i in range(8):
        model.add(keras.layers.Dense(1000))
        model.add(keras.layers.Activation('relu'))

    model.add(keras.layers.Dense(n_output))

    adam_optimizer = keras.optimizers.Adam(lr=1e-3, beta_1=0.9, beta_2=0.999, epsilon=1e-8, decay=0, amsgrad=False)

    model.compile(loss='mean_squared_error', optimizer=adam_optimizer)

    return model


def get_preprocessed_input(reflectivity: ndarray, n_val: int):
    input_preprocessor = InputPreprocessor()

    reflectivity_preprocessed = input_preprocessor.standardize(reflectivity)
    reflectivity_train = reflectivity_preprocessed[:n_val, :]
    reflectivity_val = reflectivity_preprocessed[n_val:, :]

    return reflectivity_train, reflectivity_val, input_preprocessor


def get_preprocessed_output(labels: DataFrame, n_val: int, sample: MultilayerStructure):
    output_preprocessor = OutputPreprocessor(sample, normalization='absolute_max')

    labels_preprocessed, labels_removed = output_preprocessor.apply_preprocessing(labels)
    labels_train = labels_preprocessed[:n_val]
    labels_val = labels_preprocessed[n_val:]

    return labels_train, labels_val, output_preprocessor
