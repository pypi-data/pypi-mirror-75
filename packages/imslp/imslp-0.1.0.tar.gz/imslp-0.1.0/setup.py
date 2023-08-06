# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imslp', 'imslp.helpers', 'imslp.interfaces']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'mwclient>=0.10.1,<0.11.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'imslp',
    'version': '0.1.0',
    'description': 'The clean and modern way of accessing IMSLP data and scores programmatically.',
    'long_description': '# imslp\n\n🎼 The clean and modern way of accessing IMSLP data and scores programmatically. 🎶\n\n## Installation\n\nThe package is available on PyPi and can be installed using your favorite package\nmanager:\n\n```shell\npip install imslp\n```\n\n## Data Sources\n\nThis project attempts to use robust sources of data, that do not require web scraping of some sort:\n\n- **MediaWiki API.** IMSLP is [one of tens of thousands of websites](https://wikiapiary.com/wiki/IMSLP)\nbuilt on top of [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki), the framework created for\n[Wikipedia.org](https://en.wikipedia.org/wiki/MediaWiki). As such, it can be accessed through\nthe [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page) for which, fortunately,\nthere exists a fantastic Python wrapper library called [`mwclient`](https://github.com/mwclient/mwclient).\n\n- **IMSLP API.** For convenience, the IMSLP built some *ad-hoc* scripts that can be used to get a\nlist of people and a list of works, in a variety of different formats, including JSON.\n\n### Some quirks of IMSLP\n\nWhile fortunately, as mentioned, IMSLP uses a widely used open-source Wiki platform, MediaWiki, it has a\nhandful of quirks. Such as:\n\n- Composers are stored as `Category`, for instance `Category:Scarlatti, Domenico`. For each composer,\nthere is usually three tabs: "Compositions", "Collaborations" and "Collections"; these are stored as\nseparate categories resulting from the concatenation of the composer and subtype, such as\n`Category:Scarlatti, Domenico/Collections`.\n\n- PDF files for sheet music are stored as "images"; unfortunately, for the time being, the scheme does\nnot appear in the URLs computed for the files. These need to be manually patched.\n\n- The `imslpdisclaimeraccepted` cookie must be set to `"yes"` for files to download properly (otherwise,\ndownloading any file will result in the disclaimer page). With `mwclient`, this can be specified on login.\n    ```python\n    cookies = {\n        "imslp_wikiLanguageSelectorLanguage": "en",\n        "imslpdisclaimeraccepted": "yes",\n    }\n    ```\n\n- Much of the metadata associated with images, such as the internal ID or the download counter, is stored\nseparately than the MediaWiki metadata. This makes scraping the rendered HTML page a necessary endeavour.\n\nFortunately all these quirks are handled by this package!\n\n## Related Projects\n\nHere are a handful of other related projects available on GitHub to access the IMSLP data programmatically:\n\n- [jjjake/imslp-scrape](https://github.com/): Last commit in May 2012 (32 commits), mix of Python and shell, scraping\nthe website for data (people, score links) with HTML parsing.\n\n- [FrankTheCodeMonkey/IMSLP-Scraper](https://github.com/FrankTheCodeMonkey/IMSLP-Scraper): Last commit in June 2020 \n(6 commits), Python, scraping the website for data and scores, with HTML parsing and Selenium.\n\n- [josefleventon/imslp-api](https://github.com/josefleventon/imslp-api): Last commit in May 2020 (17 commits),\nJavaScript, uses [IMSLP\'s custom API](https://imslp.org/wiki/IMSLP:API) to get the list of people and list of works\nprogrammatically through a web API query. \n\nMore recently, and in other languages:\n\n- [IMSLP Instrument Information Parsing Program](https://github.com/yoonlight/imslp): Last commit in July 2020\n(47 commits), uses scraping to extract instrumentation information. \n\n## Acknowledgements\n\nLet\'s be clear that all the heavy lifting is done by [`mwclient`](https://github.com/mwclient/mwclient)—and\nthe volunteers who uploaded and/or scanned and/or typeset the scores on IMSLP. \n\n## License\n\nThis project is licensed under the LGPLv3 license, with the understanding\nthat importing a Python modular is similar in spirit to dynamically linking\nagainst a library.\n\n- You can use the library `imslp` in any project, for any purpose, as long\n  as you provide some acknowledgement to this original project for use of\n  the library.\n\n- If you make improvements to `imslp`, you are required to make those\n  changes publicly available.\n  ',
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jlumbroso/imslp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
