# Copyright (C) 2020  The LFCNN Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from itertools import product
from typing import Optional, List, Union

import numpy as np
from scipy import ndimage


# Available/implemented augmentations, apart from cropping
AUGMENTATIONS = ["flip", "rotate", "weigh_chs", "gamma", "permute_chs", "scale"]


class AugmentResult(object):
    """Class to hold results of random augmentation operations.
    This can be used if a corresponding label augmentation
    has to be performed with the same parameters.

    The result, for example a randomly chosen scaling factor or a
    permutation list, is stored in the result attribute.
    The result attribute should always hold a dictionary.
    The value can then be obtained by calling an AugmentResult instance
    with the corresponding dictionary key.
    """
    def __init__(self):
        self._result = dict()

    def __str__(self):
        return str(self.result)

    def __repr__(self):
        return self.result

    def __call__(self, key: str):
        return self.result[key]

    @property
    def result(self):
        return self._result

    def add_result(self, key, value):
        self._result[key] = value


def lf_batch_augment(lf_batch: any,
                     augmented_shape: tuple,
                     curr_indices: List[int],
                     fix_seed: bool,
                     augment: dict,
                     aug_res: Optional[AugmentResult] = None):
    """Perform a full light field batch augmentation.

    Augmentation consists of (in the presented order)
        * Angular crop (depending on augmented_shape)
        * Spectral crop (depending on augmented_shape)
        * Random horizontal and vertical flip (if crop_only is False)
        * Random rotation by multiples of 90° (if crop_only is False)
        * Random channel weighting (if crop_only is False)
        * Random channel permutation (if crop_only is False)
        * Random spatial scaling (if crop_only is False)
        * Spatial crop to final augmented_shape.

    Args:
        lf_batch: Light field batch of shape (b, u, v, s, t, num_ch)

        augmented_shape: Target shape after augmentation.

        curr_indices: List of current light field indices.

        fix_seed: Whether to fix the seed of all random operations.

        augment: Dictionary specifying which augmentations to perform.
                 Cropping to final shape is always performed.

        aug_res: AugmentResult instance which can be used for possible
                 label augmentations.

    Returns:
        lf_batch_augmented
        Augmented light field batch of shape (b, augmented_shape)

    """

    b, u, v, s, t, num_ch = lf_batch.shape
    u_c, v_c, s_c, t_c, num_ch_c = augmented_shape

    # First, crop angular and spectrum to reduce amount of data.
    seeds = get_batch_seeds(curr_indices=curr_indices, fix_seed=fix_seed, offset=1)
    lf_batch = lf_batch_crop_angular(lf_batch, crop_shape=(u_c, v_c))
    lf_batch = lf_batch_crop_spectral(lf_batch, num_ch_cropped=num_ch_c, batch_seeds=seeds, aug_res=aug_res)

    if augment['flip']:
        # Seed and flip
        seeds = get_batch_seeds(curr_indices, fix_seed, offset=3)
        lf_batch = lf_batch_flip(lf_batch,
                                 batch_seeds=seeds, aug_res=aug_res)

    if augment['rotate']:
        # Seed and rotate
        seeds = get_batch_seeds(curr_indices, fix_seed, offset=5)
        lf_batch = lf_batch_rotate(lf_batch,
                                   batch_seeds=seeds, aug_res=aug_res)

    if augment['weigh_chs']:
        # Seed and weigh channels
        seeds = get_batch_seeds(curr_indices, fix_seed, offset=7)
        lf_batch = lf_batch_weigh_channels(lf_batch,
                                           weight_range=(0.75, 1.25),
                                           batch_seeds=seeds, aug_res=aug_res)

    if augment['gamma']:
        # Seed and gamma stretch channels
        seeds = get_batch_seeds(curr_indices, fix_seed, offset=11)
        lf_batch = lf_batch_gamma_channels(lf_batch,
                                           gamma_range=(0.8, 1.1),
                                           batch_seeds=seeds, aug_res=aug_res)

    if augment['permute_chs']:
        # Seed and permute channels
        seeds = get_batch_seeds(curr_indices, fix_seed, offset=13)
        lf_batch = lf_batch_permute_channels(lf_batch,
                                             batch_seeds=seeds, aug_res=aug_res)

    if augment['scale']:
        # Calculate scale_range
        scale_min = max(0.1 * np.ceil(10 * (s_c / s)), 0.1 * np.ceil(10 * (t_c / t)))
        scale_max = 2 - scale_min  # 1 + (1 - scale_min)

        # Seed and scale spatially
        seeds = get_batch_seeds(curr_indices, fix_seed, offset=17)
        lf_batch = lf_batch_scale(lf_batch,
                                  scale_range=(scale_min, scale_max),
                                  batch_seeds=seeds, aug_res=aug_res)

    # Seed and crop spatially
    seeds = get_batch_seeds(curr_indices, fix_seed, offset=19)
    lf_batch = lf_batch_crop_spatial(lf_batch,
                                     crop_shape=(s_c, t_c),
                                     batch_seeds=seeds, aug_res=aug_res)

    # Finally, clip values (have been normalized in base class)
    return np.clip(lf_batch, 0.0, 1.0)


