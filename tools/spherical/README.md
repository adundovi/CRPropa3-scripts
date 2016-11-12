To test module:
```
make
make test
```

To build and install python module:
```
make install
```

Usage:
```
import spherical
spherical.AssociatedLegendreP(5, 0, 0.3)
spherical.SphericalHarmonics(1, 1, 0.5, 0.5)
spherical.C(5, [0.2, 0.1, 0.0], [0.0, 0.4, 0.8])
```

== References ==
* SciPy implementation, https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.special.sph_harm.html
* Wolfram Mathematica, https://reference.wolfram.com/language/ref/SphericalHarmonicY.html
