# PhotoCrawl: A Photography Analyzer

A simple script to run analysis and get insight on my use of equipment and settings in my practice of photography.

## Install

### Prerequisites

This script runs on Python3.6.1+, and requires the following libraries: [`PyExifInfo`][pyexifinfo], `matplotlib`, `seaborn`, `pandas` and `loguru`.
Most importantly, it also requires that you have the amazing [ExifTool][exiftool] package by Phil Harvey.

### Install

This code is compatible with `Python 3.6+`.
If for some reason you have a need for it, you can simply install it in your virtual enrivonment with:
```bash
pip install photocrawl
```

## Usage

With this package is installed in the activated enrivonment, usage is:
```bash
python -m photocrawl -i files_location
```

Detailed options go as follows:
```bash
usage: __main__.py [-h] -i IMAGES_LOCATION [-o OUTPUT_DIR]
                   [--show-figures SHOW_FIGURES] [--save-figures SAVE_FIGURES]
                   [-l LOG_LEVEL]

Python 3.6.1+ utility to get insight on your photography practice.

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGES_LOCATION, --images IMAGES_LOCATION
                        Location, either relative or absolute, of the
                        directory with images you wish to crawl.
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        Location, either relative or absolute, of the output
                        directory. Defaults to 'outputs'
  --show-figures SHOW_FIGURES
                        Whether or not to show figures when plotting insights.
                        Defaults to 'False'.
  --save-figures SAVE_FIGURES
                        Whether or not to save figures when plotting insights.
                        Defaults to 'True'.
  -l LOG_LEVEL, --logs LOG_LEVEL
                        The base console logging level. Can be 'debug',
                        'info', 'warning' and 'error'. Defaults to 'info'.
```

The script will crawl files, extract exif and output visualizations named `insight_1.png` and `insight_2.png` in a newly created `outputs` folder (or a folder named as you specified).

## Output example

Here is an example of what the script outputs:

![Example_1](example_outputs/insight_1.jpg)

![Example_2](example_outputs/insight_2.jpg)

## TODO

- [x] Handling raw files.
- [x] Handling subfolders when looking for files.
- [x] Output all insight in a single/two plot.
- [x] Implement proper logging.
- [x] Make into a package
- [x] Make callable as a python module (`python -m photocrawl ...`)

## License

Copyright &copy; 2019-2020 Felix Soubelet. [MIT License][license]

[exiftool]: https://www.sno.phy.queensu.ca/~phil/exiftool/
[license]: https://github.com/fsoubelet/PhotoCrawl/blob/master/LICENSE 
[pyexifinfo]: https://github.com/guinslym/pyexifinfo