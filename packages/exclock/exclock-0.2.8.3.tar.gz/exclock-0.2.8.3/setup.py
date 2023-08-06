# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exclock', 'exclock.mains']

package_data = \
{'': ['*'], 'exclock': ['assets/clock/*', 'assets/sound/*']}

install_requires = \
['json5', 'tqdm', 'ycontract']

entry_points = \
{'console_scripts': ['exclock = exclock.main:main']}

setup_kwargs = {
    'name': 'exclock',
    'version': '0.2.8.3',
    'description': 'exclock is a cui extended timer.',
    'long_description': 'Exclock\n================================================================================\n\n.. image:: https://img.shields.io/pypi/v/exclock\n  :alt: PyPI\n  :target: https://pypi.org/project/exclock/\n\n.. image:: https://img.shields.io/pypi/pyversions/exclock\n  :alt: PyPI - Python Version\n  :target: https://pypi.org/project/exclock/\n\n.. image:: https://gitlab.com/yassu/exclock/badges/master/pipeline.svg\n  :target: https://gitlab.com/yassu/exclock/pipelines/latest\n\n.. image:: https://gitlab.com/yassu/exclock/badges/master/coverage.svg\n  :target: https://gitlab.com/yassu/exclock/-/commits/master\n\n.. image:: https://img.shields.io/pypi/l/exclock\n  :alt: PyPI - License\n  :target: https://gitlab.com/yassu/exclock/-/raw/master/LICENSE\n\n\n`exclock` is a cui extended timer.\n\nRequired\n----------\n\n* mplayer\n* xmessage or terminal-notifier(If you use mac, I recommend terminal-notifier)\n\nHow to install\n--------------------------------------------------------------------------------\n\n::\n\n  $ pip install exclock\n\nUsage\n----------\n\n::\n\n    $ exclock [options] {clock-filename}\n\nFeatures\n--------------------------------------------------------------------------------\n\n* Sound an alarm at a specified time.\n* Sound the alarm after the specified time has elapsed.\n* You can flexibly set the alarm.\n\nOptions\n--------------------------------------------------------------------------------\n\n* `--version`: show program\'s version number and exit\n* `-h, --help`: show this help message and exit\n* `-l, --list`: show clock names in your PC and exit\n* `-t, --time`: Time which spends until or to specified\n* `-r, --ring-filename`: Sound-filename which used for ringing with `-t, --time` option. Note that you can use EXCLOCK_RING_FILENAME system variable if you often indicate ring-filename option.\n* `--trace, --traceback`: show traceback\n\nHow to sound an alarm at a specified time\n--------------------------------------------------------------------------------\n\nEnter\n\n::\n\n    $ exclock -t {time}\n\nformat command.\n\nWhere time is given in the `{hour}:{min}` or `{hour}:{min}:{sec}` format.\n\nEx.\n\n::\n\n    $ exclock -t "1:00"\n    $ exclock -t "1:00:20"\n\nHow to sound the alarm after the specified time has elapsed\n--------------------------------------------------------------------------------\n\nEnter\n\n::\n\n    $ exclock -t {time}\n\nformat command.\n\nWhere time is given in the `{sec}`, `{sec}s`, `{min}m` or `{min}m{sec}s`.\n\nEx.\n\n::\n\n    $ exclock -t 3\n    $ exclock -t 3s\n    $ exclock -t 2m\n    $ exclock -t 2m3s\n\nHow to flexibly set the alarm\n--------------------------------------------------------------------------------\n\nEnter\n\n::\n\n    $ exclock {clock-filename}\n\nformat command.\nAlthough `{clock-filename}` can be omitted as descrived below.\n\nclock-file should be a file in json5 format.\n\nOfficial page for json5 format is `Here <https://json5.org/>`_.\n\nclock file format\n--------------------------------------------------------------------------------\n\n::\n\n    {\n      "title": "title(optional)",\n      "sounds": {\n        "time1": {\n          "message": "message1",\n          "sound_filename": "sound_filename1",\n        },\n        "time2":{\n        "message": "message2",\n        "sound_filename": "sound_filename2",\n        },\n        ...\n      },\n      "loop": loop_number(optional)\n    }\n\n* title(Optional): string which be used for notification.  Then the property is computed from clock-filename if this option is not indicated.\n* sounds: dictionary from time to dictionary which includes message and sound_filename.\n\n  - time format is "{sec}", "{sec}s", "{min}m" or "{min}m{sec}s" format.\n\n  - message is a string which be used for notification and terminal output. Then message is replaced by "{count}" to number of how many times execute.\n\n  - sound_filename is a string which be used for play the sound.\n\n* loop(Option): number of iterations for above clock timer. If this is nil, this means repeatation a number of times. Default value is 1.\n\nThere are sample files in `sample dir in gitlab <https://gitlab.com/yassu/exclock/-/tree/master/exclock/assets/clock>`_.\n\nHow to omit clock filename\n--------------------------------------------------------------------------------\n\nClock filename can be omitted for some case.\n\nRules are\n\n* If extension of clock filename is .json5, extension can be omitted(ex: pomodoro.json5 => pomodoro).\n* If dir is in the specified directory(~/.config/exclock/clock/ or environment variable EXCLOCK_CLOCK_DIR), dir is omitted (ex: ~/.config/exclock/clock/abc.json5 => abc).\n* Buitin clock file can be accessed. There are in `sample dir in gitlab`_ (ex: 3m or pomodoro).\n\nHow to omit sound filename\n--------------------------------------------------------------------------------\n\nSound filename can be omitted for some case.\n\nRules are\n\n* If dir is in the specified directory(~/.config/exclock/sound/ or environment variable EXCLOCK_SOUND_DIR), dir is omitted (ex: ~/.config/exclock/sound/abc.mp3 => abc.mp3).\n* Buitin sound file can be accessed. There are in `sample sound dir in gitlab <https://gitlab.com/yassu/exclock/-/tree/master/exclock/assets/sound>`_ (ex: silent.mp3 or ring.mp3).\n\nLICENSE\n-------\n\n`Apache 2.0 <https://gitlab.com/yassu/exclock/blob/master/LICENSE>`_\n',
    'author': 'yassu',
    'author_email': 'yasu0320.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/yassu/exclock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
