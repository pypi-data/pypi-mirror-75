import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dyco',
    packages=setuptools.find_packages(),
    # packages=['dyco'],
    version='0.0.16',
    license='GNU General Public License v3 (GPLv3)',
    description='A Python package to detect and compensate for shifting lag times in ecosystem time series',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lukas Hörtnagl',
    author_email='lukas.hoertnagl@usys.ethz.ch',
    url='https://gitlab.ethz.ch/holukas/dyco-dynamic-lag-compensation',
    download_url='https://pypi.org/project/dyco/',
    keywords=['ecosystem', 'eddy covariance', 'fluxes',
              'time series', 'lag', 'timeshift'],
    install_requires=['pandas', 'numpy', 'matplotlib', 'scipy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
