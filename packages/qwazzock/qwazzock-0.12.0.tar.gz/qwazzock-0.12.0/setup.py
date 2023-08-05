# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qwazzock']

package_data = \
{'': ['*'],
 'qwazzock': ['static/audio/*',
              'static/css/*',
              'static/dialog-polyfill/*',
              'static/icons/*',
              'static/images/*',
              'static/js/*',
              'templates/*']}

install_requires = \
['eventlet>=0.25.2,<0.26.0',
 'flask-socketio>=4.2.1,<5.0.0',
 'flask>=1.1.2,<2.0.0',
 'pyopenssl>=19.1.0,<20.0.0']

entry_points = \
{'console_scripts': ['qwazzock = qwazzock:run']}

setup_kwargs = {
    'name': 'qwazzock',
    'version': '0.12.0',
    'description': 'An app for hosting interactive quizzes.',
    'long_description': '\n# qwazzock\n\nAn app for hosting quizes remotely.\n\n## Installing\n\n`pip install qwazzock`\n\n## Usage\n\nStart an instance of the app using:\n\n`qwazzock`\n\nCreate a route to localhost:5000 using a hostname included in the SSL certificate.\n\nInstruct players to navigate to the site\'s root address (e.g. http://127.0.0.1:5000). They can then enter their name, team name and buzz when they know the answer. Note that players to be on the same team, their team names must match exactly (including case). \n\nAs a host, you can then navigate to the `/host` path (e.g. http://127.0.0.1:5000/host) in order to see who has buzzed first and to mark their answer. You can respond with the following:\n\n- `pass` can be used when no one wants to buzz in who still can, as they don\'t know the answer. It clears the hotseat if occupied (e.g if someone buzzed accidentally), and any locked out teams become unlocked.\n- `right` clears the hotseat, any locked out teams and awards the team a point.\n- `wrong` places the team who answered onto a "locked out" list, preventing them from buzzing in until the current question completed.\n\nYou can also use `reset` to wipe all data for the in progress game and start a new one.\n\nClicking on the team\'s button will lock out that team until the end of the round. This can be useful for managing elimitator rounds and the like.\n\n### Question Types\n\nThere are two "question types" you can select, `standard` or `picture`.\n\n#### Standard\n\nThis is the default question type. It allows you to ask any question and decide if the answer is right or wrong.\n\n#### Picture\n\nWhen this quesiton type is selected, all players are presnted with a randomly selected image from the `questions` folder in the content directory (see below) as their buzzer image. You will be presented with the name of the image they are seeing.\n\nThe ordering of the images is random. Once you select `pass`, `right` or `wrong`, the next image in the list will be presented. This will continue until you change question type, or you run out of question images. If the latter occurs, the question type will automatically revery back to `standard`.\n\nShould you not provide a content directory, the content directory does not contain a `questions` folder, or the `questions` folder is empty, then the question type will automatically revert back to `standard`.\n\n### Environment variables\n\nBehaviour of the application can be tweaked by setting the following environment variables:\n\n|Name|Options|Default|Description|\n|-|-|-|-|\n|`QWAZZOCK_CONTENT_PATH`|A valid absolute path.|Not set|If set, additional content is loaded into qwazzock from this directory.|\n|`QWAZZOCK_LOG_LEVEL`|`DEBUG`, `INFO`, `WARNING`, `ERROR`|`INFO`|Log application events at this level and above.|\n|`QWAZZOCK_SOCKETIO_DEBUG_MODE`|Any|Not set|If set, access logs from socketio will be output.|\n\n### Content Directory\n\nFor a more interactive experience, you can load custom content into a "content directory" and provide this to qwazzock using the `QWAZZOCK_CONTENT_PATH` environment variable.\n\nCurrently, the only supported custom content is images for use with the `picture` question type. These must be loaded into a `questions` folder within the content directory. The file name should be the answer as you wish it to appear to the host.\n\n## Development\n\n### Initialise development environment\n\n`make init`\n\n### Standup a local dev server\n\n`make dev`\n\nThe server will be accessible at https://127.0.0.1:5000.\n\n### Run all tests\n\n`make test`\n\nThis includes:\n\n- unit tests (`make unit_test`).\n- static code analysis (`make bandit`).\n- dependency vulnerability analysis (`make safety`).\n\n### Build artefacts\n\n`make build`\n\nThis includes:\n\n- pip wheel (`make build_wheel`).\n- docker image (`make build_image`).\n\n### Standup a local container\n\n`make run`\n\n### Stop local containers\n\n`make stop`\n\n### Release version\n\nTag the repository with the project version and publish the distributables to [PyPI](https://pypi.org/project/qwazzock/).\n\n*Local repo must be clean.*\n\n```\npoetry config pypi-token.pypi ${your-pypi-token}\nmake release\n```\n\n',
    'author': 'Dave Randall',
    'author_email': '19395688+daveygit2050@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
