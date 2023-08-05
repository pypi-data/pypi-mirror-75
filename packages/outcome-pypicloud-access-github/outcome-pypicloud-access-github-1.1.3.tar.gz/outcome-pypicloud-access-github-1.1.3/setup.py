# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome',
 'outcome.pypicloud_access_github',
 'outcome.pypicloud_access_github.graphql']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.1.0,<5.0.0',
 'dogpile.cache>=0.9.2,<0.10.0',
 'pydash>=4.8.0,<5.0.0',
 'sgqlc>=10.1,<12.0',
 'toml>=0.10.1,<0.11.0']

extras_require = \
{'memcache': ['python-memcached>=1.59,<2.0']}

setup_kwargs = {
    'name': 'outcome-pypicloud-access-github',
    'version': '1.1.3',
    'description': 'A Github-based access backend for pypicloud.',
    'long_description': '# pypicloud-access-github\n\n![ci-badge](https://github.com/outcome-co/pypicloud-access-github-py/workflows/Checks/badge.svg) ![version-badge](https://img.shields.io/badge/version-1.1.3-brightgreen)\n\nThis package provides a Github-based authentication backend for [pypicloud](https://pypicloud.readthedocs.io/en/latest/).\n\nThe package binds the PyPICloud instance to a GitHub Organization, and uses GitHub users, teams, and permissions to provide authentication and access control.\n\n## Usage\n\n### Installation\n\nYou can install the package directly from pypi, alongside your `pypicloud` installation.\n\n```sh\npoetry add outcome-pypicloud-access-github\n```\n\nOr, if you want to use `memcache` for caching.\n\n```sh\npoetry add outcome-pypicloud-access-github[memcache]\n```\n\n### Configuration\n\nYou need to configure PyPICloud to use the auth backend, in the `server.ini`:\n\n```ini\npypi.auth = outcome.pypicloud_access_github.Poetry\n\nauth.otc.github.organization = <INSERT YOUR ORGANIZATION NAME HERE>\nauth.otc.github.token = <INSERT YOUR TOKEN HERE>\n```\n\nYou can see a sample [here](./samples/server.ini).\n\n#### Caching\n\nRetrieving the authentication information from GitHub can be a relatively slow process, depending on the size of your organization. The plugin implements an internal TTL cache using [dogpile.cache](https://dogpilecache.sqlalchemy.org/en/latest/) to avoid hitting GitHub on each request.\n\nBy default the cache backend is an in-memory cache, that is not shared across threads or processes. You can configure the cache to use a `memcache` instance that will be shared amongst threads/processes.\n\n```ini\nauth.otc.github.cache.backend = memory  # Use the memory backend\nauth.otc.github.cache.expiration = 300  # Expire the cache items after 300s\n```\n\nFor `memcache`:\n\n```ini\nauth.otc.github.cache.backend = memcache  # Use the memcache backend\nauth.otc.github.cache.expiration = 300  # Expire the cache items after 300s\nauth.otc.github.cache.memcache.url = 127.0.0.1:11211  # The server:port of your memcache instance\n```\n\n#### Options\n\nThe full list of configuration options:\n\n| Option                               | \xa0Default          | Description                                                                           |\n| ------------------------------------ | ----------------- | ------------------------------------------------------------------------------------- |\n| `auth.otc.github.token`              | None              | \xa0The Github Token used to query Github for the auth information                       |\n| `auth.otc.github.organization`       | None              | The Github Organization name to use as a directory                                    |\n| `auth.otc.github.repo_pattern`       | `.*`              | A pattern that will be interpreted as a regular expression to filter repository names |\n| `auth.otc.github.repo_include_list`  | `[]`              | A list of repository names to include. Names not in the list will be excluded         |\n| `auth.otc.github.repo_exclude_list`  | `[]`              | A list of repository names to exclude. Names in the list will be excluded             |\n| `auth.otc.github.cache.backend`      | `memory`          | The cache backend to use, can be `memory` or `memcache`                               |\n| `auth.otc.github.cache.expiration`   | \xa0`300`            | The TTL for each cache key                                                            |\n| `auth.otc.github.cache.memcache.url` | `127.0.0.1:11211` | The url of the memcache server                                                        |\n\n#### Github Token\n\nYou can create a Personal Access Token from your [Developer Settings](https://github.com/settings/tokens/). The token must have `repo`, `admin:org`, and `read:user` permissions.\n\n### Publishing & Pulling Packages\n\nYou can use your standard tools to publish to the repository (see here for [Poetry](https://python-poetry.org/docs/libraries/#publishing-to-a-private-repository)). The username will be the GitHub username of the user, and the token will be a Personal Access Token assigned to that user. The token only requires `read:user` scopes as it is only used to verify the identity of the user.\n\n### How GitHub concepts are mapped to PyPICloud\n\n#### Authorization & Authentication\n\nThe GitHub ACL elements are mapped pretty intuitively onto PyPICloud ACL elements.\n\n- Users login with their username and PAT (the backend ensures that the username matches the token)\n- Permissions are defined by the GitHub roles applied either on the Team, Repository, or Organization levels\n\nThe permissions are mapped as follows:\n\n| GitHub Role | \xa0PyPI Permissions |\n| ----------- | ----------------- |\n| `admin`     | `read`, `write`   |\n| `maintain`  | `read`, `write`   |\n| `triage`    | `read`            |\n| `read`      | `read`            |\n| `write`     | `read`, `write`   |\n\n#### Packages\n\nThe backend considers each repository to be a potential package (the backend isn\'t designed for monorepos). The backend will attempt to retrieve package information from the repository. Currently, the backend only supports [Poetry](https://python-poetry.org) packages, using `pyproject.toml`, but it is easy to support other file formats by creating a new subclass of the `outcome.pypicloud_access_github.access.Access` class (see [poetry.py](./src/outcome/pypicloud_access_github/poetry.py) as an example.)\n\nFor example, the repository for this library contains a `pyproject.toml` with the following:\n\n```toml\n[tool.poetry]\nname = "outcome-pypicloud-access-github"\nversion = "0.1.0"\ndescription = "An Github-based access backend for pypicloud."\n```\n\nThe backend will read this file and determine that the package is named `outcome-pypicloud-access-github`.\n\n## Development\n\nRemember to run `./pre-commit.sh` when you clone the repository.\n\n### Testing\n\nThe testing is mainly made up of integration tests, read the [testing README](./test/README.md) for more details.\n',
    'author': 'Douglas Willcocks',
    'author_email': 'douglas@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/pypicloud-access-github-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
