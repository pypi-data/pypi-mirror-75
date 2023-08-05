# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text2excel']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.4,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1,<2']}

entry_points = \
{'console_scripts': ['text2excel = text2excel.cli:main']}

setup_kwargs = {
    'name': 'text2excel',
    'version': '0.4.0',
    'description': 'Converts to Excel XLSX from a TSV or CSV text file.',
    'long_description': '# text2excel\n\nThis program converts CSV Or TSV text files to Microsoft Excel format. It\nuses [openpyxl] to create Excel files.\n\nAs input it takes tab-separated `*.txt` files (TSV), or any CSV files\n(Comma-Separated Values) that can be auto-detected by the Python standard\nlibrary [csv] module.\n\n* There is a [GitHub page for text2excel][text2excel]\n\n[text2excel]: https://github.com/harkabeeparolus/text2excel\n[openpyxl]: https://openpyxl.readthedocs.io/\n[csv]: https://docs.python.org/3/library/csv.html\n\n## Example\n\n```bash\n$ printf "one\\ttwo\\tthree\\n1\\t2\\t3\\n" | tee my_data_file.txt\none two three\n1   2   3\n\n$ text2excel --numbers my_data_file.txt\nSaved to file: my_data_file.xlsx\n```\n\n## Installation\n\nI recommend installing *text2excel* with [pipx]:\n\n```bash\npipx install text2excel\n```\n\nIf you don\'t already have it, a guide for how to install _pipx_ is provided\nbelow on this page.\n\nTo upgrade *text2excel* to the latest version, simply run:\n\n```bash\npipx upgrade text2excel\n```\n\nOr `pipx upgrade-all` if you want to go crazy. 😉\n\nIf you want to bundle up *text2excel* into a single, standalone executable Python\n[zipapp], I highly recommend [shiv]. For example:\n\n```bash\nshiv -o text2excel -p "/usr/bin/env python3" -c text2excel text2excel\n```\n\nIf _shiv_ doesn\'t work for you for some reason, you can also use [PEX]:\n\n```bash\npex -o text2excel -c text2excel text2excel\n```\n\n[pipx]: https://github.com/pipxproject/pipx/\n[shiv]: https://github.com/linkedin/shiv\n[PEX]: https://github.com/pantsbuild/pex\n[zipapp]: https://docs.python.org/3/library/zipapp.html\n\n### Installing pipx\n\nI suggest installing everything with [pipx], because it is fantastic. 🙂\n\n```bash\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\n```\n\nAt this point, you may need to logout to refresh your shell `$PATH` before\nproceeding.\n\nFor further details, see the official\n[pipx installation guide](https://pipxproject.github.io/pipx/installation/).\n\n### Installing shiv\n\nI recommend that you use _pipx_ to install shiv:\n\n```bash\npipx install shiv\n```\n\nAlternatively, if you really don\'t want to use pipx for some reason, you can\nsimply run `python3 -m pip install --user shiv`. Then, if necessary, manually\nreconfigure your shell `$PATH` to find any pip installed binaries.\n\n## News\n\nPlease see the [changelog](CHANGELOG.md) for more details.\n\n## Contributing\n\nDo you want to help out with this project?\n\n* Please check the [CONTRIBUTING](CONTRIBUTING.md) guide.\n\n## Credits\n\nThis project was originally based on\n[a Gist by Konrad Förstner](https://gist.github.com/konrad/4154786).\n',
    'author': 'Fredrik Mellström',
    'author_email': '11281108+harkabeeparolus@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/harkabeeparolus/text2excel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
