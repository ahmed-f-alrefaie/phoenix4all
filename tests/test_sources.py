import pandas as pd

import phoenix4all.sources.core as core


def test_core_construct_dataframe():
    datafiles = [
        core.PhoenixDataFile(teff=3500, logg=5.0, feh=0.0, alpha=0.0, filename="file1"),
        core.PhoenixDataFile(teff=4000, logg=4.5, feh=-1.0, alpha=0.2, filename="file2"),
        core.PhoenixDataFile(teff=4500, logg=4.0, feh=0.5, alpha=0.0, filename="file3"),
    ]
    df = core.construct_phoenix_dataframe(datafiles)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3
    assert "filename" in df.columns
    assert (3500, 5.0, 0.0, 0.0) in df.index
    assert (4000, 4.5, -1.0, 0.2) in df.index
    assert (4500, 4.0, 0.5, 0.0) in df.index


def test_core_find_nearest_points():
    import numpy as np

    teff = np.array([3500, 4000, 4500, 5000])
    logg = np.array([5.0, 4.5, 4.0, 3.5])
    feh = np.array([0.0, -1.0, 0.5])
    alpha = np.array([0.0, 1.0])
    # Create a grid of all combinations
    grid = np.array(np.meshgrid(teff, logg, feh, alpha)).T.reshape(-1, 4)
    data = {
        "teff": grid[:, 0],
        "logg": grid[:, 1],
        "feh": grid[:, 2],
        "alpha": grid[:, 3],
        "filename": [f"file_{i}" for i in range(grid.shape[0])],
    }

    df = pd.DataFrame(data).set_index(["teff", "logg", "feh", "alpha"])

    nearest = core.find_nearest_points(df, teff=4200, logg=4.3, feh=-0.5, alpha=0.1)
    assert isinstance(nearest, pd.DataFrame)
    assert nearest.shape[0] <= 16
    assert "filename" in nearest.columns
    assert (4000, 4.5, -1.0, 0.2) in nearest.index
    assert (4500, 4.0, 0.5, 0.0) in nearest.index
