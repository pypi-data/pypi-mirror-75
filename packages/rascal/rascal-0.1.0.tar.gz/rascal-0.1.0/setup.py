# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rascal', 'rascal.arc_lines']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'pynverse>=0.1.4,<0.2.0',
 'scipy>=1.5.2,<2.0.0',
 'tqdm>=4.48.0,<5.0.0']

setup_kwargs = {
    'name': 'rascal',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Rascal\n\nRascal is a library for automated spectrometer wavelength calibration. It has been designed primarily for astrophysics applications, but should be usable with spectra captured from any similar spectrometer.\n\nGiven a set of peaks located in your spectrum, Rascal will attempt to determine a model for your spectrometer to convert between pixels and wavelengths.\n\nUnlike other calibration methods, rascal does not require you to manually select lines in your spectrum. Ideally you should know  approximate parameters about your system, namely:\n\n* What arc lamp was used (e.g. Xe, Hg, Ar, CuNeAr)\n* What the dispersion of your spectrometer is (i.e. angstroms/pixel)\n* The spectral range of your system, and the starting wavelength\n\nYou don't need to know the dispersion and start wavelength exactly. Often this information is provided by the observatory, but if you don't know it, you can take a rough guess. The closer you are to the actual system settings, the more likely it is that Rascal will be able to solve the calibration. Blind calibration, where no parameters are known, is possible but challenging currently. If you don't know the lamp, you can try iterating over the various combinations of sources. Generally when you do get a correct fit, with most astronomical instruments the errors will be extremely low.\n\n## Testing\n\nTo run the unit test suite without installing rascal, `cd` to the root directory and run:\n\n```\npython -m pytest test\n```\n\nTo view logging output during testing, run:\n\n```\npython -m pytest test -s\n```\n",
    'author': 'Josh Veitch-Michaelis',
    'author_email': 'j.veitchmichaelis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jveitchmichaelis/rascal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
