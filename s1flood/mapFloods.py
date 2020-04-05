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

