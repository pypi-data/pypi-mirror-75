# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photocrawl']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.2,<8.0.0',
 'loguru>=0.4.1,<0.5.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyexifinfo>=0.4.0,<0.5.0',
 'seaborn>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'photocrawl',
    'version': '0.2.2',
    'description': 'Analysis script of photography habits.',
    'long_description': "# PhotoCrawl: A Photography Analyzer\n\nA simple script to run analysis and get insight on my use of equipment and settings in my practice of photography.\n\n## Install\n\n### Prerequisites\n\nThis script runs on Python3.6.1+, and requires the following libraries: [`PyExifInfo`][pyexifinfo], `matplotlib`, `seaborn`, `pandas` and `loguru`.\nMost importantly, it also requires that you have the amazing [ExifTool][exiftool] package by Phil Harvey.\n\n### Install\n\nThis code is compatible with `Python 3.6+`.\nIf for some reason you have a need for it, you can simply install it in your virtual enrivonment with:\n```bash\npip install photocrawl\n```\n\n## Usage\n\nWith this package is installed in the activated enrivonment, usage is:\n```bash\npython -m photocrawl -i files_location\n```\n\nDetailed options go as follows:\n```bash\nusage: __main__.py [-h] -i IMAGES_LOCATION [-o OUTPUT_DIR]\n                   [--show-figures SHOW_FIGURES] [--save-figures SAVE_FIGURES]\n                   [-l LOG_LEVEL]\n\nPython 3.6.1+ utility to get insight on your photography practice.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i IMAGES_LOCATION, --images IMAGES_LOCATION\n                        Location, either relative or absolute, of the\n                        directory with images you wish to crawl.\n  -o OUTPUT_DIR, --output OUTPUT_DIR\n                        Location, either relative or absolute, of the output\n                        directory. Defaults to 'outputs'\n  --show-figures SHOW_FIGURES\n                        Whether or not to show figures when plotting insights.\n                        Defaults to 'False'.\n  --save-figures SAVE_FIGURES\n                        Whether or not to save figures when plotting insights.\n                        Defaults to 'True'.\n  -l LOG_LEVEL, --logs LOG_LEVEL\n                        The base console logging level. Can be 'debug',\n                        'info', 'warning' and 'error'. Defaults to 'info'.\n```\n\nThe script will crawl files, extract exif and output visualizations named `insight_1.png` and `insight_2.png` in a newly created `outputs` folder (or a folder named as you specified).\n\n## Output example\n\nHere is an example of what the script outputs:\n\n![Example_1](example_outputs/insight_1.jpg)\n\n![Example_2](example_outputs/insight_2.jpg)\n\n## TODO\n\n- [x] Handling raw files.\n- [x] Handling subfolders when looking for files.\n- [x] Output all insight in a single/two plot.\n- [x] Implement proper logging.\n- [x] Make into a package\n- [x] Make callable as a python module (`python -m photocrawl ...`)\n\n## License\n\nCopyright &copy; 2019-2020 Felix Soubelet. [MIT License][license]\n\n[exiftool]: https://www.sno.phy.queensu.ca/~phil/exiftool/\n[license]: https://github.com/fsoubelet/PhotoCrawl/blob/master/LICENSE \n[pyexifinfo]: https://github.com/guinslym/pyexifinfo",
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/PhotoCrawl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
