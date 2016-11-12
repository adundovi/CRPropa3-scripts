from distutils.core import setup, Extension

module1 = Extension('spherical',
                    sources = ['sphericalpy.c', 'spherical.c'])

setup (name = 'SphericalHarmonics',
       version = '0.1',
       description = "Module for calculating spherical harmonics Y_{lm} and power spectrum C_l.",
       long_description = 'This is a tiny and fast C extension for Python which \
                          calculate spherical harmonics and power spectrum C_l, up to l=10',
       author = "Andrej Dundovic",
       author_email = "andrej.dundovic@desy.de",
       ext_modules = [module1])
