<img align="right" src="https://raw.githubusercontent.com/lexicalunit/spellbot/master/spellbot.png" />

# SpellBot

[![build][build-badge]][build]
[![pypi][pypi-badge]][pypi]
[![codecov][codecov-badge]][codecov]
[![python][python-badge]][python]
[![black][black-badge]][black]
[![mit][mit-badge]][mit]

A Discord bot for [SpellTable][spelltable].

[![add-bot][add-img]][add-bot]

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)][ko-fi]

## 🤖 Using SpellBot

Once you've connected the bot to your server, you can interact with it over
Discord via the following commands in any of the authorized channels. **Keep in
mind that sometimes SpellBot will respond to you via Direct Message to avoid
being too spammy in text channels.**

- `!help`: Provides detailed help about all of the following commands.
- `!about`: Get information about SpellBot and its creators.

### ✋ Looking For Game

For players just looking to start some games, these commands are for you!

- `!lfg`: Create a pending game for people join.
- `!play`: Same as `!lfg`, but look for an existing game to join first.
- `!leave`: Leave any pending games that you've signed up for.

When you run the `!lfg` command, SpellBot will post a message for sign ups.

![lfg][lfg]

Other users can react to it with the ➕ emoji to be added to the game. When the
game is ready, SpellBot will update the message with your SpellTable details.

![ready][ready]

Users can also use the ➖ emoji reaction to leave the game.

### 🎟️ Commands for Event Runners

These commands are intended to be run by SpellBot Admins and help facilitate
online events.

- `!game`: Directly create games for the mentioned users.
- `!event`: Create a bunch of games all at once based on some uploaded data.
- `!begin`: Start an event that you previously created with `!event`.
- `!export`: Export historical game data for your server.

### 👑 Administrative Commands

These commands will help you configure SpellBot for your server.

- `!spellbot`: This command allows admins to configure SpellBot for their
               server. It supports the following subcommands:
  - `config`: Just show the current configuration for this server.
  - `channels`: Set the channels SpellBot is allowed to operate within.
  - `prefix`: Set the command prefix for SpellBot in text channels.
  - `expire`: Set how many minutes before games are expired due to inactivity.

### 🤫 Secrets

There's some secret hidden features of SpellBot. For example if you use the
tags `~mtgo` or `~arena` when creating a game, it will direct players to use
those systems instead of SpellTable. Ok, I guess that's not secret anymore. But
you kinda get the idea. Well, you've been warned. Hopefully these features are
intuitive and helpful 🤞 — and if not,
[please report bugs and request features][issues] to your heart's content.

## 🙌 Support Me

I'm keeping SpellBot running using my own money but if you like the bot and want
to help me out, please consider donating to [my Ko-fi][ko-fi].

## ❤️ Contributing

If you'd like to become a part of the SpellBot development community please
first know that we have a documented [code of conduct](CODE_OF_CONDUCT.md) and
then see our [documentation on how to contribute](CONTRIBUTING.md) for details
on how to get started.

## 🔧 Running SpellBot Yourself

First install `spellbot` using [`pip`](https://pip.pypa.io/en/stable/):

```shell
pip install spellbot
```

Provide your Discord bot token with the environment variable `SPELLBOT_TOKEN`.
As well as your SpellTable API authorization token via `SPELLTABLE_AUTH`. You
can get [your bot token from Discord][discord-bot-docs]. As for the SpellTable
API authorization token, you'll have to talk to the SpellTable developers.
You can join their Discord server by
[becoming a SpellTable patron][spelltable-patron].

By default SpellBot will use sqlite3 as its database. You can however choose to
use another database by providing a [SQLAlchemy Connection URL][db-url]. This
can be done via the `--database-url` command line option or the environment
variable `SPELLBOT_DB_URL`. Note that, at the time of this writing, SpellBot is
only tested against sqlite3 and PostgreSQL.

More usage help can be found by running `spellbot --help`.

## 🐳 Docker Support

You can also run SpellBot via docker. See
[our documentation on Docker Support](DOCKER.md) for help.

---

[MIT][mit] © [amy@lexicalunit][lexicalunit] et [al][contributors]

[add-bot]:            https://discordapp.com/api/oauth2/authorize?client_id=725510263251402832&permissions=92224&scope=bot
[add-img]:            https://user-images.githubusercontent.com/1903876/82262797-71745100-9916-11ea-8b65-b3f656115e4f.png
[black-badge]:        https://img.shields.io/badge/code%20style-black-000000.svg
[black]:              https://github.com/psf/black
[build-badge]:        https://github.com/lexicalunit/spellbot/workflows/build/badge.svg
[build]:              https://github.com/lexicalunit/spellbot/actions
[codecov-badge]:      https://codecov.io/gh/lexicalunit/spellbot/branch/master/graph/badge.svg
[codecov]:            https://codecov.io/gh/lexicalunit/spellbot
[contributors]:       https://github.com/lexicalunit/spellbot/graphs/contributors
[db-url]:             https://docs.sqlalchemy.org/en/latest/core/engines.html
[discord-bot-docs]:   https://discord.com/developers/docs/topics/oauth2#bots
[issues]:             https://github.com/lexicalunit/spellbot/issues
[ko-fi]:              https://ko-fi.com/Y8Y51VTHZ
[lexicalunit]:        http://github.com/lexicalunit
[lfg]:                https://user-images.githubusercontent.com/1903876/87704209-e61a0f00-c750-11ea-87d2-0d5b0a1ef42f.png
[mit-badge]:          https://img.shields.io/badge/License-MIT-yellow.svg
[mit]:                https://opensource.org/licenses/MIT
[pypi-badge]:         https://img.shields.io/pypi/v/spellbot
[pypi]:               https://pypi.org/project/spellbot/
[python-badge]:       https://img.shields.io/badge/python-3.7+-blue.svg
[python]:             https://www.python.org/
[ready]:              https://user-images.githubusercontent.com/1903876/87704204-e5817880-c750-11ea-8e39-67bbe4003ddd.png
[spelltable-patron]:  https://www.patreon.com/spelltable?fan_landing=true
[spelltable]:         https://www.spelltable.com/
