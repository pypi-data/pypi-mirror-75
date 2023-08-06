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


"""Test lfcnn.generator
"""
from pytest import raises

import h5py
from tempfile import TemporaryDirectory
import numpy as np

from lfcnn.generators import get, BaseGenerator
from lfcnn.generators import DisparityGenerator, CentralAndDisparityGenerator
from lfcnn.generators import LfDownSampleGenerator, LfGenerator
from lfcnn.generators.reshapes import lf_identity
from lfcnn.generators.utils import AUGMENTATIONS

ALL_GENERATORS = {
    "LfGenerator": LfGenerator,
    "DisparityGenerator": DisparityGenerator,
    "CentralAndDisparityGenerator": CentralAndDisparityGenerator,
    "LfDownSampleGenerator": LfDownSampleGenerator
}


def get_base_args():

    dat = ((2**16 -1)*np.random.rand(64, 9, 9, 32, 32, 3)).astype(np.uint16)
    lbl = np.random.rand(64, 32, 32)
    data = dict(data=dat, label=lbl)
    data_key = "data"
    label_keys = ["label"]
    augmented_shape = (9, 9, 32, 32, 3)
    generated_shape = [(9, 9, 32, 32, 3)]
    reshape_func = lf_identity
    batch_size = 64
    range_data = 2**16-1
    range_labels = None
    data_percentage = 1
    model_crop = None
    augment = {key: False for key in AUGMENTATIONS}
    shuffle = False
    use_mask = False
    fix_seed = True

    gen_kwargs = dict(
        data=data,
        data_key=data_key,
        label_keys=label_keys,
        augmented_shape=augmented_shape,
        generated_shape=generated_shape,
        reshape_func=reshape_func,
        batch_size=batch_size,
        range_data=range_data,
        range_labels=range_labels,
        data_percentage=data_percentage,
        model_crop=model_crop,
        augment=augment,
        shuffle=shuffle,
        use_mask=use_mask,
        fix_seed=fix_seed)

    return gen_kwargs


def test_get():

    # Test available generators
    for gen_name in ALL_GENERATORS:
        res = get(gen_name)

        assert res == ALL_GENERATORS[gen_name]

    # Test nonsense generator
    with raises(ValueError) as e:
        _ = get("nonsense")
    assert "Unknown generator" in str(e)

    return


def test_generator_base_init():

    gen_kwargs = get_base_args()
    gen = BaseGenerator(**gen_kwargs)

    assert gen.data == gen_kwargs['data']
    assert gen.data_key == gen_kwargs['data_key']
    assert gen.label_keys == gen_kwargs['label_keys']
    assert gen.augmented_shape == gen_kwargs['augmented_shape']
    assert gen.generated_shape == gen_kwargs['generated_shape']
    assert gen._reshape == gen_kwargs['reshape_func']
    assert gen.batch_size == gen_kwargs['batch_size']
    assert gen.range_data == gen_kwargs['range_data']
    assert gen.range_labels == gen_kwargs['range_labels']
    assert gen.data_percentage == gen_kwargs['data_percentage']
    assert gen.model_crop == gen_kwargs['model_crop']
    assert gen.augment == gen_kwargs['augment']
    assert gen.shuffle == gen_kwargs['shuffle']
    assert gen.use_mask == gen_kwargs['use_mask']
    assert gen.fix_seed == gen_kwargs['fix_seed']
    return


