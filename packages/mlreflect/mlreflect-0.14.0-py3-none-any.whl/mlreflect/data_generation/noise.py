import functools
from typing import Union, Tuple

import numpy as np
from numpy import ndarray
from refl1d.reflectivity import convolve as refl1d_convolve


def iterate_over_curves(func):
    @functools.wraps(func)
    def wrapper(reflectivity_curves, *args, **kwargs):
        number_of_dimensions = len(reflectivity_curves.shape)
        if number_of_dimensions not in (1, 2):
            raise ValueError('number of dimensions mus be 1 or 2')
        if number_of_dimensions == 1:
            return func(reflectivity_curves, *args, **kwargs)
        else:
            return np.array([func(reflectivity_curve, *args, **kwargs) for reflectivity_curve in reflectivity_curves])

    return wrapper


def apply_shot_noise(reflectivity_curves: ndarray, shot_noise_spread: Union[float, Tuple[float, float]]) -> Tuple[
    ndarray, ndarray]:
    """Returns reflectivity curves with applied shot noise based on `shot_noise_spread`.

        Args:
            reflectivity_curves: Array of normalized reflectivity curves
            shot_noise_spread: Scaling factor c for the standard deviation sqrt(I*c) of the shot noise around
                the intensity of simulated reflectivity curves. Since the intensity is normalized, this is
                equivalent to setting the direct beam intensity I_0 = 1/c. If a tuple with two values is given,
                a random value between the two is chosen for each curve.

        Returns:
            noisy_reflectivity, spreads
    """
    dimensions = len(reflectivity_curves.shape)
    if dimensions == 1:
        num_curves = 1
    elif dimensions == 2:
        num_curves = len(reflectivity_curves)
    else:
        raise ValueError('number of dimensions mus be 1 or 2')

    if type(shot_noise_spread) in (float, int):
        spreads = np.repeat(shot_noise_spread, num_curves)
    elif type(shot_noise_spread) is tuple:
        spreads = np.random.uniform(shot_noise_spread[0], shot_noise_spread[1], num_curves)
    else:
        raise TypeError(f'shot_noise_spread must be float or tuple and is {type(shot_noise_spread)}')

    if num_curves == 1:
        noisy_reflectivity = np.clip(np.random.normal(reflectivity_curves, np.sqrt(reflectivity_curves * spreads[0])),
                                     1e-8, None)
    else:
        noisy_reflectivity = np.array(
            [np.clip(np.random.normal(curve, np.sqrt(curve * spread)), 1e-8, None) for curve, spread in
             zip(reflectivity_curves, spreads)])
    return noisy_reflectivity, spreads


def generate_background(number_of_curves: int, number_of_q_values: int,
                        background_base_level: Union[float, Tuple[float, float]],
                        relative_background_spread: float) -> Tuple[ndarray, ndarray]:
    """Returns a background with a normal distribution that can be added to a reflectivity curve.

        Args:
            number_of_curves: Number of curves for which a background is generated
            number_of_q_values: Length of the generated array (should be same length as reflectivity curve)
            background_base_level: Range from which the mean of the normal distribution is chosen
            relative_background_spread: Relative standard deviation of the normal distribution (e.g. a value of 0.1
                means the standard deviation is 10% of the mean)

        Returns:
            background with dimensions (number_of_curves, number_of_q_values), means
    """

    if type(background_base_level) in (float, int):
        return np.random.normal(background_base_level, relative_background_spread * background_base_level,
                                (number_of_curves, number_of_q_values)), np.repeat(background_base_level,
                                                                                   number_of_curves)
    elif type(background_base_level) is tuple:
        mean = np.random.uniform(background_base_level[0], background_base_level[1], number_of_curves)
        means = np.tile(mean, (number_of_q_values, 1)).T
        stdevs = relative_background_spread * means
        return np.random.normal(means, stdevs, (number_of_curves, number_of_q_values)), mean
    else:
        raise TypeError(f'background_base_level must be float, int or tuple and is {type(background_base_level)}')


@iterate_over_curves
def apply_gaussian_convolution(reflectivity_curves: ndarray, q_before: ndarray, q_after: ndarray,
                               width: ndarray) -> ndarray:
    """Returns convolved reflectivity curves at q-values given in `q_before`.

    Args:
        reflectivity_curves: Array of normalized reflectivity curves
        q_before: q-values that correspond to the given reflectivity curve
        q_after: q-values for which the convolved curve is evaluated (shorter than `q_before`)
        width: width of the gaussian convolution at each q-value

    Returns:
        convolved reflectivity curves
    """
    if width.all() == 0:
        return reflectivity_curves
    else:
        return refl1d_convolve(q_before, reflectivity_curves, q_after, width)
