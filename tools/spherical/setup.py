from distutils.core import setup, Extension

module1 = Extension('spherical',
                    sources = ['spherical.c'])

setup (name = 'SphericalHarmonics',
       version = '0.1',
       description = 'Tiny Python module for calculating spherical harmonics and the power spectrum C_l, up to l=10',
       ext_modules = [module1])
