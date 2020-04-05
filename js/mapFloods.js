/*
S1Flood Mapping algorithm
=========================

DeVries et al., 2020, Remote Sensing of Environment

usage:
  var mapFloods = require('users/bdv/s1flood:mapFlood);
*/


var dswe = require('users/bdv/s1flood:dswe');
var zscore = require('users/bdv/s1flood:zscore');


var mapFloods = function(
  z, // ee.Image of z-score with bands "VV" and "VH"
  zvv_thd, // VV Z-score threshold
  zvh_thd, // VH Z-score threshold
  pow_thd, // Open water threshold (%)
  pin_thd, // Inundation threshold (%)
  use_dswe,  // Use DSWE? (slower)
  dswe_start, // Start date for DSWE (Landsat) data
  dswe_end,  // End date for DSWE
  doy_start, // Day of year (start) filter for DSWE/JRC background
  doy_end) // Day of year (end) filter for DSWE/JRC background

  {
  
  // defaults
  if(!pow_thd) {
    pow_thd = 90;
  }
  if(!pin_thd) {
    pin_thd = 25;
  }
  if(!dswe_start) {
    dswe_start = '2000-01-01';
  }
  if(!dswe_end) {
    dswe_end = '2016-01-01';
  }
  if(!doy_start) {
    doy_start = 1;
  }
  if(!doy_end) {
    doy_end = 366;
  }
  
  // JRC water mask
  var jrc = ee.ImageCollection("JRC/GSW1_1/MonthlyHistory");
  var jrcvalid = jrc.map(function(x) {return x.gt(0)}).sum();
  var jrcwat = jrc.map(function(x) {return x.eq(2)}).sum().divide(jrcvalid).multiply(100);
  var jrcmask = jrcvalid.gt(0);
  var ow = jrcwat.gte(ee.Image(pow_thd));

  // Seasonal inundation mask: Compute DSWE, if applicable
  var inun = ee.Image(0);
  if(use_dswe) {
    var dswe_filters = [
      ee.Filter.date(dswe_start, dswe_end),
      ee.Filter.dayOfYear(doy_start, doy_end)
      ];
    var pdswe = dswe.cdswe(dswe_filters);
    var pinun = pdswe.select("pDSWE1").add(pdswe.select("pDSWE2")).add(pdswe.select("pDSWE3"));
    ow = ow.where(pdswe.select("pDSWE1").gte(ee.Image(pow_thd)), 1);
    inun = pinun.gte(ee.Image(pin_thd));
  } else {
    inun = jrcwat.gte(ee.Image(pin_thd));
  }
  
  
  // Classify floods
  var vvflag = z.select('VV').lte(ee.Image(zvv_thd));
  var vhflag = z.select('VH').lte(ee.Image(zvh_thd));

  var flood_class = ee.Image(0)
    .add(vvflag) 
    .add(vhflag.multiply(2))
    .add(inun.multiply(10))
    .where(ow.eq(1), 20)
    .rename('flood_class')
    .updateMask(jrcmask)
    //.copyProperties(z)
    .set('system:time_start', z.get('system:time_start'));

  return flood_class;
};


var palette = [
    '#000000', // 0 - non-water; non-flood
    '#FC9272', // 1 - VV only
    '#FC9272', // 2 - VH only
    '#FF0000', // 3 - VV + VH
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#DEEBF7', // 10 - prior inundation; no flag
    '#8C6BB1', // 11 - prior inundation; VV only
    '#8C6BB1', // 12 - prior inundation; VH only
    '#810F7C', // 13 - prior inundation; VV + VH
    '#000000', 
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#000000',
    '#08306B' // 20 - permanent open water
  ];



exports.mapFloods = mapFloods;
exports.palette = palette;