def test_data_input():

    gen_kwargs = get_base_args()

    # Test Dict data input
    dat = np.random.rand(64, 9, 9, 32, 32, 3)
    lbl = np.random.rand(64, 32, 32, 3)
    data = dict(data=dat, label=lbl)
    gen_kwargs['data'] = data

    gen = BaseGenerator(**gen_kwargs)
    assert len(gen) == 1
    assert gen.data == data
    assert np.array_equal(gen.data['data'], dat)
    assert np.array_equal(gen.data['label'], lbl)

    # Test multi label input
    lbl_keys = ["lbl1", "lbl2", "lbl3"]
    lbl1 = np.random.rand(64, 32, 32, 3)
    lbl2 = "string_label"
    lbl3 = 12.0
    lbl = [lbl1, lbl2, lbl3]
    data = dict(data=dat, lbl1=lbl1, lbl2=lbl2, lbl3=lbl3)
    gen_kwargs['data'] = data
    gen_kwargs['label_keys'] = lbl_keys

    gen = BaseGenerator(**gen_kwargs)
    assert gen.data == data
    assert np.array_equal(gen.data['data'], dat)

    assert np.array_equal(gen.data['lbl1'], lbl1)
    assert np.array_equal(gen.data['lbl2'], lbl2)
    assert np.array_equal(gen.data['lbl3'], lbl3)

    # Test no label input
    gen_kwargs['label_keys'] = None
    gen = BaseGenerator(**gen_kwargs)
    data, label = gen.read_curr_data(range(64))
    assert label == []

    # Test h5 data input
    dat = np.random.rand(64, 9, 9, 32, 32, 3).astype(np.float32)
    lbl = np.random.rand(64, 32, 32).astype(np.float32)
    batch_size = 64

    with TemporaryDirectory() as tempdir:
        # Create temporary h5 file
        fname = tempdir + "/testfile.h5"

        with h5py.File(fname, 'w') as fh:
            fh.create_dataset('data', data=dat)
            fh.create_dataset('label', data=lbl)

        gen_kwargs['data'] = fname
        gen_kwargs['data_key'] = "data"
        gen_kwargs['label_keys'] = "label"
        gen_kwargs['batch_size'] = batch_size

        gen = BaseGenerator(**gen_kwargs)
        data, label = gen.read_curr_data(range(64))
        assert np.array_equal(data, dat)
        assert np.array_equal(label[0], lbl)

        # Test no label input
        gen_kwargs['label_keys'] = None
        gen = BaseGenerator(**gen_kwargs)
        data, label = gen.read_curr_data(range(64))
        assert label == []

    # Test wrong data input
    gen_kwargs = get_base_args()
    gen_kwargs['data'] = (1.0, 2.0, 3.4)
    with raises(TypeError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Data needs to be a dict or file system path (str or Path)." in str(e)


    return


def test_data_shape():
    # Data shape 64, 9, 9, 32, 32, 3
    gen_kwargs = get_base_args()

    gen_kwargs['augmented_shape'] = (7, 7, 34, 34, 3)
    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Incompatible augmented shape" in str(e)

    gen_kwargs['augmented_shape'] = (11, 11, 32, 32, 3)
    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Incompatible augmented shape" in str(e)

    gen_kwargs['augmented_shape'] = (9, 9, 32, 32, 13)
    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Incompatible augmented shape" in str(e)

    gen_kwargs['augmented_shape'] = (10, 11, 35, 36, 4)
    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Incompatible augmented shape" in str(e)

    return


def test_shuffle():
    gen_kwargs = get_base_args()
    gen_kwargs['shuffle'] = False
    gen = BaseGenerator(**gen_kwargs)
    assert np.array_equal(gen.indices, np.arange(64))
    gen.on_epoch_end()
    assert np.array_equal(gen.indices, np.arange(64))
    gen.on_epoch_end()
    assert np.array_equal(gen.indices, np.arange(64))

    # Test shuffle, epoch number is used as seed
    gen_kwargs['shuffle'] = True
    gen = BaseGenerator(**gen_kwargs)
    gt = np.arange(64)
    np.random.seed(1)
    np.random.shuffle(gt)
    assert np.array_equal(gen.indices, gt)
    gen.on_epoch_end()
    np.random.seed(2)
    np.random.shuffle(gt)
    assert np.array_equal(gen.indices, gt)
    gen.on_epoch_end()
    np.random.seed(3)
    np.random.shuffle(gt)
    assert np.array_equal(gen.indices, gt)


def test_data_normalization():

    gen_kwargs = get_base_args()
    dat = ((2**16 - 1)*np.ones((64, 9, 9, 32, 32, 3))).astype(np.uint16)
    lbl1 = ((2**16 - 1)*np.ones((64, 32, 32))).astype(np.uint16)
    lbl2 = ((2 ** 8 - 1) * np.ones((64, 32, 32, 3))).astype(np.uint8)
    lbl3 = np.ones((64, 32, 32, 13)).astype(np.float32)
    lbl4 = "string"
    data = dict(data=dat, lbl1=lbl1, lbl2=lbl2, lbl3=lbl3, lbl4=lbl4)
    data_key = "data"
    label_keys = ["lbl1", "lbl2", "lbl3", "lbl4"]
    data_range = 2**16 - 1
    label_range = [2**16 - 1, 2**8 - 1, None, None]

    gen_kwargs["data_key"] = data_key
    gen_kwargs["label_keys"] = label_keys
    gen_kwargs["data"] = data
    gen_kwargs["range_data"] = data_range
    gen_kwargs["range_labels"] = label_range

    class MockGenerator(BaseGenerator):
        def __init__(self, *args, **kwargs):
            super(MockGenerator, self).__init__(*args, **kwargs)

            return

        # Mock process_data function
        def process_data(self, lf_batch, labels, curr_indices):
            return lf_batch, labels

    gen = MockGenerator(**gen_kwargs)
    data, labels = gen.__getitem__(0)
    # Check that all data has been normalized correctly
    assert np.array_equal(np.ones((64, 9, 9, 32, 32, 3), dtype=np.float32), data)
    assert np.array_equal(np.ones((64, 32, 32), dtype=np.float32), labels["output_0"])
    assert np.array_equal(np.ones((64, 32, 32, 3), dtype=np.float32), labels["output_1"])
    assert np.array_equal(np.ones((64, 32, 32, 13), dtype=np.float32), labels["output_2"])
    assert "string" == labels["output_3"]

    gen_kwargs["range_labels"] = ["lbl"]
    with raises(ValueError) as e:
        gen = MockGenerator(**gen_kwargs)
        data, labels = gen.__getitem__(0)
    assert "Expected 4 range_labels, got 1." in str(e)

    # Check no label normalization
    gen_kwargs["range_labels"] = [None, None, None, None]

    gen = MockGenerator(**gen_kwargs)
    data, labels = gen.__getitem__(0)
    # Check that normalization has been performed
    assert np.array_equal((2**16 - 1)*np.ones((64, 32, 32), dtype=np.uint16), labels["output_0"])
    assert np.array_equal((2**8 - 1)*np.ones((64, 32, 32, 3), dtype=np.uint8), labels["output_1"])
    assert np.array_equal(np.ones((64, 32, 32, 13), dtype=np.float32), labels["output_2"])

    return


def test_data_percentage():

    gen_kwargs = get_base_args()
    gen_kwargs['batch_size'] = 8

    gen_kwargs['data_percentage'] = 0.5
    gen = BaseGenerator(**gen_kwargs)
    assert len(gen.indices) == 32

    gen_kwargs['data_percentage'] = 0.75
    gen = BaseGenerator(**gen_kwargs)
    assert len(gen.indices) == 48

    gen_kwargs['batch_size'] = 64
    gen_kwargs['data_percentage'] = 0.5
    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Insufficient number of data points. Found 32 for a batch size of 64" in str(e)

    gen_kwargs['data_percentage'] = 1.5
    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Found data_percentage > 1.0. Use a value between 0 and 1." in str(e)

    return


def test_augment_init():
    gen_kwargs = get_base_args()

    # Test augment all True
    gen_kwargs['augment'] = True
    gen = BaseGenerator(**gen_kwargs)
    assert gen.augment == {key: True for key in AUGMENTATIONS}

    # Test augment all False
    gen_kwargs['augment'] = False
    gen = BaseGenerator(**gen_kwargs)
    assert gen.augment == {key: False for key in AUGMENTATIONS}

    # Test missing entry
    gen_kwargs['augment'] = dict(flip=True)

    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Missing augmentation key(s)" in str(e)

    # Test unknown entry
    aug = {k: True for k in AUGMENTATIONS}
    aug['nonsense'] = False
    gen_kwargs['augment'] = aug

    with raises(ValueError) as e:
        gen = BaseGenerator(**gen_kwargs)
    assert "Unknown augmentation key(s)" in str(e)

    return


def test_lf_generator():
    gen_kwargs = get_base_args()
    data = gen_kwargs['data']['data']
    gen = LfGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data / (2**16 - 1))
    assert np.allclose(labels['light_field'], data / (2**16 - 1))

    return


