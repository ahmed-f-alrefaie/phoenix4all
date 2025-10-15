from astropy.utils.data import download_file
from typing import Optional
from .core import PhoenixDataFile, WeightedPhoenixDataFile
import urllib.parse
import pathlib
from astropy import units as u
import numpy as np

BASE_URL = "https://archive.stsci.edu/hlsps/reference-atlases/cdbs/grid/phoenix/"

def get_catalogue(*,path: Optional[pathlib.Path] = None,
                  base_url: Optional[str] = None) -> pathlib.Path:
    """Download the Phoenix model catalogue file if not already present locally.
    
    Args:
        path: Optional local path to save the catalogue file. If None, downloads to a temporary location.
        base_url: Optional base URL to download the catalogue from. Defaults to the standard Phoenix STSCI model url.
    Returns:
        The local file path to the downloaded catalogue file.
    """
    url = urllib.parse.urljoin(base_url or BASE_URL, "catalog.fits")
    local_path = download_file(url, cache=True) if path is None else path
    return pathlib.Path(local_path)

def list_available_files(path: Optional[str] = None, base_url: Optional[str] = None) -> list:
    """List available Phoenix model files from the catalogue.
    
    Args:
        path: Optional local path where the catalogue file is stored. If None, downloads to a temporary location.
        base_url: Optional base URL to download the catalogue from. Defaults to the standard Phoenix STSCI model url.

    Returns:
        A list of filenames available in the Phoenix model catalogue.
    """
    path = pathlib.Path(path) if path else None
    base_url = base_url or BASE_URL
    catalog_path = get_catalogue(path=path, base_url=base_url)
    from astropy.io import fits
    data_files = []
    with fits.open(catalog_path) as hdul:
        data = hdul[1].data  # Assuming the data is in the first extension
        for d in data:
            properties = d[0]
            temperature, feh, logg = [float(p) for p in properties.split(",")]
            filename = d[1][:-5]
            if path:
                filename = str(path / filename)
            else:
                filename = urllib.parse.urljoin(base_url, filename)
            data_files.append(PhoenixDataFile(teff=int(temperature), logg=logg, feh=feh, alpha=0.0, filename=filename))
            
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





