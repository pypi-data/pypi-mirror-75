# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcadminbot', 'mcadminbot.bot']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'discord.py>=1.3.4,<2.0.0',
 'loguru>=0.5.1,<0.6.0',
 'mctools>=1.0.0,<2.0.0',
 'systemd>=0.16.1,<0.17.0']

entry_points = \
{'console_scripts': ['mcadminbot = mcadminbot.entry:_main']}

setup_kwargs = {
    'name': 'mcadminbot',
    'version': '0.1.1',
    'description': 'A Discord bot used to manage a Minecraft server.',
    'long_description': "# mcadminbot\n\nA Discord bot that allows permitted server members and roles to administrate a Minecraft server over RCON through chat messages.\n\n## Requirements\n\n* Linux\n* Python 3.6 (likely works with higher versions but it has not yet been tested)\n* A Discord Bot Account and its accompanying token, see [the discord.py documentation](https://discordpy.readthedocs.io/en/latest/discord.html)\n* A Minecraft server with the RCON server enabled on an accessible interface and port\n* systemd development headers (see Installation)\n\n## Bot Permissions\n\nWhen generating the invitation link to add your bot to your Discord server, select the following permissions:\n\n* View Channels\n* Send Messages\n\n## Installation\n\nI highly recommend creating a virtual environment for this so that the required modules are isolated away from your system modules.\n\n1. Install the systemd development headers.\n\n    Debian:\n\n    ```shell\n    sudo apt-get install build-essential \\\n        libsystemd-journal-dev \\\n        libsystemd-daemon-dev \\\n        libsystemd-dev\n    ```\n\n    CentOS/RHEL:\n\n    `sudo yum install gcc systemd-devel`\n\n2. `cd` to your desired virtual environment location.\n3. Create the virtual environment.\n\n    `python3 -m venv mcadminbot_env`\n\n4. Activate your virtual environment.\n\n    `source mcadminbot_env/bin/activate`\n\n5. Install mcadminbot from the Python Package Index.\n\n    `pip install mcadminbot`\n\nTo run mcadminbot from the shell:\n\n`mcadminbot_env/bin/mcadminbot`\n\nHere is the usage text from `mcadminbot -h|--help`:\n\n```shell\nusage: mcadminbot [-h] [-d {start,stop,restart}] [-c CONFIG_PATH]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -d {start,stop,restart}, --daemon {start,stop,restart}\n                        manage mcadminbot as a daemon\n  -c CONFIG_PATH, --config CONFIG_PATH\n                        path to mcadminbot.yaml\n```\n\n__Note__: You could also use [pipx](https://packaging.python.org/guides/installing-stand-alone-command-line-tools/) to accomplish this.\n\n### Systemd Service Setup\n\nThis portion is optional but very recommended for ease of use.\n\n1. Create the file `/etc/systemd/system/mcadminbot.service` with the following contents, replacing paths where needed:\n\n    ```shell\n    [Unit]\n    Description=mcadminbot - A Minecraft Discord bot\n\n    [Service]\n    Type=forking\n    PIDFile=/run/mcadminbot.pid\n    ExecStart=/path/to/mcadminbot_env/bin/mcadminbot -d start\n    ExecReload=/path/to/mcadminbot_env/bin/mcadminbot -d restart\n    ExecStop=/path/to/mcadminbot_env/bin/mcadminbot -d stop\n    User=root\n    Group=root\n\n    [Install]\n    WantedBy=multi-user.target\n    ```\n\n2. Reload systemd.\n\n    `sudo systemctl daemon-reload`\n\n3. Enable mcadminbot to run on startup.\n\n    `sudo systemctl enable mcadminbot`\n\nNow, once you've followed the Configuration section, you can use the following commands to control the bot service:\n\n```shell\nsudo systemctl start mcadminbot\nsudo systemctl stop mcadminbot\nsudo systemctl restart mcadminbot\n```\n\n## Configuration\n\n### Config File Format\n\nPlease view [the default YAML config file](./mcadminbot/defaults.yaml) to see all of the available config keys.\n\n* `token` is a string containing your bot's token (NOT your client secret)\n* `command_prefix` is a string containing the character that all mcadminbot commands must start with in messages\n* `server_address` is a string containing the IP address or domain name that your Minecraft server is hosted from\n* `rcon_port` is an integer containing the port that the Minecraft server's RCON server is bound to\n* `rcon_password` is a string containing the password used to connect to the RCON server\n* `docker_container_name` is a string containing the name of the Docker container that is running your Minecraft server (optional, see the `restart-docker-server` command notes in Supported Commands)\n\nThe rest of the config keys must contain a list of only one of the following types of items:\n\n1. A single string `ALL` that grants all users or roles, depending on the key, access to that key's matching command/subcommands.\n2. A single string `NONE` that denies all users or roles, depending on the key, access to that key's matching command/subcommands.\n3. One or more strings containing specific Discord usernames or roles, depending on the key, that grants those entities access to that key's matching command/subcommands.\n\n__Special note about admin_users/admin_roles:__ Any users/roles specified here, respectively, will be granted access to every command supported by the bot.\n\n### Config File Location and Loading\n\nmcadminbot exposes the shell parameter `-c|--config` which takes a path to your desired config file. If specified, the default config is loaded first and then your specified config is merged on top to override with your custom values. Configuration is then complete and the bot starts. Be sure to edit the systemd service file shown above to include this parameter if desired.\n\nIf a desired config file is not specified with `-c|--config`, mcadminbot loads the default config and then looks for config files in two places:\n\n1. `/etc/mcadminbot/mcadminbot.yaml`\n2. `/home/$USER/mcadminbot.yaml` (the home directory of the user running the process)\n\nmcadminbot will load these files in this order; any conflicting keys specified in `/home/$USER/mcadminbot.yaml` will override the values found in `/etc/mcadminbot/mcadminbot.yaml`. Configuration is then complete and the bot starts.\n\n## Supported Commands\n\nPlease visit the [official Minecraft wiki's reference for Minecraft command syntax](https://minecraft.gamepedia.com/Commands).\n\nCurrently supported Minecraft commands:\n\n```shell\nlist\nsay\ntell\nwhitelist (and all subcommands)\nban\nban-ip\nbanlist\nkick\npardon\npardon-ip\nop\ndeop\n```\n\nCurrently supported system commands:\n\n```shell\nrestart-docker-server\n```\n\nThe `restart-docker-server` command allows permitted users and roles to restart a Docker container that is running the Minecraft server. In its current state, this will only work if the bot is running on the same server as the Docker container and therefore `server_address` is `localhost`. Be sure to set `docker_container_name` in the config.\n\n## Contributing\n\nPull requests are happily welcomed for any additions or improvements!\n\nThis project is managed through [Poetry](https://python-poetry.org/).\n\n## Todo\n\n* [ ] Implement more Minecraft commands\n* [ ] Write tests and implement automated testing of branches\n* [ ] Implement proper semantic versioning and CI/CD\n",
    'author': 'Matt Bobke',
    'author_email': 'mcbobke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcbobke/mcadminbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