def test_lf_downsample_generator():
    gen_kwargs = get_base_args()
    data = gen_kwargs['data']['data']

    # Test standard downsampling s, t factor 2
    gen_kwargs['generated_shape'] = [(9, 9, 16, 16, 3)]
    gen = LfDownSampleGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data[:, :, :, ::2, ::2] / (2**16 - 1))
    assert np.allclose(labels['light_field'], data / (2**16 - 1))

    # Test downsampling s, t factor 4
    gen_kwargs['generated_shape'] = [(9, 9, 8, 8, 3)]
    gen_kwargs['ds'] = 4
    gen_kwargs['dt'] = 4
    gen = LfDownSampleGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data[:, :, :, ::4, ::4] / (2**16 - 1))
    assert np.allclose(labels['light_field'], data / (2**16 - 1))

    # Test downsampling u, v factor 2
    gen_kwargs['generated_shape'] = [(5, 5, 32, 32, 3)]
    gen_kwargs['du'] = 2
    gen_kwargs['dv'] = 2
    gen_kwargs['ds'] = 1
    gen_kwargs['dt'] = 1
    gen = LfDownSampleGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data[:, ::2, ::2] / (2**16 - 1))
    assert np.allclose(labels['light_field'], data / (2**16 - 1))

    # Test downsampling ch factor 2
    gen_kwargs['generated_shape'] = [(9, 9, 32, 32, 2)]
    gen_kwargs['du'] = 1
    gen_kwargs['dv'] = 1
    gen_kwargs['ds'] = 1
    gen_kwargs['dt'] = 1
    gen_kwargs['dch'] = 2
    gen = LfDownSampleGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data[..., ::2] / (2**16 - 1))
    assert np.allclose(labels['light_field'], data / (2**16 - 1))

    # Test greyscale conversion
    gen_kwargs['generated_shape'] = [(9, 9, 32, 32, 1)]
    gen_kwargs['bw'] = 1
    gen = LfDownSampleGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert lf_batch.shape == (64, 9, 9, 32, 32, 1)

    return


