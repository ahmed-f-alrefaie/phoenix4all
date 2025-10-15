from astropy import units as u

from phoenix4all import radiative


def test_planck():
    wave = 5000  # Angstrom
    temp = 5800  # Kelvin
    intensity = radiative.planck(wave << u.AA, temp << u.K)
    assert intensity > 0
    assert isinstance(intensity, u.Quantity)
