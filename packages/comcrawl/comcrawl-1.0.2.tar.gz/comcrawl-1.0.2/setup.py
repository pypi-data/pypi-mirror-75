# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comcrawl', 'comcrawl.core', 'comcrawl.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'comcrawl',
    'version': '1.0.2',
    'description': 'A python utility for downloading Common Crawl data.',
    'long_description': '# comcrawl\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/michaelharms/comcrawl/CI)\n[![codecov](https://codecov.io/gh/michaelharms/comcrawl/branch/master/graph/badge.svg?token=FEw4KEcpRm)](https://codecov.io/gh/michaelharms/comcrawl)\n![GitHub](https://img.shields.io/github/license/michaelharms/comcrawl)\n\n_comcrawl_ is a python package for easily querying and downloading pages from [commoncrawl.org](https://commoncrawl.org).\n\n## Introduction\n\nI was inspired to make _comcrawl_ by reading this [article](https://www.bellingcat.com/resources/2015/08/13/using-python-to-mine-common-crawl/).\n\n**Note:** I made this for personal projects and for fun. Thus this package is intended for use in small to medium projects, because it is not optimized for handling gigabytes or terrabytes of data. You might want to check out [cdx-toolkit](https://pypi.org/project/cdx-toolkit/) or [cdx-index-client](https://github.com/ikreymer/cdx-index-client) in such cases.\n\n### What is Common Crawl?\n\nThe Common Crawl project is an _"open repository of web crawl data that can be accessed and analyzed by anyone"_.\nIt contains billions of web pages and is often used for NLP projects to gather large amounts of text data.\n\nCommon Crawl provides a [search index](https://index.commoncrawl.org), which you can use to search for certain URLs in their crawled data.\nEach search result contains a link and byte offset to a specific location in their [AWS S3 buckets](https://commoncrawl.s3.amazonaws.com/cc-index/collections/index.html) to download the page.\n\n### What does _comcrawl_ offer?\n\n_comcrawl_ simplifies this process of searching and downloading from Common Crawl by offering a simple API interface you can use in your python program.\n\n## Installation\n\n_comcrawl_ is available on PyPI.\n\nInstall it via pip by running the following command from your terminal:\n\n```\npip install comcrawl\n```\n\n## Usage\n\n### Basic\n\nThe HTML for each page will be available as a string in the \'html\' key in each results dictionary after calling the `download` method.\n\n```python\nfrom comcrawl import IndexClient\n\nclient = IndexClient()\n\nclient.search("reddit.com/r/MachineLearning/*")\nclient.download()\n\nfirst_page_html = client.results[0]["html"]\n```\n\n### Multithreading\n\nYou can leverage multithreading while searching or downloading by specifying the number of threads you want to use.\n\nPlease keep in mind to not overdo this, so you don\'t put too much stress on the Common Crawl servers (have a look at [Code of Conduct](#code-of-conduct)).\n\n```python\nfrom comcrawl import IndexClient\n\nclient = IndexClient()\n\nclient.search("reddit.com/r/MachineLearning/*", threads=4)\nclient.download(threads=4)\n```\n\n### Removing duplicates & Saving\n\nYou can easily combine this package with the [pandas](https://github.com/pandas-dev/pandas) library, to filter out duplicate results and persist them to disk:\n\n```python\nfrom comcrawl import IndexClient\nimport pandas as pd\n\nclient = IndexClient()\nclient.search("reddit.com/r/MachineLearning/*")\n\nclient.results = (pd.DataFrame(client.results)\n                  .sort_values(by="timestamp")\n                  .drop_duplicates("urlkey", keep="last")\n                  .to_dict("records"))\n\nclient.download()\n\npd.DataFrame(client.results).to_csv("results.csv")\n```\n\nThe urlkey alone might not be sufficient here, so you might want to write a function to compute a custom id from the results\' properties for the removal of duplicates.\n\n### Searching subsets of Indexes\n\nBy default, when instantiated, the `IndexClient` fetches a list of currently available Common Crawl indexes to search. You can also restrict the search to certain Common Crawl Indexes, by specifying them as a list.\n\n```python\nfrom comcrawl import IndexClient\n\nclient = IndexClient(["2019-51", "2019-47"])\nclient.search("reddit.com/r/MachineLearning/*")\nclient.download()\n```\n\n### Logging HTTP requests\n\nWhen debugging your code, you can enable logging of all HTTP requests that are made.\n\n```python\nfrom comcrawl import IndexClient\n\nclient = IndexClient(verbose=True)\nclient.search("reddit.com/r/MachineLearning/*")\nclient.download()\n```\n\n## Code of Conduct\n\nWhen accessing Common Crawl, please beware these guidelines posted by one of the Common Crawl maintainers:\n\nhttps://groups.google.com/forum/#!msg/common-crawl/3QmQjFA_3y4/vTbhGqIBBQAJ\n',
    'author': 'Michael Harms',
    'author_email': 'michaelharms95@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/michaelharms/comcrawl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