def disp_batch_augment(disp_batch: any, augment: dict, aug_res: AugmentResult):
    """Perform a full disparity batch augmentation in accordance with
    the light field augmentation :func:`lf_batch_augment`.

    Not all light field augmentation have a analogous disparity augmentation.
    For example, the disparity is invariant under light field channel
    weighting and permutation.

    Args:
        disp_batch: Disparity batch of shape (b, s, t)

        crop_only: Which augmentations to perform. Cropping is always performed.

        aug_res: AugmentResult instance which holds the results from the
                 previous light field batch augmentation.

    Returns:
        disp_batch_augmented
        Augmented disparity batch.

    """
    # Remove unnecessary channel axis if necessary
    if disp_batch.shape[-1] == 1:
        disp_batch = np.squeeze(disp_batch, axis=-1)

    if augment['flip']:
        disp_batch = disp_batch_flip(disp_batch, aug_res=aug_res)

    if augment['rotate']:
        disp_batch = disp_batch_rotate(disp_batch, aug_res=aug_res)

    if augment['scale']:
        disp_batch = disp_batch_scale(disp_batch, aug_res=aug_res)

    # Crop spatially, add channel axis
    disp_batch = disp_batch_crop_spatial(disp_batch, aug_res=aug_res)
    return disp_batch[..., np.newaxis]


def lf_batch_code(lf_batch, curr_indices, fix_seed):
    """Apply spectral coding mask to a batch of light fields.

    Args:
        lf_batch: Batch of light fields.
                  Shape (b, u, v, s, t, lambda).

        curr_indices: List of current light field indices.

        fix_seed: Whether to fix the seed of all random operations.

    Returns:
        lf_batch_coded
        Shape is unchanged.
    """
    _, _, _, s, t, num_ch = lf_batch.shape

    batch_seeds = get_batch_seeds(curr_indices=curr_indices, fix_seed=fix_seed, offset=19)

    for i, seed in enumerate(batch_seeds):
        lf_batch[i] *= _create_lf_mask(s, t, num_ch, seed=seed)

    return lf_batch


def model_crop_spatial(labels, model_crop):
    """For models with spatial cropping (e.g. padding='valid',
    crop the spatial dimensions of the given labels.
    """
    start, end = model_crop

    for i, label in enumerate(labels):
        # Full light field label (b, u, v, s, t, ch)
        if label.ndim == 6:
            labels[i] = labels[i][:, :, :, start:-end, start:-end, :]

        # Light field stream (b, u, s, t, ch)
        elif label.ndim == 5:
            labels[i] = labels[i][:, :, start:-end, start:-end, :]

        # Light field subaperture or disparity (b, s, t, ch)
        elif label.ndim == 4:
            labels[i] = labels[i][:, start:-end, start:-end, :]

        else:
            raise ValueError("Unknown label dimension.")

    return labels


