
from setuptools import setup
import snip_setuptools_verify1

setup(
    zip_safe=False,
    packages=['snip_setuptools_verify1'],
    ext_modules=[snip_setuptools_verify1.ffi.verifier.get_extension()])
