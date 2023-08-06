# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alacritty_colorscheme']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['alacritty-colorscheme = alacritty_colorscheme.cli:main']}

setup_kwargs = {
    'name': 'alacritty-colorscheme',
    'version': '0.2.0',
    'description': 'Change colorscheme of alacritty with ease',
    'long_description': '# Alacritty Colorscheme\n\nChange colorscheme of alacritty with ease.\n\n![Usage](https://user-images.githubusercontent.com/4928045/38159826-c451861a-34d0-11e8-979b-34b67027fb87.gif)\n\n## Usage\n\n```\nusage: alacritty-colorscheme [-h] (-s | -l | -a colorscheme | -t colorschemes [colorschemes ...] | -T) [-r] [-c configuration file] [-C colorscheme directory] [-V]\n\nChange colorscheme of alacritty with ease.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s, --show-applied    Show applied colorscheme\n  -l, --list-available  List available colorschemes\n  -a colorscheme, --apply colorscheme\n                        Apply colorscheme\n  -t colorschemes [colorschemes ...], --toggle colorschemes [colorschemes ...]\n                        Toggle colorschemes\n  -T, --toggle-available\n                        Toggle all available colorschemes\n  -r, --reverse-toggle  Toggle through colorschemes in reverse order\n  -c configuration file, --config-file configuration file\n                        Path to configuration file\n  -C colorscheme directory, --colorscheme-directory colorscheme directory\n                        Path to colorscheme directory\n  -V, --base16-vim      Support base16-vim\n```\n\n## Installation\n\nYou can install it from pip:\n\n```bash\npip install --user alacritty-colorscheme\n```\n\n## Running locally\n\n```bash\n# Install poetry\npip install --user poetry\n\n# Get program\ngit clone https://github.com/toggle-corp/alacritty-colorscheme.git\n\n# Run program\ncd alacritty-colorscheme\npoetry install\npoetry run python alacritty_colorscheme/cli.py\n```\n\n## Getting themes\n\nYou can get themes from [aaron-williamson/base16-alacritty](https://github.com/aaron-williamson/base16-alacritty)\n\n```bash\nDEST="$HOME/.aaron-williamson-alacritty-theme"\n\n# Get themes\ngit clone https://github.com/aaron-williamson/base16-alacritty.git $DEST\n```\n\nYou can alternatively get themes from from [eendroroy/alacritty-theme](https://github.com/eendroroy/alacritty-theme)\n\n```bash\nDEST="$HOME/.eendroroy-alacritty-theme"\n\n# Get themes\ngit clone https://github.com/eendroroy/alacritty-theme.git $DEST\n```\n\n## Synchronizing with vim/neovim\n\nIf you are using base16 colorschemes from\n[base16-vim](https://github.com/chriskempson/base16-vim), you can use the `-V`\nargument to generate `~/.vimrc_background` file when you change alacritty\ncolorscheme.\n\nYou will need to source the file in your vimrc to load the appropriate\ncolorscheme in vim. Add the following in your vimrc file:\n\n```vim\nif filereadable(expand("~/.vimrc_background"))\n  let base16colorspace=256          " Remove this line if not necessary\n  source ~/.vimrc_background\nendif\n```\n\nAfter changing alacritty colorscheme, you need to simply reload your vimrc\nconfiguration.\n\n### Reloading neovim\n\nIf you are using neovim, you can use\n[neovim-remote](https://github.com/mhinz/neovim-remote) to reload the nvim\nsessions externally.\n\nInstall neovim-remote:\n\n```bash\npip install --user neovim-remote\n```\n\nReload a neovim session using:\n\n```bash\nnvr -cc "source ~/.config/nvim/init.vim"\n```\n\n## Example bash/zsh configuration (base16-vim + neovim + neovim-remote)\n\nYou can add this example configuration in your .zshrc or .bashrc to switch\nbetween dark and light theme.\nThis snippet creates two aliases namely: `day`, `night`\n\n```bash\nfunction reload_nvim {\n    for SERVER in $(nvr --serverlist); do\n        nvr -cc "source ~/.config/nvim/init.vim" --servername $SERVER &\n    done\n}\n\nCOLOR_DIR="$HOME/.aaron-williamson-alacritty-theme/colors"\nLIGHT_COLOR=\'base16-gruvbox-light-soft.yml\'\nDARK_COLOR=\'base16-gruvbox-dark-soft.yml\'\n\nalias day="alacritty-colorscheme -C $COLOR_DIR -a $LIGHT_COLOR -V && reload_nvim"\nalias night="alacritty-colorscheme -C $COLOR_DIR -a $DARK_COLOR -V && reload_nvim"\n```\n\n## Example i3wm/sway configuration\n\n```bash\nset $color_dir $HOME/.aaron-williamson-alacritty-theme/colors\nset $light_color base16-gruvbox-light-soft.yml\nset $dark_color base16-gruvbox-dark-soft.yml\n\n# Toggle between light and dark colorscheme\nbindsym $mod+Shift+n exec alacritty-colorscheme -C $color_dir -t $light_color $dark_color\n\n# Toggle between all available colorscheme\nbindsym $mod+Shift+m exec alacritty-colorscheme -C $color_dir -T\n\n# Get notification with current colorscheme\nbindsym $mod+Shift+b exec notify-send "Alacritty Colorscheme" `alacritty-colorscheme -C $color_dir -s`\n```\n\n## License\n\nContent of this repository is released under the [Apache License, Version 2.0].\n\n[Apache License, Version 2.0](./LICENSE-APACHE)\n',
    'author': 'Safar Ligal',
    'author_email': 'weathermist@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/toggle-corp/alacritty-colorscheme/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