def shape_wrapper(input_shape: Union[list, tuple, List[list], List[tuple]]) -> List[tuple]:
    """Converts a generated_shapes attribute into the form needed by LFCNN.
    I.e. if input is a single tuple, will warp result in a list,
    if input is a single list, will convert to a tuple and wrap in a list,
    if input is a list of lists, will convert inner lists to tuples,
    if input is a list of tuple, nothing changes.

    Args:
        input_shape: Shape-linke input.

    Returns:
        List of tuples of shapes.
    """
    if not isinstance(input_shape, list):
        res = [input_shape]

    else:
        if isinstance(input_shape[0], list):
            res = [tuple(i) for i in input_shape]

        elif isinstance(input_shape[0], tuple):
            res = input_shape

        else:
            res = [tuple(input_shape)]

    return res


def _is_iterable(x):
    """Check whether variable is iterable"""
    res = True
    try:
        x.__iter__()
    except TypeError:
        res = False
    return res


def _to_list(x):
    """Convert a variable into a list.
    If input is not iterable, make it iterable (and mutable)."""

    if x is None or type(x) == str or not _is_iterable(x):
        res = [x]
    else:
        res = list(x)

    return res


def _set_seed(seed=None):
    """Sets the Numpy random seed, if necessary."""
    if seed is None:
        pass
    else:
        np.random.seed(seed)


def _reset_seed(seed=None):
    """Re-sets the Numpy random seed, if necessary."""
    if seed is not None:
        np.random.seed(None)
    else:
        pass


def single_seed_setter(f):
    """Decorator function to ensure proper seeding."""
    def seed_wrapper(*args, **kwargs):

        if "seed" not in kwargs:
            raise ValueError("No seed argument given.")
        else:
            seed = kwargs["seed"]

        # Set seed, call, reset seed
        _set_seed(seed)
        res = f(*args, **kwargs)
        _reset_seed(seed)
        return res

    return seed_wrapper


def get_batch_seeds(curr_indices: List[int], fix_seed: bool, offset: int = 0) -> List[Union[None, int]]:
    """Create a list of seeds for the current batch.
    The data index is used as a seed, so when the seed is fixed,
    all random batch operations are reproducible."""

    if fix_seed:
        seeds = [seed + offset for seed in curr_indices]
    else:
        seeds = [None for _ in curr_indices]

    return seeds


@single_seed_setter
def _create_lf_mask(s: int, t: int, num_ch: int, *, seed=None):
    """Create a color/spectral coding mask corresponding to a
    color/spectrally coded microlens array.
    """
    mask = np.zeros((s, t, num_ch))
    ch = np.random.randint(0, num_ch, size=(s, t))
    a = np.repeat(np.arange(0, s), t)
    b = np.tile(np.arange(0, t), s)
    mask[a, b, ch[a, b]] = 1.0

    return mask


def lf_batch_crop_angular(lf_batch: any, crop_shape) -> any:
    """Crop the light field batch to target angular shape.
    The light field is always cropped around the center.

    Args:
        lf_batch: Batch of light fields.
                  Shape (b, u, v, s, t, lambda).

        crop_shape: Size of the angular cropped data. Shape (u_crop, v_crop).
                    Should be odd-valued, otherwise behaviour might not
                    be as expected.

    Returns:
        lf_cropped
        Shape (b, u_crop, v_crop, s, t, lambda).

    """
    _, u_in, v_in, _, _, _ = lf_batch.shape
    u_crop, v_crop = crop_shape

    if u_crop == u_in and v_crop == v_in:
        # Nothing to do
        return lf_batch

    # Output and crop compatibility has already been checked at init
    else:
        # Crop central angular components
        off_u = (u_in - u_crop) // 2
        off_v = (v_in - v_crop) // 2
        return lf_batch[:, off_u:off_u + u_crop, off_v:off_v + v_crop, :, :, :]


