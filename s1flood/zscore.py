'''
Functions to compute baseline statistics from S1 time series
'''

import ee

def filterOrbit(x, direction):
    return x.filter(ee.Filter.equals('orbitProperties_pass', direction))

def filterMode(x, mode):
    return x.filter(ee.Filter.equals('instrumentMode', mode))

def calc_basemean(x, start, end, mode = "IW", direction = "DESCENDING"):
    '''
    Computes the mean backscatter for a baseline period, given an acquisition mode and orbital direction

    Args:
    =====
    x:          A Sentinel-1 ee.ImageCollection
    start:      Start date of baseline period ("YYYY-MM-DD")
    end:        End date of baseline period ("YYYY-MM-DD")
    mode:       Acquisition mode. Can be one of "IW" (default) or "SM"
    direction:  Orbital direction. Can be either "DESCENDING" (default) or "ASCENDING"

    Returns:
    ========
    An ee.Image object that represents the mean backscatter for the given baseline period.
    '''
    return x \
        .filter(ee.Filter.equals('orbitProperties_pass', direction)) \
        .filter(ee.Filter.equals('instrumentMode', mode)) \
        .filterDate(start, end) \
        .mean()

def calc_basesd(x, start, end, mode = "IW", direction = "DESCENDING"):
    '''
    Computes the standard deviation backscatter for a baseline period, given an acquisition mode and orbital direction

    Args:
    =====
    x:          A Sentinel-1 ee.ImageCollection
    start:      Start date of baseline period ("YYYY-MM-DD")
    end:        End date of baseline period ("YYYY-MM-DD")
    mode:       Acquisition mode. Can be one of "IW" (default) or "SM"
    direction:  Orbital direction. Can be either "DESCENDING" (default) or "ASCENDING"

    Returns:
    ========
    An ee.Image object that represents the standard deviation backscatter for the given baseline period.
    '''
    return x \
        .filter(ee.Filter.equals('orbitProperties_pass', direction)) \
        .filter(ee.Filter.equals('instrumentMode', mode)) \
        .filterDate(start, end) \
        .reduce(ee.Reducer.stdDev()) \
        .rename(['VV', 'VH', 'angle'])

def calc_anomaly(x, start, end, mode = "IW", direction = "DESCENDING"):
    '''
    Computes the backscatter anomaly for each image in a collection, given a baseline period, acquisition mode and orbital direction

    Args:
    =====
    x:          A Sentinel-1 ee.ImageCollection
    start:      Start date of baseline period ("YYYY-MM-DD")
    end:        End date of baseline period ("YYYY-MM-DD")
    mode:       Acquisition mode. Can be one of "IW" (default) or "SM"
    direction:  Orbital direction. Can be either "DESCENDING" (default) or "ASCENDING"

    Returns:
    ========
    An ee.ImageCollection object that represents the backscatter anomaly for each image in the input ImageCollection
    '''
    basemean = calc_basemean(x, start, end, mode, direction)
    def _calcanom(y):
        return y \
            .subtract(basemean) \
            .set({'system:time_start': y.get('system:time_start')})
    return x \
        .filter(ee.Filter.equals('orbitProperties_pass', direction)) \
        .filter(ee.Filter.equals('instrumentMode', mode)) \
        .map(_calcanom)

def calc_zscore(x, start, end, mode = "IW", direction = "DESCENDING"):
    '''
    Computes the pixelwise backscatter Z-scores for each image in a collection, given a baseline period, acquisition mode and orbital direction

    Args:
    =====
    x:          A Sentinel-1 ee.ImageCollection
    start:      Start date of baseline period ("YYYY-MM-DD")
    end:        End date of baseline period ("YYYY-MM-DD")
    mode:       Acquisition mode. Can be one of "IW" (default) or "SM"
    direction:  Orbital direction. Can be either "DESCENDING" (default) or "ASCENDING"

    Returns:
    ========
    An ee.ImageCollection object that represents the pixelwise backscatter Z-scores for each image in the input ImageCollection
    '''
    anom = calc_anomaly(x, start, end, mode, direction)
    basesd = calc_basesd(x, start, end, mode, direction)
    def _calcz(y):
        return y \
            .divide(basesd) \
            .set({'system:time_start': y.get('system:time_start')})
    return anom.map(_calcz)

