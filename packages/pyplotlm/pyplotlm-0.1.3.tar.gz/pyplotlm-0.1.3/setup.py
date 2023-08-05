from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'pyplotlm',
  packages = ['pyplotlm'],
  version = '0.1.3',
  license = 'MIT',
  description = 'A Python package for sklearn to produce linear regression summary and diagnostic plots similar to those made in R with summary.lm and plot.lm',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = 'Esmond Chu',
  author_email = 'chuhke@gmail.com',
  url = 'https://github.com/esmondhkchu/pyplotlm',
  download_url = 'https://github.com/esmondhkchu/pyplotlm/archive/v0.1.3.tar.gz',
  keywords = ['statistics', 'machine learning', 'regression'],
  test_suite = 'tests',
  install_requires = ['numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
