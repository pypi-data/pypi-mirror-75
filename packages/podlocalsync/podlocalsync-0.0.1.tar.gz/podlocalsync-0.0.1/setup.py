# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['podlocalsync']
install_requires = \
['cleo>=0.8.1,<0.9.0', 'lxml>=4.5.2,<5.0.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['podlocalsync = podlocalsync:main']}

setup_kwargs = {
    'name': 'podlocalsync',
    'version': '0.0.1',
    'description': 'Manage and serve podcast RSS feeds locally',
    'long_description': "# Pod Local Sync\n\nThis utility allows you to manage a podcast RSS feed locally and spin up a small\nserver to sync it with podcast applications like macOS' Podcast.app.\n\nI wrote this since in macOS Catalina (10.15), it is no longer possible to\nmanually add local files to the app.\n\n## How to\n\nPython 3.8 is required.\n\n```bash\npip install podlocalsync\n```\n\n`podlocalsync` works in the current directory and will automatically pick up\nfiles.\n\nTo start, you need an image for the feed in the current directory:\n\n```console\n$ podlocalsync init\nFeed title: My Feed\nUsing image myimage.png.\n```\n\nThis will create `feed.toml`, which stores the information about the feed.\n\nNext, you can add episodes. `podlocalsync` will look for `*.m4a` and `.mp3`\nfiles. The publication date is also filled in from the file time.\n\n```console\n$ podlocalsync add\nEpisode audio: [episode-1.m4a]:\n [0] episode-1.m4a\n [1] episode-2.mp3\n [2] episode-3.m4a\n >\nEpisode title: My Episode about Cats\nEpisode publication date: [Fri, 31 Jul 2020 06:26:31 +0000]\n```\n\nIf you've added an episode, it will be excluded from the next `add`.\n\nFinally, you can serve the feed locally. This will create or overwrite\n`feed.rss` and spin up a server:\n\n```console\n$ podlocalsync serve\nhttp://localhost:8000/feed.rss\n^C\nKeyboard interrupt received, exiting.\n```\n\nYou can subscribe to this URL in a podcasting application, although the server\nisn't intended to be run for a long time, and certainly [don't expose it to the\ninternet](https://docs.python.org/3/library/http.server.html).\n\nIf you want to subscribe from e.g. an iPhone, use your computer's IP address\nas the hostname (and make sure the firewall allows connections):\n\n```console\n$ podlocalsync serve --host 192.168.1.136\nhttp://192.168.1.136:8000/feed.rss\n```\n\n## License\n\nThis program is licensed under the GNU General Public License 3.0. For more information, see `LICENSE`.\n",
    'author': 'Toby Fleming',
    'author_email': 'tobywf@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
