# s1flood
GEE flood algorithm as described in DeVries et al., Remote Sensing of Environment (2020)

Load the repository by including the following line in your script:

```javascript
var s1flood = require('users/bdv/s1flood');
```

Specific scripts (functions) can be accessed as follows:

```javascript
var zscore = require('users/bdv/s1flood:zscore');
var mapFloods = require('users/bdv/s1flood:mapFloods');
```

## Examples

Summary stats demo: https://code.earthengine.google.com/fe91cf1ab5df51fe107dd9b07f84835a  

Houston (Hurricane Harvey), 2017-08-30: https://code.earthengine.google.com/5ff925dd39ac4a1994719bb4f7681940  

Beira, Mozambique (Cyclone Idai), 2018-03-23: https://code.earthengine.google.com/444cf654636f01877875721c9c402c7c  

The Bahamas (Hurricane Dorian), 2019-09-04: https://code.earthengine.google.com/29e799edb05ab69e11dfa3bd14146e33  

Omaha, Nebraska, 2019-03-25: https://code.earthengine.google.com/5bdf08bae781e45564bc8c6b31d4067e  

Central Greece, 2018-03-01: https://code.earthengine.google.com/3ee7b5408c7a7aa1ee13988afa6236c9  

## Reference

DeVries, B., Huang, C-Q., Armston, J. Huang, W., Jones, J.W. and Lang M.W. 2020. Rapid and robust monitoring of floods using Sentinel-1 and Landsat data on the Google Earth Engine. Remote Sensing of Environment, 24:111664,  [doi:10.1016/j.rse.2020.111664](10.https://doi.org/10.1016/j.rse.2020.111664).

