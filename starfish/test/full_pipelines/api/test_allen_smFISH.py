import numpy as np
import pytest

import starfish.data
from starfish.image._filter.bandpass import Bandpass
from starfish.image._filter.clip import Clip
from starfish.image._filter.gaussian_low_pass import GaussianLowPass
from starfish.spots._detector.trackpy_local_max_peak_finder import TrackpyLocalMaxPeakFinder


@pytest.mark.skip('issues with checksums prevent this data from working properly')
def test_allen_smFISH_cropped_data():

    # set random seed to errors provoked by optimization functions
    np.random.seed(777)

    # load the experiment
    experiment = starfish.data.allen_smFISH(use_test_data=True)

    primary_image = experiment.fov().primary_image

    clip = Clip(p_min=10, p_max=100)
    clipped_image = clip.run(primary_image, in_place=False)

    bandpass = Bandpass(lshort=0.5, llong=7, threshold=None, truncate=4)
    bandpassed_image = bandpass.run(clipped_image, in_place=False)

    clip = Clip(p_min=10, p_max=100, is_volume=False)
    clipped_bandpassed_image = clip.run(bandpassed_image, in_place=False)

    sigma = (1, 0, 0)  # filter only in z, do nothing in x, y
    glp = GaussianLowPass(sigma=sigma, is_volume=True)
    z_filtered_image = glp.run(clipped_bandpassed_image, in_place=False)

    lmpf = TrackpyLocalMaxPeakFinder(
        spot_diameter=3,
        min_mass=300,
        max_size=3,
        separation=5,
        noise_size=0.65,
        preprocess=False,
        percentile=10,
        verbose=True,
        is_volume=True,
    )
    intensities = lmpf.run(z_filtered_image)  # noqa
