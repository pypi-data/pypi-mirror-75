# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastflix',
 'fastflix.builders',
 'fastflix.plugins',
 'fastflix.plugins.av1',
 'fastflix.plugins.common',
 'fastflix.plugins.gif',
 'fastflix.plugins.hevc',
 'fastflix.plugins.svt_av1',
 'fastflix.plugins.vp9',
 'fastflix.widgets',
 'fastflix.widgets.panels']

package_data = \
{'': ['*'], 'fastflix': ['data/*', 'data/rotations/*']}

install_requires = \
['PySide2>=5.15.0,<6.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'python-box[all]>=5.0.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'reusables>=0.9.5,<0.10.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'shiboken2>=5.15.0,<6.0.0']

entry_points = \
{'console_scripts': ['fastflix = fastflix.__main__:main']}

setup_kwargs = {
    'name': 'fastflix',
    'version': '2.3.2',
    'description': 'Easy to use video encoder GUI wrapper',
    'long_description': '[![Build status](https://ci.appveyor.com/api/projects/status/208k29cvoq8xwf8j/branch/master?svg=true)](https://ci.appveyor.com/project/cdgriffith/fastflix/branch/master)\n\n# FastFlix\n\nFastFlix is a AV1 and HEVC encoder, GIF maker, and general ffmpeg command wrapper.\n\nIt can encode videos into HEVC, AV1, GIF, and VP9, and is easily extendable!\n\nRead more about it and the licensing in the [docs](docs/README.md) folder.\n\n![preview](https://raw.githubusercontent.com/cdgriffith/binary-files/fast-flix/media/fastflix/2.0.0/main.png)\n\n\n# Encoders\n\nCurrently there is support for:\n\n* HEVC (libx265)\n* AV1 (SVT-AV1)\n* AV1 (FFMPEG libaom - currently very slow)\n* VP9\n* GIF\n\n\n# Releases\n\n## Windows\nView the [releases](https://github.com/cdgriffith/FastFlix/releases) for 64 bit Windows binaries (Generated via Appveyor and also [available there](https://ci.appveyor.com/project/cdgriffith/fastflix)).\n\n## MacOS and Linux\n\nPlease use [pipx](https://pipxproject.github.io/pipx/installation/) to install as a properly virtualized app\n\n```\npipx install fastflix\n```\n\n## Running from source code or without pipx\n\n```\ngit clone https://github.com/cdgriffith/FastFlix.git\ncd FastFlix\npython3 -m venv venv\n. venv/bin/activate\npip install -r requirements.txt\npython -m flix\n```\n\n# License\n\nCopyright (C) 2019-2020 Chris Griffith\n\nThis software is licensed under the MIT which you can read in the `LICENSE` file.\n\nThis software dynamically links PySide2 which is [LGPLv3 licensed](https://doc.qt.io/qt-5/lgpl.html) and can change the\nlibrary used by specifying two environment variables, `SHIBOKEN2` and `PYSIDE2` which must point to the `__init__.py` file for the respective libraries.\n\n',
    'author': 'Chris Griffith',
    'author_email': 'chris@cdgriffith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
