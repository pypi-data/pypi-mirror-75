from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(name = "bingau",
      version = '1.0',
      description = 'Gaussian & Binomial distributions',
      url='https://github.com/tyagihardik42/bingau',
      packages = ['bingau'],
      author = 'Hardik Tyagi',
      author_email = 'tyagi.hardik42@yahoo.com',

      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],

      keywords='binomial, gaussian, distribution',
      install_requires=[
          'matplotlib',
      ],

      project_urls={  
        'Bug Reports': 'https://github.com/tyagihardik42/bingau/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'https://saythanks.io/to/tyagi.hardik42%40yahoo.com',
        'Source': 'https://github.com/tyagihardik42/bingau',
    },

      
      zip_safe = False)
