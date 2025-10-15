# Phoenix4All - The Phoenix library for the lazy astronomer

[![Release](https://img.shields.io/github/v/release/ahmed-f-alrefaie/phoenix4all)](https://img.shields.io/github/v/release/ahmed-f-alrefaie/phoenix4all)
[![Build status](https://img.shields.io/github/actions/workflow/status/ahmed-f-alrefaie/phoenix4all/main.yml?branch=main)](https://github.com/ahmed-f-alrefaie/phoenix4all/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/ahmed-f-alrefaie/phoenix4all/branch/main/graph/badge.svg)](https://codecov.io/gh/ahmed-f-alrefaie/phoenix4all)
[![Commit activity](https://img.shields.io/github/commit-activity/m/ahmed-f-alrefaie/phoenix4all)](https://img.shields.io/github/commit-activity/m/ahmed-f-alrefaie/phoenix4all)
[![License](https://img.shields.io/github/license/ahmed-f-alrefaie/phoenix4all)](https://img.shields.io/github/license/ahmed-f-alrefaie/phoenix4all)

All in one library for loading and using phoenix spectra

- **Github repository**: <https://github.com/ahmed-f-alrefaie/phoenix4all/>
- **Documentation** <https://ahmed-f-alrefaie.github.io/phoenix4all/>


## What is it?

Phoenix4All is a Python library that provides an easy-to-use interface for accessing and utilizing the PHOENIX stellar atmosphere models and synthetic spectra. It attempts to solve the infuriatingly complex process of downloading, managing, and interpolating PHOENIX models by providing a simple and efficient API that does it for you. It has been especially designed for astronomers and astrophysicists who need to work with stellar spectra in their research. But its really designed to make your life easier if you need to use PHOENIX models.

## Features

- **Lazy loading**: Download and cache models on-the-fly as needed.
- **Downloader**: A downloader to grab the models if you want to manage them yourself.
- **Interpolation**: Linearly interpolate between models to get spectra for arbitrary stellar parameters.
- **Multiple sources**: Support for different PHOENIX model sources, including high-resolution FITS files and lower-resolution ASCII files.
- **Minimal memory usage**: Only needed spectral files are downloaded then loaded into memory.
- **Command-line interface**: A CLI tool to quickly fetch and manage models from the terminal.


## Installation
You can install Phoenix4All using pip:

```bash
pip install phoenix4all
```

## Usage
Here's a simple example of how to use Phoenix4All to fetch and interpolate a PHOENIX model:

```python
from phoenix4all import get_spectrum

wavelength, flux = get_spectrum(
    teff=5778,  # Effective temperature in Kelvin
    logg=4.44,  # Surface gravity in cgs
    feh=0.0,    # Metallicity [Fe/H]
    alpha=0.0,  # Alpha element enhancement [alpha/Fe] if you're too cool for school.
    source='synphot',  # Source of the models
)

print(wavelength, flux)
```

That's it! Phoenix4All will handle the rest, downloading and caching the necessary models, and interpolating to get the desired spectrum.
Now if you have already downloaded the models, you can specify the directory where they are stored:

```python
from phoenix4all import get_spectrum
wavelength, flux = get_spectrum(
    teff=5778,
    logg=4.44,
    feh=0.0,
    alpha=0.0,
    source='synphot',
    path='/path/to/your/phoenix/models'  # Specify your local directory
)
print(wavelength, flux)
```

## Being less lazy

You can work directly with the sources if you want more control:

```python
from phoenix4all import SynphotSource

source = SynphotSource(path='/path/to/your/phoenix/models')
spectrum = source.spectrum(teff=5778, logg=4.44, feh=0.0, alpha=0.0)
wavelength, flux = spectrum
print(wavelength, flux)
```

Its faster since theres less overhead in figuring out which files are available.

## Downloading 

Ohhhh fancy! You can also use the command-line interface to fetch a model:

```bash
python -m phoenix4all.downloader /path/to/store synphot --teff-range 5000 6000 --logg-range 0 2 --feh 0.0 --alpha 0.0
```

This will download all models with effective temperatures between 5000K and 6000K, surface gravities between 0 and 2, metallicity [Fe/H] of 0.0, and alpha element enhancement [alpha/Fe] of 0.0 from the synphot source.

## Supported Sources

Right now, Phoenix4All supports the following PHOENIX model sources:

- **HiResFITS**: High-resolution FITS files from the [PHOENIX project](https://phoenix.astro.physik.uni-goettingen.de/data/v2.0/HiResFITS/).
- **Synphot**: FITS files from [STSCI](https://archive.stsci.edu/hlsps/reference-atlases/cdbs/grid/phoenix/)


## TODO

- Add support for more sources (e.g., BT-Settl, NextGen).
- Make an auto guessing function to figure out which source to use based on available files.

## Contributing

For the love of God, please do. Open an issue or a pull request on GitHub. Really just adding more sources would be amazing.

## License 

Phoenix4All is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

