# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spellbot', 'spellbot.versions', 'spellbot.versions.versions']

package_data = \
{'': ['*'], 'spellbot': ['assets/*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'discord-py>=1.3.3,<2.0.0',
 'dunamai>=1.2.0,<2.0.0',
 'humanize>=2.5.0,<3.0.0',
 'hupper>=1.10.2,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'sqlalchemy>=1.3.17,<2.0.0',
 'unidecode>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['spellbot = spellbot:main']}

setup_kwargs = {
    'name': 'spellbot',
    'version': '3.9.3',
    'description': 'A Discord bot for SpellTable',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/lexicalunit/spellbot/master/spellbot.png" />\n\n# SpellBot\n\n[![build][build-badge]][build]\n[![pypi][pypi-badge]][pypi]\n[![codecov][codecov-badge]][codecov]\n[![python][python-badge]][python]\n[![black][black-badge]][black]\n[![mit][mit-badge]][mit]\n\nA Discord bot for [SpellTable][spelltable].\n\n[![add-bot][add-img]][add-bot]\n\n[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)][ko-fi]\n\n## 🤖 Using SpellBot\n\nOnce you\'ve connected the bot to your server, you can interact with it over\nDiscord via the following commands in any of the authorized channels. **Keep in\nmind that sometimes SpellBot will respond to you via Direct Message to avoid\nbeing too spammy in text channels.**\n\n- `!help`: Provides detailed help about all of the following commands.\n- `!about`: Get information about SpellBot and its creators.\n\n### ✋ Looking For Game\n\nFor players just looking to start some games, these commands are for you!\n\n- `!lfg`: Create a pending game for people join.\n- `!play`: Same as `!lfg`, but look for an existing game to join first.\n- `!leave`: Leave any pending games that you\'ve signed up for.\n\nWhen you run the `!lfg` command, SpellBot will post a message for sign ups.\n\n![lfg][lfg]\n\nOther users can react to it with the ➕ emoji to be added to the game. When the\ngame is ready, SpellBot will update the message with your SpellTable details.\n\n![ready][ready]\n\nUsers can also use the ➖ emoji reaction to leave the game.\n\n### 🎟️ Commands for Event Runners\n\nThese commands are intended to be run by SpellBot Admins and help facilitate\nonline events.\n\n- `!game`: Directly create games for the mentioned users.\n- `!event`: Create a bunch of games all at once based on some uploaded data.\n- `!begin`: Start an event that you previously created with `!event`.\n- `!export`: Export historical game data for your server.\n\n### 👑 Administrative Commands\n\nThese commands will help you configure SpellBot for your server.\n\n- `!spellbot`: This command allows admins to configure SpellBot for their\n               server. It supports the following subcommands:\n  - `config`: Just show the current configuration for this server.\n  - `channels`: Set the channels SpellBot is allowed to operate within.\n  - `prefix`: Set the command prefix for SpellBot in text channels.\n  - `expire`: Set how many minutes before games are expired due to inactivity.\n\n### 🤫 Secrets\n\nThere\'s some secret hidden features of SpellBot. For example if you use the\ntags `~mtgo` or `~arena` when creating a game, it will direct players to use\nthose systems instead of SpellTable. Ok, I guess that\'s not secret anymore. But\nyou kinda get the idea. Well, you\'ve been warned. Hopefully these features are\nintuitive and helpful 🤞 — and if not,\n[please report bugs and request features][issues] to your heart\'s content.\n\n## 🙌 Support Me\n\nI\'m keeping SpellBot running using my own money but if you like the bot and want\nto help me out, please consider donating to [my Ko-fi][ko-fi].\n\n## ❤️ Contributing\n\nIf you\'d like to become a part of the SpellBot development community please\nfirst know that we have a documented [code of conduct](CODE_OF_CONDUCT.md) and\nthen see our [documentation on how to contribute](CONTRIBUTING.md) for details\non how to get started.\n\n## 🔧 Running SpellBot Yourself\n\nFirst install `spellbot` using [`pip`](https://pip.pypa.io/en/stable/):\n\n```shell\npip install spellbot\n```\n\nProvide your Discord bot token with the environment variable `SPELLBOT_TOKEN`.\nAs well as your SpellTable API authorization token via `SPELLTABLE_AUTH`. You\ncan get [your bot token from Discord][discord-bot-docs]. As for the SpellTable\nAPI authorization token, you\'ll have to talk to the SpellTable developers.\nYou can join their Discord server by\n[becoming a SpellTable patron][spelltable-patron].\n\nBy default SpellBot will use sqlite3 as its database. You can however choose to\nuse another database by providing a [SQLAlchemy Connection URL][db-url]. This\ncan be done via the `--database-url` command line option or the environment\nvariable `SPELLBOT_DB_URL`. Note that, at the time of this writing, SpellBot is\nonly tested against sqlite3 and PostgreSQL.\n\nMore usage help can be found by running `spellbot --help`.\n\n## 🐳 Docker Support\n\nYou can also run SpellBot via docker. See\n[our documentation on Docker Support](DOCKER.md) for help.\n\n---\n\n[MIT][mit] © [amy@lexicalunit][lexicalunit] et [al][contributors]\n\n[add-bot]:            https://discordapp.com/api/oauth2/authorize?client_id=725510263251402832&permissions=92224&scope=bot\n[add-img]:            https://user-images.githubusercontent.com/1903876/82262797-71745100-9916-11ea-8b65-b3f656115e4f.png\n[black-badge]:        https://img.shields.io/badge/code%20style-black-000000.svg\n[black]:              https://github.com/psf/black\n[build-badge]:        https://github.com/lexicalunit/spellbot/workflows/build/badge.svg\n[build]:              https://github.com/lexicalunit/spellbot/actions\n[codecov-badge]:      https://codecov.io/gh/lexicalunit/spellbot/branch/master/graph/badge.svg\n[codecov]:            https://codecov.io/gh/lexicalunit/spellbot\n[contributors]:       https://github.com/lexicalunit/spellbot/graphs/contributors\n[db-url]:             https://docs.sqlalchemy.org/en/latest/core/engines.html\n[discord-bot-docs]:   https://discord.com/developers/docs/topics/oauth2#bots\n[issues]:             https://github.com/lexicalunit/spellbot/issues\n[ko-fi]:              https://ko-fi.com/Y8Y51VTHZ\n[lexicalunit]:        http://github.com/lexicalunit\n[lfg]:                https://user-images.githubusercontent.com/1903876/87704209-e61a0f00-c750-11ea-87d2-0d5b0a1ef42f.png\n[mit-badge]:          https://img.shields.io/badge/License-MIT-yellow.svg\n[mit]:                https://opensource.org/licenses/MIT\n[pypi-badge]:         https://img.shields.io/pypi/v/spellbot\n[pypi]:               https://pypi.org/project/spellbot/\n[python-badge]:       https://img.shields.io/badge/python-3.7+-blue.svg\n[python]:             https://www.python.org/\n[ready]:              https://user-images.githubusercontent.com/1903876/87704204-e5817880-c750-11ea-8e39-67bbe4003ddd.png\n[spelltable-patron]:  https://www.patreon.com/spelltable?fan_landing=true\n[spelltable]:         https://www.spelltable.com/\n',
    'author': 'Amy',
    'author_email': 'amy@lexicalunit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lexicalunit/spellbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
