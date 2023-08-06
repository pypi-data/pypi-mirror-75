# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['torchjpeg',
 'torchjpeg.codec',
 'torchjpeg.dct',
 'torchjpeg.metrics',
 'torchjpeg.quantization',
 'torchjpeg.transforms']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0', 'torch==1.5.1', 'torchvision==0.6.1']

setup_kwargs = {
    'name': 'torchjpeg',
    'version': '0.9.6.dev12',
    'description': 'Utilities for JPEG data access and manipulation in pytorch',
    'long_description': "# TorchJPEG\n\nThis package contains a C++ extension for pytorch that interfaces with libjpeg to allow for manipulation of low-level JPEG data.\nBy using libjpeg, quantization results are guaranteed to be consistent with other applications, like image viewers or MATLAB,\nwhich use libjpeg to compress and decompress images. This is useful because JPEG images can be effected by round-off\nerrors or slight differences in the decompression procedure. Besides this, this library can be used to read and write\nDCT coefficients, functionality which is not available from other python interfaces.\n\nBesides this, the library includes many utilities related to JPEG compression, many of which are written using native pytorch code meaning\nthey can be differentiated or GPU accelerated. The library currently includes packages related to the DCT, quantization, metrics, and dataset\ntransformations.\n\n## LIBJPEG\n\nCurrently builds against: `libjpeg-9d`. libjpeg is statically linked during the build process. See http://www.ijg.org/files/ for libjpeg source.\n\n## Documentation\n\nSee https://queuecumber.gitlab.io/torchjpeg/ \n\n## Install\n\nInstall using pip, note that only Linux builds are supported at the moment. \n\n```\npip install torchjpeg\n```\n\nIf there is demand for builds on other platforms it may happen in the future. Also note that the wheel is intended to be compatible with manylinux2014\nwhich means it should work on modern Linux systems, however, because of they way pytorch works, we can't actually build it using all of the manylinux2014\ntools. So compliance is not guaranteed and YMMV.\n\n",
    'author': 'Max Ehrlich',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://queuecumber.gitlab.io/torchjpeg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.9',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
