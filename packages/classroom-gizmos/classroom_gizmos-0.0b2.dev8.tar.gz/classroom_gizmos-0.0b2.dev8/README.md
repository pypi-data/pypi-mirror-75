# Classroom Gizmos
This is a collection of functions for classroom instruction in
introductory physics. This is basically using ipython as a calculator
that displays the calculation and the results.<br>
Typical usage to make a set of useful functions available in ipython:

    from classroom_gizmos.handies import *

<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
## handies
*_classroom_gizmos.handies_* is a collection of small functions
that are
useful from an ipython prompt. <br>
__Note: Imports from astropy, PyQt5, and func_timeout__<br>
Certain functions and functionality are not available when some of the
imported packages are unavailable.<br>
The **mine()** function lists all the user functions defined
in *_handies.py_*.

### handies defines:
    cdbn(), osname(),
    hostname(), call(), rad(), deg(), sinD(), cosD(), tanD(),
    asinD(), acosD(), atanD(), atan2D(), atan2P(), nCr(), comb(),
    pltsize(), select_file(), select_file_timeout(), getTS(), timeStampStr(),
    isInstalled(),
    mine()
Trig Functions in Degrees<br>
&nbsp;&nbsp;&nbsp;&nbsp;'D' and 'P' trig functions work with degrees.<br>
&nbsp;&nbsp;&nbsp;&nbsp;'P' inverse functions return only positive angles.

greek  &#10230; a string with greek alphabet.<br>
pltsize( w, h, dpi=150) &#10230; resizes plots in matplotlib.<br>
getTS() &#10230; returns a readable time stamp string.<br>
isInstalled( pkgNameStr) &#10230; returns package or None if pkg is not installed.<br>
timeStampStr() &#10230; returns a readable, timestamp string.<br>
mine() &#10230; lists what handies.py defines.
### If PyQt5 package is available defines:
select_file and select_file_timeout
### From math imports these functions:
pi, sqrt, cos, sin, tan, acos, asin, atan, atan2,
degrees, radians, log, log10, exp
### When astropy is available:
Defines nowMJD(); mjd2date(), date2mjd().<br>
Imports astropy.units as "u", i.e. u.cm or u.GHz

## import_install
### importInstall()
    pkg = importInstall( 'pkg_name')
    OR
    pkg = importInstall( 'pkg_name, 'PyPI_name')
This function tries to import a specified package and if that fails,
it tries to install the package and then import it.<br>
_*importInstall*_ was written so that python programs can be
distributed to students without detailed instructions on checking if
package is installed
and on installing the needed packages.<br>
The function returns the package or None.<br>

**Warning:** _importInstall_ can not install all packages. It is less likely to install a package that is not pure python.

<hr>
All functions should have doc strings that give more information about usage and parameters.

