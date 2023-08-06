# lfcnn - A TensorFlow framework for light field deep learning
[![build status](https://gitlab.com/iiit-public/lfcnn/badges/master/pipeline.svg)](https://gitlab.com/iiit-public/lfcnn/commits/master)
[![coverage report](https://gitlab.com/iiit-public/lfcnn/badges/master/coverage.svg)](https://gitlab.com/iiit-public/lfcnn/commits/master)
[![PyPI](https://img.shields.io/pypi/v/lfcnn.svg)](https://pypi.org/project/lfcnn/#description)
[![PyPI](https://img.shields.io/pypi/pyversions/lfcnn.svg)](https://pypi.org/project/lfcnn/#description)
[![PyPI](https://img.shields.io/pypi/status/lfcnn.svg)](https://pypi.org/project/lfcnn/#description)


[![Image](https://gitlab.com/iiit-public/lfcnn/-/wikis/uploads/c8f13881b0f2cb18f0db3247c6f2cc66/lfcnn_logo_gitlab.png)](https://gitlab.com/iiit-public/lfcnn/)


## License and Usage

This software is licensed under the GNU GPLv3 license (see below).

If you use this software in your scientific research, please cite our paper:


    Not yet available. Please check back later.


## Quick Start
Have a look at the [Documentation](https://iiit-public.gitlab.io/lfcnn) 
for notes on usage.

Furthermore, you can find some useful examples in the `examples` folder which
can help you to get started.


## Installation

It is recommended to use Conda to setup a new environment with tensorflow and GPU support.
To install with GPU support, run

```
conda create -n lfcnn python=3.8 tensorflow-gpu=2.2 tensorflow numpy scipy imageio h5py cudnn cudatoolkit
conda activate lfcnn
```

Then, install the provided package using `pip`:

```
pip install lfcnn
```

### Optional dependencies
Optionally, for some of LFCNN's features, install the following:

- `matplotlib` (via conda or pip)
- `sacred` (via pip)
- `pymongo` (via conda or pip)
- `mdbh` (via pip)


### Installation on Windows
LFCNN is mostly compatible with all TF versions TensorFlow >= 2.0, 
however there is a bug in tf.keras that causes OOMs with data generators 
(which LFCNN uses) and multithreading and -processing. 
Therefore, we specify `tensorflow >= 2.2` as a dependency, 
for which this bug has been [resolved](https://github.com/tensorflow/tensorflow/commit/e918c6e6fab5d0005fcde83d57e92b70343d3553).
 
However, as of July 2020, TF 2.2 and TF 2.3 are not released on Anaconda for Windows. 
So for Windows, it is necessary to install TF via pip. 
However, installation of the compatible cuDNN and CUDA should still be 
performed via conda for simplicity.
To setup the new environment with the correct CUDA and cuDNN versions, run

```
conda create -n lfcnn python=3.8 numpy scipy imageio h5py cudnn=7.6.5 cudatoolkit=10.1
conda activate lfcnn
pip install tensorflow==2.3 tensorflow-gpu==2.3
```
Furthermore, the [Visual C++ redistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)
has to be installed on Windows.

Finally, install LFCNN via pip as usual:

```
pip install lfcnn
```


### Testing

You can manually run the tests using `pytest`:

    $ pytest <path-to-lfcnn>/test/



### Uninstallation
Uninstall ``lfcnn`` using

    $ pip uninstall lfcnn


## Contribute
If you are interested in contributing to LFCNN, feel free to create an issue or
fork the project and submit a merge request. As this project is still undergoing
restructuring and extension, help is always welcome!


### For Programmers

Please stick to the 
[PEP 8 Python coding styleguide](https://www.python.org/dev/peps/pep-0008/).

The docstring coding style of the reStructuredText follows the 
[googledoc style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).



## License

Copyright (C) 2020  The LFCNN Authors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
