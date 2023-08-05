# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['at16k', 'at16k.api']

package_data = \
{'': ['*'], 'at16k': ['bin/*', 'blocks/*', 'core/*', 'utils/*']}

install_requires = \
['progressbar>=2.5,<3.0',
 'scipy>=1.3.3,<2.0.0',
 'sentencepiece==0.1.82',
 'tensorflow==1.14']

entry_points = \
{'console_scripts': ['at16k-convert = at16k.bin.speech_to_text:main']}

setup_kwargs = {
    'name': 'at16k',
    'version': '0.1.4',
    'description': 'at16k is a Python library to perform automatic speech recognition or speech to text conversion.',
    'long_description': '[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/GlibAI/at16k/graphs/commit-activity)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![PyPI license](https://img.shields.io/pypi/l/at16k.svg)](https://pypi.python.org/pypi/at16k/)\n[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)\n<img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat">\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/at16k.svg)\n[![Downloads](https://pepy.tech/badge/at16k)](https://pepy.tech/project/at16k)\n\n# at16k\nPronounced as ***at sixteen k***.\n\n[Try out the interactive demo here.](https://at16k.com/demo)\n\n# What is at16k?\nat16k is a Python library to perform automatic speech recognition or speech to text conversion. The goal of this project is to provide the community with a production quality speech-to-text library.\n\n# Installation\nIt is recommended that you install at16k in a virtual environment.\n\n## Prerequisites\n- Python >= 3.6\n- Tensorflow = 1.14\n- Scipy (for reading wav files)\n\n\n## Install via pip\n```\n$ pip install at16k\n```\n\n## Install from source\nRequires: [poetry](https://github.com/sdispater/poetry)\n```\n$ git clone https://github.com/at16k/at16k.git\n$ poetry env use python3.6\n$ poetry install\n```\n\n# Download models\nCurrently, three models are available for speech to text conversion.\n- en_8k (Trained on English audio recorded at 8 KHz, supports offline ASR)\n- en_16k (Trained on English audio recorded at 16 KHz, supports offline ASR)\n- en_16k_rnnt (Trained on English audio recorded at 16 KHz, supports real-time ASR)\n\nTo download all the models:\n```\n$ python -m at16k.download all\n```\nAlternatively, you can download only the model you need. For example:\n```\n$ python -m at16k.download en_8k\n$ python -m at16k.download en_16k\n$ python -m at16k.download en_16k_rnnt\n```\nBy default, the models will be downloaded and stored at <HOME_DIR>/.at16k. To override the default, set the environment variable AT16K_RESOURCES_DIR.\nFor example:\n```\n$ export AT16K_RESOURCES_DIR=/path/to/my/directory\n```\nYou will need to reuse this environment variable while using the API via command-line, library or REST API.\n\n# Preprocessing audio files\nat16k accepts wav files with the following specs:\n- Channels: 1\n- Bits per sample: 16\n- Sample rate: 8000 (en_8k) or 16000 (en_16k)\n\nUse ffmpeg to convert your audio/video files to an acceptable format. For example,\n```\n# For 8 KHz\n$ ffmpeg -i <input_file> -ar 8000 -ac 1 -ab 16 <output_file>\n\n# For 16 KHz\n$ ffmpeg -i <input_file> -ar 16000 -ac 1 -ab 16 <output_file>\n```\n\n# Usage\nat16k supports two modes for performing ASR - offline and real-time. And, it comes with a handy command line utility to quickly try out different models and use cases.\n\nHere are a few examples -\n```\n# Offline ASR, 8 KHz sampling rate\n$ at16k-convert -i <path_to_wav_file> -m en_8k\n\n# Offline ASR, 16 KHz sampling rate\n$ at16k-convert -i <path_to_wav_file> -m en_16k\n\n# Real-time ASR, 16 KHz sampling rate, from a file, beam decoding\n$ at16k-convert -i <path_to_wav_file> -m en_16k_rnnt -d beam\n\n# Real-time ASR, 16 KHz sampling rate, from mic input, greedy decoding (requires pyaudio)\n$ at16k-convert -m en_16k_rnnt -d greedy\n```\nIf the ***at16k-convert*** binary is not available for some reason, replace it with - \n```\npython -m at16k.bin.speech_to_text ...\n```\n\n## Library API\nCheck [this file](https://github.com/at16k/at16k/blob/master/at16k/bin/speech_to_text.py) for examples on how to use at16k as a library.\n\n# Limitations\n\nThe max duration of your audio file should be less than **30 seconds** when using **en_8k**, and less than **15 seconds** when using **en_16k**. An error will not be thrown if the duration exceeds the limits, however, your transcript may contain errors and missing text.\n\n# License\n\nThis software is distributed under the MIT license.\n\n# Acknowledgements\n\nWe would like to thank [Google TensorFlow Research Cloud (TFRC)](https://www.tensorflow.org/tfrc) program for providing access to cloud TPUs.\n',
    'author': 'Mohit Shah',
    'author_email': 'mohit@at16k.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/at16k/at16k.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
