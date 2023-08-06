# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hint_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'colorama>=0.4.3,<0.5.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['hint = hint_cli.hint:cli']}

setup_kwargs = {
    'name': 'hint-cli',
    'version': '0.0.1',
    'description': 'Hint exists to get help on commands from the command line, without switching context or applications.',
    'long_description': "# hint\n\nHint exists to get help on commands from the command line, without switching context or applications. \n\n## Project status\n\nThis is currently a POC project I'm using to see what I find useful and how I want the project to develop. For all intents and purposes this tool is completely unsupported. I make no guarantees about backwards compatibility or commitment to responding to issues or PRs. It is a personal project which I'm happy to share, as open source software licensed with the MIT license if you find it useful and/or want any changes I would suggest forking this repo.    \n\n## Details\n\nFor the first POC this cli will pull information from GitHub from a fixed repository, branch and folder and display the contents on the command line. The markdown will be structured using headings which can also be specified. \n\n## Installation\n\nTBC once published on pypi.org. \n\nRecommended installation method is with [pipx](https://pipxproject.github.io/pipx/).\n\n## Usage\n\n`hint bash` - Output the contents of https://raw.githubusercontent.com/agarthetiger/mkdocs/master/docs/hints/bash.md\n \n`hint --help` - Show help text\n\n## Requirements\n\n* User has permissions to install software on the target system.\n* System has internet access to github.com\n\n## Concept\n\nI use GitHub Pages and MKDocs to collect notes and technical information which I personally find useful. I have a few cheat-sheets with reminders on commands I use regularly but infrequently. The `man` and `info` commands provide help on most commands, however they are very detailed and more useful commands often involve multiple cli tools. Examples bridge the gap between the low level documentation and complex infrequent commands which won't necessarily be in the command history for the current system. \n\nOften I'm using a terminal within PyCharm or VS Code and it's undesirable to switch context to a different application, navigate to a site which may not be open, get the right page and click or scroll to the relevant section. It's not an insurmountable problem, but a workflow which I wanted to optimise. \n\nThis tool was inspired in multiple ways by Thomas Stringer's post on [My Personal Wiki … Now Through the Terminal](https://medium.com/@trstringer/my-personal-wiki-now-through-the-terminal-689794e07b42). The fact that I stumbled across this while searching for something else is validation for having a tool and workflow which enables me to remain in the IDE and not switch to a browser. It's similar to taking an alcoholic to a pub and constantly offering them a drink, then saying it's his fault if he ends up drinking. Sure, there is some level of personal responsibility with the alcoholic to resist but a better solution would be to avoid the pub.\n\n## Backlog of ideas for improvement\n\n* Load configuration from file (ie. ~/.hintrc)\n* Configurable url, repo, branch and folder\n* More Ansi color output for markdown elements (bold, italic, lists, etc)\n* Improved formatting for console output not markdown\n* Tab completion for subsections, based on fetching and parsing the markdown document\n* Caching the pages locally for faster execution\n* Use a local file path for offline mode\n* Add commands to add free text to the repo using GitHub auth token\n* Add a command to add the previous command (using !! ?) To a specified section of a markdown document.\n* Index commands and provide mechanism to run an indexed command\n* Prompt for variable substitution when running indexed commands with mandatory configurable parameters.\n* Add a comment to the added commands (ie update an existing line)\n* Only use Python3 standard library modules\n* Launch GitHub webpage for topic in browser\n* Configure alternate webpage to launch MKDocs site\n* Support other cloud VCS\n* Automated build with TravisCI or CircleCI\n* Automated publish on merge to trunk\n* Extract markdown parsing code into separate python package\n* Add unit tests\n* Add automated semantic versioning based on commit/PR messages\n* If the topic matches an executable on the local system, also print the version information from it as well as the hint text\n* Grey-out commands which have a minimum version which is higher than the locally installed tool\n",
    'author': 'Andrew Garner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agarthetiger/hint/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
