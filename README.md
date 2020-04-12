# s1flood

Google Earth Engine (GEE) flood algorithm as described in DeVries et al., Remote Sensing of Environment (2020).

An account on the GEE is required to use `s1flood`. To sign up for an account, go to https://earthengine.google.com.

## 1. On the GEE Playground

Load the repository by including the following line in your script:

```javascript
var s1flood = require('users/bdv/s1flood');
```

Specific scripts (functions) can be accessed as follows:

```javascript
var zscore = require('users/bdv/s1flood:zscore');
var mapFloods = require('users/bdv/s1flood:mapFloods');
```

### Examples

Summary stats demo: https://code.earthengine.google.com/fe91cf1ab5df51fe107dd9b07f84835a  

Houston (Hurricane Harvey), 2017-08-30: https://code.earthengine.google.com/5ff925dd39ac4a1994719bb4f7681940  

Beira, Mozambique (Cyclone Idai), 2018-03-23: https://code.earthengine.google.com/444cf654636f01877875721c9c402c7c  

The Bahamas (Hurricane Dorian), 2019-09-04: https://code.earthengine.google.com/29e799edb05ab69e11dfa3bd14146e33  

Omaha, Nebraska, 2019-03-25: https://code.earthengine.google.com/5bdf08bae781e45564bc8c6b31d4067e  

Central Greece, 2018-03-01: https://code.earthengine.google.com/3ee7b5408c7a7aa1ee13988afa6236c9  

## 2. Python Package

To install the `s1flood` python package into a conda environment:

```bash
conda create -n ee python earthengine-api
conda activate ee
```

You will need to authrorize use of your GEE account the first time you load and inialize the `ee` module:

```bash
python -c "import ee; ee.Initialize()"
```

Follow the instructions after running this code.

Finally, install `s1flood` using pip.

```bash
pip install s1flood
```

### Using DSWE

In addition to using Sentinel-1 backscatter anomalies (Z-scores) to map floods, Landsat data are used to map historical inundation and permanent open water. Two options are avialable for the historical inundaiton and permanent open water mapping:  
1. Exclusive use of the JRC Global Surface Water (GSW) dataset. Two probability thresholds are applied: 90% for permanent open water and 25% for seasonal inundation.  
2. Combined use of the JRC-GSW and the Dynamic Surface Water Extent (DSWE). The two thresholds described in (1) are applied to both datasets to define permanent open water and seasonal inundation.  

Option (1) is used by default, and Option (2) is triggered by the `use_dswe` argument in the `mapFloods()` function. Use of this option requires installation of the `eedswe` package, available [here](https://github.com/bendv/eedswe). `mapFloods()` will default to Option (1) with a warning if `eedswe` is not installed and `use_dswe` is `True`.

### Examples

Some example notebooks are included in the "examples/" directory. To run these, you also need to install `geemap`, `matplotlib`, `pandas` and `jupyter`:

```bash
conda install geemap matplotlib pandas jupyter
jupyter notebook
```

## Reference

DeVries, B., Huang, C-Q., Armston, J. Huang, W., Jones, J.W. and Lang M.W. 2020. Rapid and robust monitoring of floods using Sentinel-1 and Landsat data on the Google Earth Engine. Remote Sensing of Environment, 24:111664,  [doi:10.1016/j.rse.2020.111664](10.https://doi.org/10.1016/j.rse.2020.111664).

