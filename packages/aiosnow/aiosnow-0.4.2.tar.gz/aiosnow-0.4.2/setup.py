# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosnow',
 'aiosnow.models',
 'aiosnow.models.common',
 'aiosnow.models.common.schema',
 'aiosnow.models.common.schema.fields',
 'aiosnow.models.common.schema.helpers',
 'aiosnow.models.table',
 'aiosnow.query',
 'aiosnow.request',
 'aiosnow.request.helpers',
 'aiosnow.request.response',
 'aiosnow.schemas',
 'aiosnow.schemas.table']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'marshmallow>=3.6.1,<4.0.0']

setup_kwargs = {
    'name': 'aiosnow',
    'version': '0.4.2',
    'description': 'Asynchronous Python ServiceNow library',
    'long_description': '# aiosnow: Asynchronous Python ServiceNow library\n\n[![image](https://badgen.net/pypi/v/aiosnow)](https://pypi.org/project/aiosnow)\n[![image](https://badgen.net/badge/python/3.7+?color=purple)](https://pypi.org/project/aiosnow)\n[![image](https://badgen.net/travis/rbw/aiosnow)](https://travis-ci.org/rbw/aiosnow)\n[![image](https://badgen.net/pypi/license/aiosnow)](https://raw.githubusercontent.com/rbw/aiosnow/master/LICENSE)\n[![image](https://pepy.tech/badge/snow/month)](https://pepy.tech/project/snow)\n\nThis is a simple and lightweight yet powerful and extensible library for interacting with ServiceNow that works\nwith modern versions of Python and utilizes the stdlib [asyncio](https://docs.python.org/3/library/asyncio.html) library.\n\n### asyncio\n\nIn a nutshell, asyncio uses non-blocking sockets tracked by an event loop, and while adding some complexity, it allows for running large amounts of I/O operations simultaneously, and is typically a good choice for high-concurrency backend applications.\n\n##### Scripting\n\nThe aiosnow library can, of course, be used in scripts - but requires an event loop to be created and coroutines to be written with the *async/await* syntax.\n\n\n*Example code*\n```python\n\nimport asyncio\n\nimport aiosnow\nfrom aiosnow.schemas.table import IncidentSchema as Incident\n\nsnow = aiosnow.Client("<instance>.service-now.com", basic_auth=("<username>", "<password>"))\n\nasync def main():\n    # Make a TableModel object from the built-in Incident schema\n    async with snow.get_table(Incident) as inc:\n        # Get high-priority incidents\n        for response in await inc.get(Incident.priority <= 3, limit=5):\n            print(f"Number: {response[\'number\']}, Priority: {response[\'priority\'].text}")\n\nasyncio.run(main())\n\n```\n\nCheck out the [examples directory](examples) for more.\n\n### Documentation\n\nThe aiosnow reference and more is available in the [documentation](https://aiosnow.readthedocs.io/en/latest).\n\n\n### Funding\n\nThe aiosnow code is permissively licensed, and can be incorporated into any type of application–commercial or otherwise–without costs or limitations.\nIts author believes it\'s in the commercial best-interest for users of the project to invest in its ongoing development.\n\nConsider leaving a [donation](https://paypal.vault13.org) if you like this software, it will:\n\n- Directly contribute to faster releases, more features, and higher quality software.\n- Allow more time to be invested in documentation, issue triage, and community support.\n- Safeguard the future development of aiosnow.\n\n### Development status\n\nThe fundamental components (models, client code, error handling, documentation, etc) of the library is considered complete.\nHowever, automatic testing and real-world use is somewhat lacking, i.e. there are most likely bugs lurking about,\nand the software should be considered Alpha, shortly Beta.\n\n### Contributing\n\nCheck out the [contributing guidelines](CONTRIBUTING.md) if you want to help out with code or documentation.\n\n\n### Author\n\nRobert Wikman \\<rbw@vault13.org\\>\n\n',
    'author': 'Robert Wikman',
    'author_email': 'rbw@vault13.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rbw/aiosnow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