def lf_batch_crop_spatial(lf_batch, crop_shape, batch_seeds,
                          aug_res: Optional[AugmentResult] = None):
    """Crop the light field batch to the target spatial shape.
    For better memory performance, the same crop is applied to all
    light fields in the batch.

    Args:
        lf_batch:    Batch of light fields.
                     Shape (b, u, v, s, t, lambda).

        crop_shape:  Size of the spatially cropped data. Shape (s_crop, t_crop).

        batch_seeds: Seeds for the current batch.

        aug_res:     Result of the random augmentation operations.
                     Can be used to pass to label augmentation.

    Returns:
        lf_batch_cropped
        Shape (b, u, v, s_crop, t_crop, lambda).

    """
    b, _, _, s_in, t_in, _ = lf_batch.shape
    s_crop, t_crop = crop_shape

    if aug_res is not None:
        aug_res.add_result("crop_shape", crop_shape)

    if s_crop == s_in and t_crop == t_in:
        # Nothing to do
        return lf_batch

    # Output and crop compatibility has already been checked at init
    else:
        # Only use first seed
        _set_seed(batch_seeds[0])
        off_s = np.random.randint(0, s_in - s_crop)
        off_t = np.random.randint(0, t_in - t_crop)
        _reset_seed(batch_seeds[0])

        if aug_res is not None:
            aug_res.add_result("offset", [off_s, off_t])

        return lf_batch[:, :, :, off_s:off_s + s_crop, off_t:off_t + t_crop, :]


def disp_batch_crop_spatial(disp_batch, aug_res: AugmentResult):
    """Crop the disparity batch to target spatial shape according to the
    crop region that the light field batch was cropped with.

    Args:
        disp_batch: Batch of  disparities.
                    Shape (b, s, t).

        aug_res:    Augmentation result of the corresponding lf_batch augmentation.

    Returns:
        lf_cropped
        Shape (b, u, v, s_crop, t_crop, lambda).

    """
    _, s_in, t_in = disp_batch.shape
    s_crop, t_crop = aug_res("crop_shape")

    if s_crop == s_in and t_crop == t_in:
        # Nothing to do
        return disp_batch

    else:
        off_s, off_t = aug_res("offset")
        return disp_batch[:, off_s:off_s + s_crop, off_t:off_t + t_crop]


def lf_batch_crop_spectral(lf_batch, num_ch_cropped: int, batch_seeds,
                           aug_res: Optional[AugmentResult] = None):
    """Crop the light field and disparity to target spectral/color shape.
    A random subset of the color channels is used.

    Args:
        lf_batch:       Batch of light fields.
                        Shape (b, u, v, s, t, lambda).

        num_ch_cropped: Number of spectral/color channels in the cropped light field.
                        Needs to be smaller than input number of channels.

        batch_seeds:    Seeds for the current batch.

        aug_res:        Result of the random augmentation operations.
                        Can be used to pass to label augmentation.

    Returns:
        lf_batch_cropped
        Shape (b, u, v, s, t, num_ch_cropped).

    """
    num_ch = lf_batch.shape[-1]

    if num_ch_cropped == num_ch:
        # Nothing to do
        return lf_batch

    else:
        # Crop random subset of color channels
        channel_order = np.arange(num_ch)
        _set_seed(batch_seeds[0])
        np.random.shuffle(channel_order)
        _reset_seed(batch_seeds[0])
        crop_channels = channel_order[:num_ch_cropped]

        if aug_res is not None:
            aug_res.add_result("crop_channels", crop_channels)

        return lf_batch[:, :, :, :, :, crop_channels]


