import pytest

from phoenix4all.sources.core import PhoenixDataFile
from phoenix4all.sources.hiresfits import parse_filename

# lte12000-2.00-0.5.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06300-1.50-1.5.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte03100-2.00-3.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte04200-5.50-1.0.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06000-5.00-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06800-1.50-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06100-2.00-1.5.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte02900-1.50-0.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte04900-1.00-2.0.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte02700-0.50-4.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06100-0.50+1.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte07800-5.00-0.5.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte04400-2.50-0.5.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte04700-3.50-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte04900+0.50-3.0.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte02800-2.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06300-5.00-0.0.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte05600-0.00-1.0.Alpha=+1.00.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte05000-5.50-0.0.Alpha=+0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte03700-6.00-0.5.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte08200-2.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte05800-3.50-3.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte02300-1.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06000-4.50-1.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte08400-2.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06400-5.00-1.5.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte09200-2.50-2.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte03500-0.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte04900-2.50-3.0.Alpha=+0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits
# lte06200-1.50-2.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits


@pytest.mark.parametrize(
    "filename, expected",
    [
        (
            "hello/lte12000-2.00-0.5.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=12000,
                logg=2.0,
                feh=-0.5,
                alpha=0.6,
                filename="hello/lte12000-2.00-0.5.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06300-1.50-1.5.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6300,
                logg=1.5,
                feh=-1.5,
                alpha=0.0,
                filename="lte06300-1.50-1.5.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte03100-2.00-3.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=3100,
                logg=2.0,
                feh=-3.0,
                alpha=0.6,
                filename="lte03100-2.00-3.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte04200-5.50-1.0.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=4200,
                logg=5.5,
                feh=-1.0,
                alpha=-0.2,
                filename="lte04200-5.50-1.0.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06000-5.00-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6000,
                logg=5.0,
                feh=-1.5,
                alpha=-0.4,
                filename="lte06000-5.00-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06800-1.50-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6800,
                logg=1.5,
                feh=-1.5,
                alpha=-0.4,
                filename="lte06800-1.50-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06100-2.00-1.5.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6100,
                logg=2.0,
                feh=-1.5,
                alpha=1.2,
                filename="lte06100-2.00-1.5.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte02900-1.50-0.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=2900,
                logg=1.5,
                feh=-0.5,
                alpha=-0.4,
                filename="lte02900-1.50-0.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte04900-1.00-2.0.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=4900,
                logg=1.0,
                feh=-2.0,
                alpha=1.2,
                filename="lte04900-1.00-2.0.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte02700-0.50-4.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=2700,
                logg=0.5,
                feh=-4.0,
                alpha=0.0,
                filename="lte02700-0.50-4.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06100-0.50+1.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6100,
                logg=0.5,
                feh=1.0,
                alpha=0.0,
                filename="lte06100-0.50+1.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte07800-5.00-0.5.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=7800,
                logg=5.0,
                feh=-0.5,
                alpha=1.2,
                filename="lte07800-5.00-0.5.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte04400-2.50-0.5.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=4400,
                logg=2.5,
                feh=-0.5,
                alpha=-0.2,
                filename="lte04400-2.50-0.5.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte04700-3.50-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=4700,
                logg=3.5,
                feh=-1.5,
                alpha=-0.4,
                filename="lte04700-3.50-1.5.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte04900+0.50-3.0.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=4900,
                logg=-0.5,
                feh=-3.0,
                alpha=1.2,
                filename="lte04900+0.50-3.0.Alpha=+1.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte02800-2.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=2800,
                logg=2.0,
                feh=1.0,
                alpha=0.6,
                filename="lte02800-2.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06300-5.00-0.0.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6300,
                logg=5.0,
                feh=0.0,
                alpha=-0.2,
                filename="lte06300-5.00-0.0.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte05600-0.00-1.0.Alpha=+1.00.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=5600,
                logg=0.0,
                feh=-1.0,
                alpha=1.0,
                filename="lte05600-0.00-1.0.Alpha=+1.00.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte05000-5.50-0.0.Alpha=+0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=5000,
                logg=5.5,
                feh=0.0,
                alpha=0.4,
                filename="lte05000-5.50-0.0.Alpha=+0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte03700-6.00-0.5.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=3700,
                logg=6.0,
                feh=-0.5,
                alpha=-0.2,
                filename="lte03700-6.00-0.5.Alpha=-0.20.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte08200-2.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=8200,
                logg=2.5,
                feh=0.0,
                alpha=0.0,
                filename="lte08200-2.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte05800-3.50-3.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=5800,
                logg=3.5,
                feh=-3.0,
                alpha=0.6,
                filename="lte05800-3.50-3.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte02300-1.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=2300,
                logg=1.0,
                feh=1.0,
                alpha=0.6,
                filename="lte02300-1.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06000-4.50-1.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6000,
                logg=4.5,
                feh=-1.0,
                alpha=-0.4,
                filename="lte06000-4.50-1.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte08400-2.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=8400,
                logg=2.5,
                feh=0.0,
                alpha=0.0,
                filename="lte08400-2.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06400-5.00-1.5.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6400,
                logg=5.0,
                feh=-1.5,
                alpha=0.0,
                filename="lte06400-5.00-1.5.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte09200-2.50-2.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=9200,
                logg=2.5,
                feh=-2.0,
                alpha=-0.4,
                filename="lte09200-2.50-2.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte03500-0.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=3500,
                logg=0.0,
                feh=1.0,
                alpha=0.6,
                filename="lte03500-0.00+1.0.Alpha=+0.60.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte04900-2.50-3.0.Alpha=+0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=4900,
                logg=2.5,
                feh=-3.0,
                alpha=0.4,
                filename="lte04900-2.50-3.0.Alpha=+0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
        (
            "lte06200-1.50-2.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            PhoenixDataFile(
                teff=6200,
                logg=1.5,
                feh=-2.0,
                alpha=-0.4,
                filename="lte06200-1.50-2.0.Alpha=-0.40.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits",
            ),
        ),
    ],
)
def test_parse_filename(filename, expected):
    result = parse_filename(filename)
    assert result == expected
