import os
from distutils.core import setup
import setuptools

modules = ['dev_ping_tester']
package_data = {}
setup(
  name = 'dev-ping-tester',         # How you named your package folder (MyLib)
  packages = modules,   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A automation framework to simplify automation tasks',   # Give a short description about your library
  author = 'Jiaming Li',                   # Type in your name
  author_email = 'jiaminli@cisco.com',      # Type in your E-Mail
  url = 'https://www.github.com/ljm625/dev_ping_tester',   # Provide either the link to your github or to your website
  download_url = 'https://www.github.com/ljm625/dev_ping_tester/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['AUTOMATION', 'CISCO'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pexpect',
      ],
  scripts=[],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2',  # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 2.7',  # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  package_data = package_data
)
