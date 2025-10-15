import functools
import pathlib
import re
import urllib.parse
from typing import Optional

import numpy as np
from astropy import units as u
from astropy.utils.data import download_file

from ..net.http import fetch_listing
from .core import PhoenixDataFile

BASE_URL = "https://phoenix.astro.physik.uni-goettingen.de/data/v2.0/HiResFITS/"

WAVE_URL = "https://phoenix.astro.physik.uni-goettingen.de/data/v2.0/HiResFITS/WAVE_PHOENIX-ACES-AGSS-COND-2011.fits"


# Ignore anything before lte and after .fits
PATTERN_WITH_ALPHA = re.compile(
    r".*lte(\d{5})([+-][0-9]+\.[0-9]+)([+-][0-9]+\.[0-9]+)\.Alpha=([+-][0-9]+\.[0-9]+)\..*\.fits$"
)
PATTERN_WITHOUT_ALPHA = re.compile(r".*lte(\d{5})([+-][0-9]+\.[0-9]+)([+-][0-9]+\.[0-9]+)\..*\.fits$")


@functools.lru_cache(maxsize=100)
def recursive_list(url: str) -> list:
    """Recursively list all files in a given URL directory.

    Args:
        url: The base URL to start listing from.
    Returns:
        A list of all file URLs found recursively.

    """
    files = []
    _, listing = fetch_listing(url)
    for item in listing:
        if item.name in ("./", "../"):
            continue
        if item.name.endswith("/"):
            # It's a directory, recurse into it
            new_url = urllib.parse.urljoin(url, item.name)
            files.extend(recursive_list(urllib.parse.urljoin(url, item.name)))
        elif item.name.endswith(".fits"):
            # It's a file, add to the list
            files.append(urllib.parse.urljoin(url, item.name))
    return files


def parse_filename(filename: str) -> Optional[PhoenixDataFile]:
    """Parse a Phoenix model filename to extract its parameters.

    Args:
        filename: The Phoenix model filename.
    Returns:
        A PhoenixDataFile instance with extracted parameters, or None if parsing fails.
    """
    # There are two forms of the files names
    # ALpha enhancement:
    # lte02300-0.00+0.5.Alpha=+0.60.[SOME MODEL NAME WE DONT CARE ABOUT].fits
    # No alpha enhancement:
    # lte02300-0.00-0.0.[SOME MODEL NAME WE DONT CARE ABOUT].fits

    # Format is
    # lte<temperature>-<logg>+/-<feh>.[SOME MODEL NAME WE DONT CARE ABOUT].fits
    # or
    # lte<temperature>-<logg>+/-<feh>.Alpha=+/-<alpha>.[SOME MODEL NAME WE DONT CARE ABOUT].fits

    match = PATTERN_WITH_ALPHA.match(filename)
    if match:
        teff = int(match.group(1))
        logg = float(match.group(2))
        feh = float(match.group(3))
        alpha = float(match.group(4))
        return PhoenixDataFile(teff=teff, logg=-logg, feh=feh, alpha=alpha, filename=filename)
    match = PATTERN_WITHOUT_ALPHA.match(filename)
    if match:
        teff = int(match.group(1))
        logg = float(match.group(2))
        feh = float(match.group(3))
        alpha = 0.0
        return PhoenixDataFile(teff=teff, logg=-logg, feh=feh, alpha=alpha, filename=filename)
    return None


def load_wavelength_grid(path: Optional[str] = None, url: Optional[str] = None) -> u.Quantity:
    """Load the wavelength grid

    Args:
        path: Optional local path to the wavelength grid file. If None, downloads to astropy cache.
        url: Optional URL to download the wavelength grid from. Defaults to the standard Gottingen model url.
    Returns:
        The wavelength grid as an astropy Quantity.
    """
    url = url or WAVE_URL
    local_path = download_file(url, cache=True) if path is None else path
    from astropy.io import fits

    with fits.open(local_path) as hdul:
        data = hdul[0].data.copy()  # Assuming the data is in the first extension

    return np.asarray(data) << u.AA


def list_available_files(
    path: Optional[str] = None,
    base_url: Optional[str] = None,
    url_model: str = "PHOENIX-ACES-AGSS-COND-2011",
) -> list:
    """List available Phoenix model files from the catalogue.

    Args:
        path: Optional local path where the catalogue file is stored. If None, downloads to a temporary location.
        base_url: Optional base URL to download the catalogue from. Defaults to the standard Phoenix STSCI model url.

    Returns:
        A list of filenames available in the Phoenix model catalogue.
    """
    # if path is given walk through the directory and list all fits files
    if path:
        path = pathlib.Path(path)
        data_files = path.rglob("*.fits")
        data_files = [str(f) for f in data_files]

    else:
        base_url = base_url or BASE_URL
        # We recuresively list all files in the base_url
        # Make sure model_url ends with /

        model_url = urllib.parse.urljoin(base_url, url_model)
        if not model_url.endswith("/"):
            model_url += "/"
        data_files = recursive_list(str(model_url))
    print(data_files[:5])
    data_files = [parse_filename(f) for f in data_files]

    return data_files


def load_file(dataset: PhoenixDataFile, wavelength_grid: u.Quantity) -> tuple[u.Quantity, u.Quantity]:
    """Load the content of a Phoenix model file.

    Args:
        dataset: A PhoenixDataFile instance representing the model to load.
    Returns:
        The content of the model file as a string.
    """

    local_path = dataset.filename
    if not pathlib.Path(local_path).exists():
        local_path = download_file(dataset.filename, cache=True)

    wav = wavelength_grid
    # erg/s/cm^2/cm
    flux = np.array(flux) << (u.erg / (u.s * u.cm**2) / u.cm)
    return wav, flux


def download_model(
    output_path: pathlib.Path,
    *,
    teff: int,
    logg: float,
    feh: float,
    alpha: float = 0.0,
    base_url: Optional[str] = None,
    create_folder: bool = False,
) -> pathlib.Path:
    """Download a specific Phoenix model file based on the given parameters.

    Args:
        output_path: Local path to save the downloaded model file.
        teff: Effective temperature of the desired model.
        logg: Surface gravity of the desired model.
        feh: Metallicity of the desired model.
        alpha: Alpha element enhancement of the desired model (default is 0.0).
        base_url: Optional base URL to download the catalogue from. Defaults to the standard Phoenix STSCI model url.
    Returns:
        The local file path to the downloaded model file.
    """
    base_url = base_url or BASE_URL
    files = list_available_files(base_url=base_url)
