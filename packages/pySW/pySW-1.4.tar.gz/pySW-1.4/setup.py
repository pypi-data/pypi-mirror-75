import setuptools
#
with open("README.md", "r") as fh:
    long_description = fh.read();
#
setuptools.setup(
    name="pySW",
    packages = ['pySW'],
    version="1.4",
    author="Kalyan Inamdar",
    author_email="kalyaninamdar@protonmail.com",
    url = 'https://github.com/kalyanpi4/pySW',
    download_url='https://github.com/kalyanpi4/pySW/archive/V1.4.tar.gz',
    description="A Wrapper around Solidworks VBA API for Automating Geometry Modifications for Python based Optimization and Design Space Exploration.",
	long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
          'numpy',
          'pandas',
          'pywin32',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)