from dataclasses import dataclass, asdict
from typing import Optional,Callable
import pandas as pd
import numpy as np
from astropy import units as u



@dataclass
class PhoenixDataFile:
    """Class representing a Phoenix model data file with its parameters."""
    teff: int
    logg: float
    feh: float
    filename: str
    alpha: float

@dataclass
class WeightedPhoenixDataFile(PhoenixDataFile):
    """Class representing a Phoenix model data file with its parameters and interpolation weight."""
    weight: float


DataFileLoader = Callable[[PhoenixDataFile], tuple[u.Quantity, u.Quantity]]

def construct_phoenix_dataframe(datafile_list: list[PhoenixDataFile]) -> pd.DataFrame:
    """Construct a DataFrame from a list of PhoenixDataFile instances."""

    serialised_data = [asdict(datafile) for datafile in datafile_list]
    df = pd.DataFrame(serialised_data)
    df.set_index(['teff', 'logg', 'feh', 'alpha'], inplace=True)
    return df

def find_nearest_points(df: pd.DataFrame, teff: int, logg: float, feh: float, alpha: float=0.0) -> pd.DataFrame:
    """Find the nearest grid points in the DataFrame to the specified parameters.
    
    Args:
        df: DataFrame with MultiIndex (teff, logg, feh, alpha) and a 'filename' column.
        teff: Effective temperature to match.
        logg: Surface gravity to match.
        feh: Metallicity to match.
        alpha: Alpha element enhancement to match (default is 0.0).
    Returns:
        DataFrame with the nearest grid points and their filenames.
    
    """
    # Since there will be multiple temperatures, we will progressively filter the DataFrame

    tvalues = df.index.get_level_values('teff').unique()
    tclosest = tvalues[np.abs(tvalues - teff).argsort()[:2]]  # Get two closest temperatures
    if np.any(tclosest == teff):
        tclosest = np.array([teff])  # If exact match, only keep that
    df_t = df.loc[df.index.get_level_values('teff').isin(tclosest)]
    # Now filter by logg
    gvalues = df_t.index.get_level_values('logg').unique()
    gclosest = gvalues[np.abs(gvalues - logg).argsort()[:2]]  # Get two closest logg values
    if np.any(gclosest == logg):
        gclosest = np.array([logg])  # If exact match, only keep that
    df_g = df_t.loc[df_t.index.get_level_values('logg').isin(gclosest)]
    # Now filter by feh
    fvalues = df_g.index.get_level_values('feh').unique()
    fclosest = fvalues[np.abs(fvalues - feh).argsort()[:2]]  # Get two closest feh values
    if np.any(fclosest == feh):
        fclosest = np.array([feh])  # If exact match, only keep that
    df_f = df_g.loc[df_g.index.get_level_values('feh').isin(fclosest)]
    # Finally filter by alpha
    avals = df_f.index.get_level_values('alpha').unique()
    aclosest = avals[np.abs(avals - alpha).argsort()[:2]]  # Get two closest alpha values
    if np.any(aclosest == alpha):
        aclosest = np.array([alpha])  # If exact match, only keep that
    df_a = df_f.loc[df_f.index.get_level_values('alpha').isin(aclosest)]
    return df_a


