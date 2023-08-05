# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gender_bender']

package_data = \
{'': ['*'], 'gender_bender': ['language_models/*', 'language_models/english/*']}

install_requires = \
['EbookLib>=0.17.1,<0.18.0',
 'gender-guesser>=0.4.0,<0.5.0',
 'spacy>=2.3.2,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'titlecase>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'gender-bender',
    'version': '0.1.2',
    'description': 'Flips the gender in a text snippet or epub',
    'long_description': '## Gender Bender\n\nThis library allows you to flip the gender of a string or eBook (only works with the `epub` format).  The motivation was to be able to examine gender norms in a fun way.\n\nTo use the `epub` format, I recommend the Calibre reader or the Kobo.\n\n### Installation\n\n_Python 3 only_\n\nWith `pip`:\n```shell script\npip install gender-bender \n```\n\nor with `poetry`:\n```shell script\npoetry add gender-bender\n```\n\nNote: on first usage, it will install an English model for the Spacy dependency.  This\nis unable to be installed from PyPI due to [this issue](https://github.com/explosion/spaCy/issues/3536).\n\n### Usage\n\nOr from python:\n\n```python\nfrom gender_bender import gender_bend_epub\ngender_bend_epub(\'./Mythical_Man_Month.epub\')\n```\n\nYou can also gender-bend a string:\n\n```python\nfrom gender_bender import gender_bend\nx = gender_bend("If Ivanka weren\'t my daughter, perhaps I\'d be dating her.")\n\nassert x == "If Ivan weren\'t my son, perhaps I\'d be dating him."\n```\n\n### Installing from source\n\nGet the repo:\n\n```shell script\ngit clone https://github.com/Garrett-R/gender_bender.git\ncd gender_bender\npip install -r requirements.txt\n```\n\nIt can be run as a script:\n\n```shell script\n./main.py --input Lord_of_the_Flies.epub  --output Lady_of_the_Flies.epub\n```\n\nIf you\'d like to choose the names yourself (recommended for translating a whole ebook), you can do:\n\n```shell script\n./main.py --input The_Little_Mermaid.epub --interactive-naming\n```\n',
    'author': 'Garrett-R',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Garrett-R/gender_bender',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
