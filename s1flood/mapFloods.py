import ee
from .zscore import *
import warnings

try:
    from eedswe import cdswe
    has_eedswe = True
except ImportError:
    has_eedswe = False


def mapFloods(
    z, 
    zvv_thd, 
    zvh_thd, 
    pow_thd = 90, 
    pin_thd = 25, 
    use_dswe = False, 
    dswe_start = "2000-01-01", 
    dswe_end = "2018-01-01", 
    doy_start = 1, 
    doy_end = 366
    ):
    '''
    Generates a flood map from a Sentinel-1 image using the Z-score flood mapping algorithm described in DeVries et al. (2020), RSE.

    Args:
    =====

    z:              ee.Image object from the 'COPERNICUS/S1_GRD' ImageCollection
    zvv_thd:        VV Z-score threshold (Z_VV < zvv_thd indicates floods)
    zvh_thd:        VH Z-score threshold (Z_VH < zvh_thd indicates floods)
    pow_thd:        Open water probability threshold (in %) applied to JRC Global Surface Water ImageCollection (as well as DSWE, if eedswe is installed). Values abovfe this threshold are interpreted as permanent open water (90)
    pin_thd:        Inundation probability threshold (in %) applied to historical DSWE class probabilities, or the JRC Global Surface Water dataset if eedswe is not available. Values above this threshold are interpreted as historical seasonal inundation. (25)
    use_dswe:       Use historical DSWE data? The `eedswe` package must be installed.
    dswe_start:     Start date (YYYY-MM-DD) for DSWE class probabilities.
    dswe_end:       End date (YYYY-MM-DD) for DSWE class probabilities.
    doy_start:      Day-of-year start for DSWE class probabilities.
    doy_end:        Day-of-year end for DSWE class probabilities.

    Returns:
    ========
    An ee.Image object with values corresponding to flood classes:
        0 - non-water; non-flood
        1 - VV flood flag only
        2 - VH flood flag only
        3 - VV and VH flood flag
        10 - prior seasonal inundation; no flag
        11 - prior seasonal inundation; VV flood flag only
        12 - prior seasonal inundation; VH flood flag only
        13 - prior seasonal inundation; VV and VH flood flag
        20 - permanent open water
    '''

    if use_dswe and not has_eedswe:
        warnings.warn("`eedswe` package is not installed. Using JRC Global Surface Water for historical inundation instead.")
        use_dswe = False

    # permanent open water (POW) mask
    jrc = ee.ImageCollection("JRC/GSW1_1/MonthlyHistory")
    def _getvalid(x):
        return x.gt(0)
    jrcvalid = jrc.map(_getvalid).sum()
    def _getwat(x):
        return x.eq(2)
    jrcwat = jrc.map(_getwat).sum().divide(jrcvalid).multiply(100)
    jrcmask = jrcvalid.gt(0)
    ow = jrcwat.gte(pow_thd)

    # inundation frequency
    if use_dswe:
        dswe_filters = [
            ee.Filter.date(dswe_start, dswe_end),
            ee.Filter.dayOfYear(doy_start, doy_end)
            ]
        pdswe = dswe.cdswe(dswe_filters)
        pinun = pdswe.select("pDSWE1").add(pdswe.select("pDSWE2")).add(pdswe.select("pDSWE3"))
        ow = ow.where(pdswe.select("pDSWE1").gte(ee.Image(pow_thd)), 1)
        inun = pinun.gte(pin_thd)
    else:
        inun = jrcwat.gte(pin_thd)

    # classify floods
    vvflag = z.select('VV').lte(zvv_thd)
    vhflag = z.select('VH').lte(zvh_thd)

    flood_class = ee.Image(0) \
        .add(vvflag) \
        .add(vhflag.multiply(2)) \
        .add(inun.multiply(10)) \
        .where(ow.eq(1), 20) \
        .rename('flood_class') \
        .updateMask(jrcmask) \
        .set('system:time_start', z.get('system:time_start'))

    return flood_class



floodPalette = [
    '#000000', # 0 - non-water; non-flood
    '#FC9272', # 1 - VV only
    '#FC9272', # 2 - VH only
    '#FF0000', # 3 - VV + VH
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#DEEBF7', # 10 - prior inundation; no flag
    '#8C6BB1', # 11 - prior inundation; VV only
    '#8C6BB1', # 12 - prior inundation; VH only
    '#810F7C', # 13 - prior inundation; VV + VH
    '#000000', 
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#08306B' # 20 - permanent open water
  ]