def test_disparity_generator():
    gen_kwargs = get_base_args()

    # Test no channel exis label
    d = np.random.rand(64, 32, 32)
    gen_kwargs['data']['label'] = d
    data = gen_kwargs['data']['data']
    disp = gen_kwargs['data']['label']
    gen = DisparityGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data / (2**16 - 1))
    assert np.allclose(labels['disparity'], disp[..., np.newaxis])

    # Test no channel exis label
    d = np.random.rand(64, 32, 32, 1)
    gen_kwargs['data']['label'] = d
    data = gen_kwargs['data']['data']
    disp = gen_kwargs['data']['label']
    gen = DisparityGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data / (2**16 - 1))
    assert np.allclose(labels['disparity'], disp)

    return


def test_center_and_disparity_generator():
    gen_kwargs = get_base_args()

    # Test no channel exis label
    d = np.random.rand(64, 32, 32)
    gen_kwargs['data']['label'] = d
    data = gen_kwargs['data']['data']
    disp = gen_kwargs['data']['label']
    gen = CentralAndDisparityGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data / (2**16 - 1))
    assert np.allclose(labels['disparity'], disp[..., np.newaxis])
    # Central view of 9x9 LF is (u, v) = (5, 5) -> index starts at 0 -> (4, 4)
    assert np.allclose(labels['central_view'], lf_batch[:, 4, 4])

    # Test no channel exis label
    d = np.random.rand(64, 32, 32, 1)
    gen_kwargs['data']['label'] = d
    data = gen_kwargs['data']['data']
    disp = gen_kwargs['data']['label']
    gen = CentralAndDisparityGenerator(**gen_kwargs)

    lf_batch, labels = gen.__getitem__(0)
    assert np.allclose(lf_batch, data / (2**16 - 1))
    assert np.allclose(labels['disparity'], disp)
    # Central view of 9x9 LF is (u, v) = (5, 5) -> index starts at 0 -> (4, 4)
    assert np.allclose(labels['central_view'], lf_batch[:, 4, 4])

    return
