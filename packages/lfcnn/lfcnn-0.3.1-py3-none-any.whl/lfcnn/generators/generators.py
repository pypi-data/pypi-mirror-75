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

from typing import List, Tuple

from .abstracts import BaseGenerator
from .utils import AugmentResult, lf_batch_augment, disp_batch_augment, rgb2grey


class LfGenerator(BaseGenerator):
    """Generates light field batches and light field labels."""

    def __init__(self, *args, **kwargs):
        super(LfGenerator, self).__init__(*args, **kwargs)
        self._label_names = ["light_field"]

    def process_data(self,
                     lf_batch: any,
                     labels: List[any],
                     curr_indices: List[int]) -> Tuple[any, List[any]]:
        """Processes a batch of sample and labels.

        Here, no label inputs are assumed. The light field batch
        is also returned as the label list.

        Args:

            lf_batch: Batch of light fields.

            labels: Batch of corresponding labels. Here, should be an empty list.

            curr_indices: List of current sample indices.

        Returns:
            Tuple of lf_batch, [lf_batch].
            The light field batch is also returned as the label.
        """
        lf_batch = lf_batch_augment(lf_batch=lf_batch,
                                    augmented_shape=self.augmented_shape,
                                    curr_indices=curr_indices,
                                    fix_seed=self.fix_seed,
                                    augment=self.augment)

        # Return light field copy as label
        return lf_batch, [lf_batch.copy()]


class DisparityGenerator(BaseGenerator):
    """Generates light field batches and central view disparity labels."""

    def __init__(self, *args, **kwargs):
        super(DisparityGenerator, self).__init__(*args, **kwargs)
        self._label_names = ["disparity"]

    def process_data(self,
                     lf_batch: any,
                     labels: List[any],
                     curr_indices: List[int]) -> Tuple[any, List[any]]:
        """Processes a batch of light fields and disparity as label.

        Args:

            lf_batch: Batch of light fields.

            labels: Single element list containing a batch of disparities.

            curr_indices: List of current sample indices.

        Returns:
            Tuple (lf_batch, [disp_batch]).
        """
        # Create empty augmentation result instance
        aug_res = AugmentResult()

        # Perform light field batch augmentation, save results in aug_res
        lf_batch = lf_batch_augment(lf_batch=lf_batch,
                                    augmented_shape=self.augmented_shape,
                                    curr_indices=curr_indices,
                                    fix_seed=self.fix_seed,
                                    augment=self.augment,
                                    aug_res=aug_res)

        # Perform corresponding disparity batch augmentation
        disp_batch = disp_batch_augment(disp_batch=labels[0],
                                        augment=self.augment,
                                        aug_res=aug_res)

        # Return light field and disparity as label
        return lf_batch, [disp_batch]


class CentralAndDisparityGenerator(BaseGenerator):
    """Generates light field batches and central view as well as disparity labels."""

    def __init__(self, *args, **kwargs):
        super(CentralAndDisparityGenerator, self).__init__(*args, **kwargs)
        self._label_names = ["disparity", "central_view"]

    def process_data(self,
                     lf_batch: any,
                     labels: List[any],
                     curr_indices: List[int]) -> Tuple[any, List[any]]:
        """Processes a batch of light fields and labels.

        Here, the light field's central view and the disparity are returned
        as the labels.

        Args:

            lf_batch: Batch of light fields.

            labels: Single element list containing a batch of disparities.

            curr_indices: List of current sample indices.

        Returns:
            Tuple (lf_batch, [disp_batch, central_view_batch]).
        """
        # Create empty augmentation result instance
        aug_res = AugmentResult()

        # Perform light field batch augmentation, save results in aug_res
        lf_batch = lf_batch_augment(lf_batch=lf_batch,
                                    augmented_shape=self.augmented_shape,
                                    curr_indices=curr_indices,
                                    fix_seed=self.fix_seed,
                                    augment=self.augment,
                                    aug_res=aug_res)

        # Perform corresponding disparity batch augmentation
        disp_batch = disp_batch_augment(disp_batch=labels[0],
                                        augment=self.augment,
                                        aug_res=aug_res)

        # Crop central view from light field before coding
        _, u, v, _, _, _ = lf_batch.shape
        u_center = u // 2
        v_center = v // 2

        # Copy central view, so it does not get coded
        central_view = lf_batch[:, u_center, v_center, :, :, :].copy()

        # Return disparity and central view as labels
        return lf_batch, [disp_batch, central_view]


class LfDownSampleGenerator(BaseGenerator):
    """Generates downsampled light field batches and originally sized
    (and thus superresolved w.r.t. to the input) light field labels.
    Currently, downsampling is performed by nearest neighbor interpolation
    without anti-aliasing due to perfomance.

    TODO: Add different downsampling strategies.
    """

    def __init__(self, du=1, dv=1, ds=2, dt=2, dch=1, bw=False, *args, **kwargs):
        """

        Args:
            du: Downsample factor of u-axis.

            dv: Downsample factor of v-axis.

            ds: Downsample factor of s-axis.

            dt: Downsample factor of t-axis.

            dch: Downsample factor of channel-axis.

            bw: Whether to convert RGB to greyvalues.
        """
        super(LfDownSampleGenerator, self).__init__(*args, **kwargs)
        self._label_names = ["light_field"]
        self.du = du
        self.dv = dv
        self.ds = ds
        self.dt = dt
        self.dch = dch
        self.bw = bw

    def process_data(self,
                     lf_batch: any,
                     labels: List[any],
                     curr_indices: List[int]) -> Tuple[any, List[any]]:
        """Processes a batch of sample and labels.

        Here, no label inputs are assumed.
        The input light field is downsampled while the label corresponds to
        the original light field. This can be used to train CNNs for
        light field super-resolution.
        By "downsampling" we here refer to a simple sub-view of the light field,
        taking every x-th element along the corresponding axis. No downsampling
        in the sense of signal processing (e.g. accounting for aliasing)
        is performed.

        Args:

            lf_batch: Batch of light fields.

            labels: Batch of corresponding labels. Here, should be an empty list.

            curr_indices: List of current sample indices.

        Returns:
            Tuple of lf_downsampled_batch, [lf_batch].
            The light field batch is also returned as the label.
        """
        lf_batch = lf_batch_augment(lf_batch=lf_batch,
                                    augmented_shape=self.augmented_shape,
                                    curr_indices=curr_indices,
                                    fix_seed=self.fix_seed,
                                    augment=self.augment)

        if self.bw:
            lf_batch = rgb2grey(lf_batch)

        label = [lf_batch.copy()]

        # Return downsampled light field copy as label
        return lf_batch[:, ::self.du, ::self.dv, ::self.ds, ::self.dt, ::self.dch], label
