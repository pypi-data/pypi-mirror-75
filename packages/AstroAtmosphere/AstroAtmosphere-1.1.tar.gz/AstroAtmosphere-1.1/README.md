# AstroAtmosphere

**Note:**
It would be appreciated if a reference to the following work, for which this package was originally build, is included whenever this code is used for a publication: 
*Quantification of the expected residual dispersion of the MICADO Near-IR imaging instrument*, van den Born & Jellema, 2020, MNRAS, DOI: [10.1093/mnras/staa1870](https://doi.org/10.1093/mnras/staa1870).


**Author info**: *Joost van den Born*, *born@astron.nl*


## Example

A minimal working example to calculate the atmospheric dispersion at Cerro Armazones between 1.49 and 1.78 micron.

```python
from AstroAtmosphere import *

# Parameters at Cerro Armazones
T   = 279.65    # k
P   = 71200     # Pa
H   = 0.22
xc  = 450       # ppm
lat = -24.5983  # degrees
h   = 3064      # m
l1  = 1.49      # micron
l2  = 1.78      # micron
z0  = 30

# Initializing dispersion model
at  = Observatory()

# Calculating indices of refraction for l1 and l2
n1  = at.n_tph(l=l1, T=T, p=P, RH=H, xc=xc)
n2  = at.n_tph(l=l2, T=T, p=P, RH=H, xc=xc)

# Density of the atmosphere (following CIPM-81/91 equations)
rho = at.rho(p=P, T=T, RH=H, xc=xc)

# Initializing refraction model and setting the reduced height
disp = dispersion(lat, h)
disp.setReducedHeight(P, rho)

# Calculation of the atmopheric dipsersion
atm_dispersion = disp.cassini(n1, z0) * 3.6e6
print ('The dispersion is %.03f milli arc seconds' %(atm_dispersion))
```

## Installation

The package is available through Git-Lab and through PyPI. The package may be installed using the `setup.py` file, but easier is to install using `pip`.

```bash
pip install AstroAtmosphere
```


## Contents of the AstroAtmosphere package

The package contains the following files:
- `/data/1976USSA.txt` 			: Data file of the 1976 US Standard Atmosphere.
- `ciddorModel.py` 				: Contains the `Observatory()` class to calculate the refractive index of atmospheric air, using the Ciddor (1996) model.
- `dispersionModels.py` 		: Contains various atmospheric models that can be used to calculate the atmospheric dispersion
- `examples.py` 				: Contains several quick functions, e.g. to quickly calculate the refractive index.
- `refractionModels.py`		 		: Contains various atmospheric models that can be used to calculate the atmospheric refraction
- `refractivityModels.py` 		: Contains various functions from literature to calculate the refractive index. Some examples of works included are Ciddor (1996), Barrell & Sears (1939), SLALIB, Owens (1967) and Edlen (1966).


## The Ciddor refractivity model

The refractivity model from Ciddor, 1996, calculates the index of refraction of air using the following parameters:
- T - Temperature in Kelvin
- p - Pressure in Pascal
- RH - Relative humidity in fractional units
- xc - CO2 density in parts per million

It is invoked by first initializing an `Observatory()` object. The atmospheric conditions can be parsed into the `n_tph()` function.

```python
at  = Observatory()
n   = at.n_tph(l=0.55, T=273.15, p=101325, RH=0.2, xc=300)
```

Basic functionality of other refractivity models is included as well and is discussed below.


## The atmospheric refraction and atmospheric dispersion models

If the atmospheric refraction is denoted as R(n), then atmospheric dispersion is defined as R(n1) - R(n2). Thus they are very similar in function and also in use.


The available models in this package:
- `refractionIntegral()` - Full integration using the refractive integral (requires detailed information about the atmosphere, e.g. `AstroAtmosphere/data/1976USSA.txt`)
- `planeParallel()` - Plane-parallel atmosphere refraction model
- `cassini()` - Cassini's homogeneous atmosphere refraction model
- `oriani()` - Oriani's theorem ( Atan(z) + Btan^3(z) )
- `tan5()` - Oriani's theorem expanded ( Atan(z) + Btan^3(z) + Ctan^5(z)  )
- `corbard()` - Error function refraction model
- `matharExponential()` - Barometric exponential model by R. Mathar.


Input parameters for the spherical atmosphere models (all but the first):
- T - Temperature               [K]
- p - Pressure                  [Pa]
- RH - Relative humidity
- xc - CO2 density              [ppm]
- lat - Latitude                [deg]
- h - Height above sea level    [m]
- l - Wavelength(s)             [um]
- z - Zenith angle              [deg]

An example - To calculate the atmospheric refraction we set up a `refraction()` object. This requires the latitude and altitude of the observer. The atmospheric dispersion is calculated similarly, but by exchanging the `refraction()` object by a `dispersion()` object and parsing two refractive indices into the `cassini()` function.

```python
# Density of the atmosphere (following CIPM-81/91 equations)
rho = at.rho(p=101325, T=273.15, RH=0.2, xc=300)

# Initializing refraction model and setting the reduced height
ref = refraction(lat=30, h=2200)
ref.setReducedHeight(p=101325, rho)

# Calculating the atmospheric refraction
atm_ref = ref.cassini(n, zenith=30)
```


## Analytical error propagation

Full analytical error propagation is available for the Ciddor dispersion model (`Observatory.dn_tph()`), for the Cassini refraction model (`refraction.cassiniError()`) and for the Cassini dispersion model (`dispersion.cassiniError()`).
The results agree well with a Monte Carlo simulation, suggesting that if additional errors have not been considered, they are of neglible importance.

Uncertainties that are considered:

Ciddor dispersion model:

| Param. | Description | Unit |
| ------ | ------ | ------ |
| dl | Wavelength | um |
| dT | Temperature | K |
| dP | Pressure | Pa |
| dRH | Relative Humidity |  |
| dCO2 | CO2 density | ppm |
 

Cassini refraction model:

| Param. | Description | Unit |
| ------ | ------ | ------ |
| dn | Refractive index |  |
| dz | Zenith angle | deg |

Cassini dispersion model:


| Param. | Description | Unit |
| ------ | ------ | ------ |
| dl1, dl2 | Wavelength(s) | um |
| dT | Temperature | K |
| dP | Pressure | Pa |
| dRH | Relative Humidity |  |
| dCO2 | CO2 density | ppm |
| dz | Zenith angle | deg |
 
An example of its use is given in the code snippet here:
```python
 # Initializing dispersion object
disp = dispersion(lat, h)
disp.setReducedHeight(P, rho)

# Atmospheric dispersion
dispersion_obs = disp.cassini(n1, n2, zenith_obs)

# Uncertainty in the atmospheric dispersion
dispersion_unc = disp.cassiniError(zenith_obs, l1, l2, T, P, H, xc, 
    dl1=0.001, dl2=0.001, dT=0.2, dP=30, dRH=0.03, dCO2=25, dz=1/3600) * 3.6e6
```

## Other refractivity models

The package also includes limited functionality of other refractivity models. These are not as extensive, work only under standard atmospheric conditions, or over a limited wavelength range, compared to the Ciddor model.

Included are

| Model name | Function | Remarks |
| ---------- | -------- | ------- |
| Barrell & Sears (1939) | `BarrellAndSears()` | Outdated model, especially poor for short wavelengths. |
| Ciddor (1996) | `Ciddor()` | Only at standard atmosphere. CO2 density can be changed. |
| Edlen (1953) | `Edlen1953()` | Only at standard atmosphere. Function requires wavelength only. |
| Edlen (1966) | `Edlen1966()` | Only at standard atmosphere. Function requires wavelength only. |
| Owens (1967) | `Owens()` | - |
| Bonsch & Potulski (1998) | `BonschPotulski()` | Function does not include humidity |
| Birch & Downs (1994) | `BirchDowns()` | Only at standard atmosphere. Function requires wavelength only. |
| Peck & Reeder (1972) | `PeckReeder()` | Only at standard atmosphere. Function requires wavelength only. |
| Hohenkerk & Sinclair (1985) | `slalib()` | Only at standard atmosphere. Function requires wavelength only. |

The last function extracts the refractive index from the `pyslalib.sla_refro()` function and thus requires [pyslalib](https://pypi.org/project/pySLALIB/). This is an optional dependency for the setup of AstroAtmosphere.

## Quick functions

Some functions that assume default conditions for the atmosphere. Then only the wavelength and zenith angle are required to calculate the refraction and dispersion. 

Presently, only the `'STANDARD'` and `'CERRO_ARMAZONES'` flags are known. Contact the author to add additional standard conditions.

```python
 # Quick refractive index
nq = quick_refractive_index(l=1.49, conditions='STANDARD')

# Quick refraction
rq = quick_refraction(l1, zenith_obs, conditions='STANDARD')

# Quick dispersion
dq = quick_dispersion(l1, l2, zenith_obs, conditions='STANDARD')
```
