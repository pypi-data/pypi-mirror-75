
![chime-frb-constants](https://github.com/CHIMEFRB/frb-constants/workflows/chime-frb-constants/badge.svg) 
[![Coverage Status](https://coveralls.io/repos/github/CHIMEFRB/frb-constants/badge.svg?branch=master&t=2TpXqG)](https://coveralls.io/github/CHIMEFRB/frb-constants?branch=master)
![pypi-version](https://img.shields.io/pypi/v/chime-frb-constants)
![black-formatting](https://img.shields.io/badge/code%20style-black-000000.svg)
# CHIME/FRB Constants 
A pure-python, lightweight and zero dependency package to access constants used in the CHIME/FRB software projects.

## Installation
```
pip install chime-frb-constants
```

### Optional
If `scipy` is installed in the python environment, `frb-constants` will also expose the physical constants, otherwise it is set to `None`
```python
import chime_frb_constants as constants
constants.phy_const
```

## Usage
```python
import chime_frb_constants as constants

>>> constants.K_DM
4149.377593360996

>>> constants.phys_const.speed_of_light
299792458.0
```

## Changelog

### 2020.07
  - Updated `CHANNEL_BANDWIDTH_MHZ`
  - Fixed errors with `FREQ`
  - Added optional physical constants from `scipy`

### 2020.06.3
  - Fixed error with `CHANNEL_BANDWIDTH_MHZ`
  - Change to `SAMPLING_TIME_MS`
  - New constant `SAMPLING_TIME_S`

### 2020.06.2
  - Added constants `FREQ` and `FREQ_FREQ`

### 2020.06
  - Release on [PYPI](https://pypi.org/project/chime-frb-constants/)
  - All constants are now uppercase
  - All physical constants from `scipy` are not availaible anymore under constants.