def compute_weights(nearest_df: pd.DataFrame, teff: int, logg: float, feh: float, alpha: float=0.0,
                ) -> list[WeightedPhoenixDataFile]:
    """Compute interpolation weights for the nearest grid points and attach to the DataFrame.
    
    Args:
        nearest_df: DataFrame with the nearest grid points and their filenames.
        teff: Effective temperature to match.
        logg: Surface gravity to match.
        feh: Metallicity to match.
        alpha: Alpha element enhancement to match (default is 0.0).
    Returns:
        Dataframe with an additional 'weight' column for interpolation.
    """
    # Extract the unique values for each parameter
    teff_vals = sorted(nearest_df.index.get_level_values('teff').unique())
    logg_vals = sorted(nearest_df.index.get_level_values('logg').unique())
    feh_vals = sorted(nearest_df.index.get_level_values('feh').unique())
    alpha_vals = sorted(nearest_df.index.get_level_values('alpha').unique())

    target_point = [teff, logg, feh, alpha]

    t = []
    for param_val, param_values in zip(target_point, [teff_vals, logg_vals, feh_vals, alpha_vals]):
        if len(param_values) == 1:
            t.append(0.0)
        else:
            lower, upper = min(param_values), max(param_values)
            t_val = (param_val - lower) / (upper - lower)
            t.append(t_val)
    t_teff, t_logg, t_feh, t_alpha = t

    weights = {}
    for idx, row in nearest_df.iterrows():
        teff_i, logg_i, feh_i, alpha_i = idx
        i = teff_vals.index(teff_i)
        j = logg_vals.index(logg_i)
        k = feh_vals.index(feh_i)
        l = alpha_vals.index(alpha_i)

        weight = (
            (1 - t_teff) if i == 0 else t_teff if len(teff_vals) > 1 else 1 
        ) * (
            (1 - t_logg) if j == 0 else t_logg if len(logg_vals) > 1 else 1 
        ) * (
            (1 - t_feh) if k == 0 else t_feh if len(feh_vals) > 1 else 1 
        ) * (
            (1 - t_alpha) if l == 0 else t_alpha if len(alpha_vals) > 1 else 1 
        )
        weights[idx] = weight

    nearest_df = nearest_df.copy()
    weighted_datafile = []
    nearest_df['weight'] = pd.Series(weights)
    for idx, row in nearest_df.iterrows():
        if row["weight"] > 0:
            weighted_datafile.append(WeightedPhoenixDataFile(
                teff=idx[0], logg=idx[1], feh=idx[2], alpha=idx[3],
                filename=row['filename'], weight=row['weight']
            ))
    return weighted_datafile

def find_nearest_datafile(df: pd.DataFrame, teff: int, logg: float, feh: float, alpha: float=0.0) -> PhoenixDataFile:
    """Find the single nearest data file in the DataFrame to the specified parameters.
    
    Args:
        df: DataFrame with MultiIndex (teff, logg, feh, alpha) and a 'filename' column.
        teff: Effective temperature to match.
        logg: Surface gravity to match.
        feh: Metallicity to match.
        alpha: Alpha element enhancement to match (default is 0.0).
    Returns:
        PhoenixDataFile instance with the nearest grid point and its filename.
    """
    # Compute the distance to each point in the DataFrame
    distances = np.sqrt(
        (df["teff"] - teff) ** 2 +
        (df["logg"] - logg) ** 2 +
        (df["feh"] - feh) ** 2 +
        (df["alpha"] - alpha) ** 2
    )
    min_idx = distances.idxmin()
    row = df.loc[min_idx]
    return PhoenixDataFile(
        teff=min_idx[0], logg=min_idx[1], feh=min_idx[2], alpha=min_idx[3],
        filename=row['filename']
    )

def compute_weighted_flux(
        weighted_data: list[WeightedPhoenixDataFile],
        file_loader: DataFileLoader,
        *,
        wavelength_grid: Optional[u.Quantity] = None
) -> tuple[u.Quantity, u.Quantity]:
    """Compute the weighted flux from a list of WeightedPhoenixDataFile instances.
    
    Args:
        weighted_data: List of WeightedPhoenixDataFile instances with weights and filenames.
    Returns:
        A tuple of (wavelengths, weighted_flux) as astropy Quantities.
    """
    fluxes=[]
    wls = []

    for data in weighted_data:
        wl, flux = file_loader(data)

        wls.append(wl)
        fluxes.append(flux*data.weight)
    
    perform_interpolation = wavelength_grid is not None
    # Check that all wavelength arrays are the same
    if not perform_interpolation:
        for wl in wls[1:]:

            if not np.array_equal(wl, wls[0]):
                smallest_wl = np.argmin([len(w) for w in wls])
                wavelength_grid = wls[smallest_wl]
                perform_interpolation = True
                break
    if perform_interpolation:
        # Interpolate all fluxes to the common wavelength grid
        new_fluxes = []

        for wl, flux in zip(wls, fluxes):
            interp_flux = np.interp(wavelength_grid.value, wl.value, flux.value, left=0.0, right=0.0) << flux.unit
            new_fluxes.append(interp_flux)
        total_flux = sum(new_fluxes)
        return wavelength_grid, total_flux
    else:
        total_flux = sum(fluxes)
        return wls[0], total_flux
    