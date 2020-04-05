/*
Functions to compute baseline statistics from S1 time series

calc_basemean()
calc_basesd()
calc_anomaly()
calc_zscore()

Usage:

```
var zscore = require('users/bdv/zscore');
```
*/

var filterOrbit = function(x, direction) {
  return x.filter(
    ee.Filter.equals('orbitProperties_pass', direction)
    );
};

var filterMode = function(x, mode) {
  return x.filter(
    ee.Filter.equals('instrumentMode', mode)
    );
};

// baseline (mean)
var calc_basemean = function(x, start, end, mode, direction) {
  return x
    .filter(ee.Filter.equals('orbitProperties_pass', direction))
    .filter(ee.Filter.equals('instrumentMode', mode))
    .filterDate(start, end)
    .mean();
};

// baseline (sd)
var calc_basesd = function(x, start, end, mode, direction) {
  return x
    .filter(ee.Filter.equals('orbitProperties_pass', direction))
    .filter(ee.Filter.equals('instrumentMode', mode))
    .filterDate(start, end)
    .reduce(ee.Reducer.stdDev())
    .rename(['VV', 'VH', 'angle']);
};

// anomaly
var calc_anomaly = function(x, start, end, mode, direction) {
  var basemean = calc_basemean(x, start, end, mode, direction);
  
  return x
    .filter(ee.Filter.equals('orbitProperties_pass', direction))
    .filter(ee.Filter.equals('instrumentMode', mode))
    .map(function(y) {
    return y
      .subtract(basemean)
      .set({'system:time_start': y.get('system:time_start')});
    });
};

// Z-score
var calc_zscore = function(x, start, end, mode, direction) {
  var anom = calc_anomaly(x, start, end, mode, direction);
  var basesd = calc_basesd(x, start, end, mode, direction);
  return anom.map(function(x) {
    return x
      .divide(basesd)
      .set({'system:time_start': x.get('system:time_start')});
    });
};

exports.calc_basemean = calc_basemean;
exports.calc_basesd = calc_basesd;
exports.calc_anomaly = calc_anomaly;
exports.calc_zscore = calc_zscore;