@single_seed_setter
def _lf_flip(lf, *, seed=None):
    """Horizontally flip a single light field with 50% probability.

    Args:
        lf: Light field
            Shape (u, v, s, t, lambda).

        seed: Seed for the current batch.

    Returns:
        lf_flipped
        Shape is unchanged.
    """

    if np.random.randint(0, 2):
        return lf[::-1, :, ::-1, :, :], True
    else:
        return lf, False


def lf_batch_flip(lf_batch, batch_seeds, aug_res: Optional[AugmentResult] = None):
    """Flip light fields in light field batch horizontally with a 50:50 chance.
    Vertical flipping is not performed since it is equivalent to rotation
    by 180 degrees and horizontal flipping.

    Args:
        lf_batch:    Batch of light fields.
                     Shape (b, u, v, s, t, lambda).

        batch_seeds: Seeds for the current batch.

        aug_res: Result of the random augmentation operations.
                 Can be used to pass to label augmentation.

    Returns:
        lf_batch_flipped
        Shape is unchanged.
    """
    flips = []

    for i, seed in enumerate(batch_seeds):
        lf_batch[i], res = _lf_flip(lf_batch[i], seed=seed)

        flips.append(res)

    if aug_res is not None:
        aug_res.add_result("flips", flips)

    return lf_batch


def disp_batch_flip(disp_batch, aug_res: AugmentResult):
    """Flip disparities when corresponding light fields have been flipped.

    Args:
        disp_batch: Batch of disparities
                    Shape (b, s, t).

        aug_res: Augmentation result of the corresponding lf_batch augmentation.

    Returns:
        disp_batch_flipped
        Shape is unchanged.
    """
    flips = aug_res("flips")

    for i, flip in enumerate(flips):
        if flip:
            disp_batch[i] = disp_batch[i, ::-1, :]

    return disp_batch


@single_seed_setter
def _lf_rotate(lf, *, seed=None):
    """Random rotation through 0, 90, 180, 270 degree of single light field.

    Args:
        lf:     light field
                Shape (u, v, s, t, lambda).

        seed:   Seeds for the current light field.

    Returns:
        lf_rotated, deg (number of 90° rotations)
        Shape is unchanged.
    """

    deg = np.random.randint(0, 4)  # random number of times the array is rotated by 90 degree
    return np.rot90(np.rot90(lf, k=deg, axes=(2, 3)), k=deg, axes=(0, 1)), deg


def lf_batch_rotate(lf_batch, batch_seeds, aug_res: Optional[AugmentResult] = None):
    """Rotate each light field randomly by 0, 90, 180 or 270 degrees.

    Args:
        lf_batch: Batch of light fields.
                  Shape (b, u, v, s, t, lambda).

        aug_res: Result of the random augmentation operations.
                 Can be used to pass to label augmentation.

    Returns:
        lf_batch_rotated
        The shape is unchanged.
    """
    degs = []

    b, u, v, *_ = lf_batch.shape

    # No rotation possible if operatung on EPI volumes
    if u == 1 or v == 1:
        degs.append(0)

    else:
        for i, seed in enumerate(batch_seeds):
            lf_batch[i], deg = _lf_rotate(lf_batch[i], seed=seed)
            degs.append(deg)

    if aug_res is not None:
        aug_res.add_result("degs", degs)

    return lf_batch


def disp_batch_rotate(disp_batch, aug_res):
    """Random rotation through 0, 90, 180, 270 degree.

    Args:
        disp_batch: Batch of disparities.
                    Shape (b, s, t).

        aug_res: Augmentation result of the corresponding lf_batch augmentation.

    Returns:
        disp_batch_rotated
        The shape is unchanged.
    """
    degs = aug_res("degs")

    for i, deg in enumerate(degs):
        disp_batch[i] = np.rot90(disp_batch[i], k=deg, axes=(0, 1))

    return disp_batch


