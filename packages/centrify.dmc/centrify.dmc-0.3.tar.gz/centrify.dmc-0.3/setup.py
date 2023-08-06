
from distutils.core import setup
setup(
  name = 'centrify.dmc',
  packages = ['dmc'],
  version = '0.3', 
  license='	apache-2.0',
  description = 'Library to retrieve an access token to Centrify PAS from an enrolled machine',
  author = 'Harvey Kwok',
  author_email = 'harvey.kwok@centrify.com',
  url = 'https://github.com/centrify/dmc-python',
  download_url = 'https://github.com/centrify/dmc-python/archive/v0.3-alpha.tar.gz',
  keywords = ['Centrify', 'DMC'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)