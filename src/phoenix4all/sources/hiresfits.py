from astropy.utils.data import download_file
from typing import Optional
from .core import PhoenixDataFile, WeightedPhoenixDataFile
import urllib.parse
import pathlib
from astropy import units as u
import numpy as np
from ..net.http import fetch_listing
import re
BASE_URL = "https://phoenix.astro.physik.uni-goettingen.de/data/v2.0/HiResFITS/"

PATTERN_WITH_ALPHA = re.compile(r'lte(\d{5})([+-][0-9]+\.[0-9]+)([+-][0-9]+\.[0-9]+)\.Alpha=([+-][0-9]+\.[0-9]+)\..*\.fits$')
PATTERN_WITHOUT_ALPHA = re.compile(r'lte(\d{5})([+-][0-9]+\.[0-9]+)([+-][0-9]+\.[0-9]+)\..*\.fits$')


def recursive_list(url: str) -> list:
    """Recursively list all files in a given URL directory."""
    files = []
    _, listing = fetch_listing(url)
    for item in listing:
        if item.name in ('./', '../'):
            continue
        if item.name.endswith('/'):
            # It's a directory, recurse into it
            new_url = urllib.parse.urljoin(url, item.name)
            files.extend(recursive_list(urllib.parse.urljoin(url, item.name)))
        elif item.name.endswith('.fits'):
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
    import re

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






def list_available_files(path: Optional[str] = None, 
                         base_url: Optional[str] = None,
                         url_model: str = "PHOENIX-ACES-AGSS-COND-2011",) -> list:
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
        if not model_url.endswith('/'):
            model_url += '/'
        data_files = recursive_list(str(model_url))
    


            
    return data_files

def load_file(dataset: PhoenixDataFile) -> tuple[u.Quantity, u.Quantity]:
    """Load the content of a Phoenix model file.
    
    Args:
        dataset: A PhoenixDataFile instance representing the model to load.
    Returns:
        The content of the model file as a string.
    """
    from astropy.io import fits

    local_path = dataset.filename
    if not pathlib.Path(local_path).exists():

        local_path = download_file(dataset.filename, cache=True)


    with fits.open(local_path) as hdul:
        columns = hdul[1].columns
        # logg has format g10 = log = 1.0 so convert to int
        logg = int(dataset.logg * 10)
        # No alpha enhancement in this version

        logg_index = columns.names.index(f'g{logg:02d}')
        

        data = np.array(hdul[1].data.copy()) # Assuming the data is in the first extension

        data_shape = data.shape[0]
        data_view = data.view(">f8").reshape(data_shape ,-1)
        wav = data_view[:,0]
        flux = data_view[:,logg_index]

    wav = np.array(wav) << u.AA
    flux = np.array(flux) << (u.erg / (u.s * u.cm**2 * u.AA))
    return wav, flux

def download_model(output_path: pathlib.Path, *, teff: int, logg: float, feh: float, alpha: float=0.0,
                   base_url: Optional[str] = None,
                   create_folder: bool = False) -> pathlib.Path:
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