def lf_batch_scale(lf_batch, scale_range, batch_seeds,
                   aug_res: Optional[AugmentResult] = None):
    """Random scaling with a scale factor within scale_range.
    For speed, the 0 order spline interpolation (nearest) is used.
    Note that all light fields in a batch are scaled with the same
    scale factor such that shape compatibility is assured.

    Args:
        lf_batch: Batch of light fields.
                  Shape (b, u, v, s, t, lambda).

        scale_range: Tuple (a, b). A scaling factor is sampled from a
                     uniform distribution over [a, b]

        batch_seeds: Seeds for the current batch.

        aug_res: Result of the random augmentation operations.
                 Can be used to pass to label augmentation.

    Returns:
        lf_batch_scaled
        Shapes (b, u, v, s_scaled, t_scaled, lambda)
    """
    # Only use one seed here
    _set_seed(batch_seeds[0])
    s_start, s_stop = scale_range
    scaling_factor = np.random.uniform(s_start, s_stop)
    _reset_seed(batch_seeds[0])

    b, u, v, s, t, num_ch = lf_batch.shape
    s_scaled, t_scaled = np.round(scaling_factor * np.asarray((s, t))).astype(np.int)
    lf_out_shape = b, u, v, s_scaled, t_scaled, num_ch

    lf_scaled = np.empty(lf_out_shape, dtype='float32')

    # Iterate over angular and spectral component.
    # This has been shown to give the fastest performance.
    for idu, idv, ch in product(range(u), range(v), range(num_ch)):
        # Use 2D rescaling for performance
        lf_scaled[:, idu, idv, :, :, ch] = ndimage.zoom(
            lf_batch[:, idu, idv, :, :, ch], (1, scaling_factor, scaling_factor),
            order=0, mode='nearest')

    if aug_res is not None:
        aug_res.add_result("scaling_factor", scaling_factor)

    return lf_scaled


def disp_batch_scale(disp_batch, aug_res: AugmentResult):
    """Random scaling with a scale factor within scale_range.
    For speed, the 0 order spline interpolation (nearest) is used.
    Note that all light fields in a batch are scaled with the same
    scale factor such that shape compatibility is assured.

    Args:
        disp_batch: Batch of light fields.
                  Shape (b, u, v, s, t, lambda).

        aug_res: Augmentation result of the corresponding lf_batch augmentation.

    Returns:
        disp_batch_scaled
        Shapes (b, s_scaled, t_scaled, lambda)
    """
    scale = aug_res("scaling_factor")
    # Scale disparity size, but also its values due to the changed effective baseline!
    return scale*ndimage.zoom(disp_batch[:], (1, scale, scale), mode='nearest', order=0)


@single_seed_setter
def _lf_permute_channels(lf, *, seed=None):
    """Randomly permute the order of color/spectral channels.
    Args:
        lf:     Single light field.
                Shape (u, v, s, t, lambda).

        seed:   Seed for the current light field.

    Returns:
        lf_permuted
        Shape is unchanged.
    """
    num_ch = lf.shape[-1]
    channel_order = np.arange(num_ch)
    np.random.shuffle(channel_order)
    return lf[:, :, :, :, channel_order], channel_order


def lf_batch_permute_channels(lf_batch, batch_seeds,
                              aug_res: Optional[AugmentResult] = None):
    """Randomly permute the order of color/spectral channels.
    Args:
        lf_batch:    Batch of light fields.
                     Shape (b, u, v, s, t, lambda).

        batch_seeds: Seeds for the current batch.

        aug_res: Result of the random augmentation operations.
                 Can be used to pass to label augmentation.


    Returns:
        lf_batch_permuted
        Shape is unchanged.
    """

    channel_orders = []

    for i, seed in enumerate(batch_seeds):
        lf_batch[i], res = _lf_permute_channels(lf_batch[i], seed=seed)
        channel_orders.append(res)

    if aug_res is not None:
        aug_res.add_result("channel_orders", channel_orders)

    return lf_batch


@single_seed_setter
def _lf_weigh_channels(lf, weight_range, *, seed=None):
    """Randomly weigh the color/spectral channels of a light field.
    The light field values are multiplied by a random weight factor
    which is for every channel chosen uniformly from the weight_range
    interval.

    Args:
        lf:     Light field.
                Shape (u, v, s, t, lambda).

        weight_range: Tuple (a, b). A weight is sampled from a
                     uniform distribution over [a, b]

        seed:   Seed for the current light field.

    Returns:
        lf_weighted
        Shape is unchanged.
    """
    num_ch = lf.shape[-1]
    w_start, w_stop = weight_range

    # If weighting would shift values out of the dynamic range, normalize
    if w_stop > 1.0:
        norm = 1/w_stop
    else:
        norm = 1.0

    weights = np.random.uniform(w_start, w_stop, num_ch)

    return np.multiply(lf, norm*weights), weights


def lf_batch_weigh_channels(lf_batch, weight_range, batch_seeds,
                            aug_res: Optional[AugmentResult] = None):
    """Randomly weigh the color/spectral channels.
    The light field values are multiplied by a random weight factor
    which is for every channel chosen uniformly from the weight_range
    interval.

    Args:
        lf_batch:     Batch of light fields.
                Shape (b, u, v, s, t, lambda).

        weight_range: Tuple (a, b). A weight is sampled from a
                     uniform distribution over [a, b]

        batch_seeds: Seeds for the current batch.

        aug_res: Result of the random augmentation operations.
                 Can be used to pass to label augmentation.

    Returns:
        lf_batch_weighted
        Shape is unchanged.
    """
    weights = []
    for i, seed in enumerate(batch_seeds):
        lf_batch[i], res = _lf_weigh_channels(lf_batch[i], weight_range, seed=seed)
        weights.append(res)

    if aug_res is not None:
        aug_res.add_result("weights", weights)

    return lf_batch


@single_seed_setter
def _lf_gamma_channels(lf, gamma_range, *, seed=None):
    """Randomly perform gamma stretch on channels of a light field.


    Args:
        lf:     Light field.
                Shape (u, v, s, t, lambda).

        gamma_range: Tuple (a, b). A gamma value is sampled from a
                     uniform distribution over [a, b]

        seed:   Seed for the current light field.

    Returns:
        lf_gammad
        Shape is unchanged.
    """
    num_ch = lf.shape[-1]
    w_start, w_stop = gamma_range

    gammas = np.random.uniform(w_start, w_stop, num_ch)

    return np.power(lf, gammas), gammas


def lf_batch_gamma_channels(lf_batch, gamma_range, batch_seeds,
                            aug_res: Optional[AugmentResult] = None):
    """Randomly weigh the color/spectral channels.
    The light field values are multiplied by a random weight factor
    which is for every channel chosen uniformly from the weight_range
    interval.

    Args:
        lf_batch:     Batch of light fields.
                Shape (b, u, v, s, t, lambda).

        gamma_range: Tuple (a, b). A gamma value is sampled from a
                     uniform distribution over [a, b]

        batch_seeds: Seeds for the current batch.

        aug_res: Result of the random augmentation operations.
                 Can be used to pass to label augmentation.

    Returns:
        lf_batch_weighted
        Shape is unchanged.
    """
    gammas = []
    for i, seed in enumerate(batch_seeds):
        lf_batch[i], res = _lf_weigh_channels(lf_batch[i], gamma_range, seed=seed)
        gammas.append(res)

    if aug_res is not None:
        aug_res.add_result("gammas", gammas)

    return lf_batch


def rgb2grey(input):
    """Convert RGB input to grey using the CIE 1931 standard."""
    return np.sum(np.multiply(input, [0.2126, 0.7152, 0.0722]), axis=-1, keepdims=True)
