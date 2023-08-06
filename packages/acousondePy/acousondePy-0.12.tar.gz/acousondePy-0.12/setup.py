# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 17:35:08 2020

@author: sven
"""


from setuptools import setup

setup(name='acousondePy',
      version='0.12',
      description='Read and plot Acousonde MT files',
      author='Sven Gastauer',
      url='https://github.com/SvenGastauer/acousondePy',
      download_url = 'https://github.com/user/acousondePy/archive/0.12.tar.gz',
      author_email='sgastauer@ucsd.edu',
      license='MIT',
      packages=['acousondePy'],
      keywords = ['Acousonde', 'Python', 'acoustics','oceanography'],
      install_requires=[
          'scipy',
          'numpy',
          'pandas',
          'datetime',
          'matplotlib',
        ],
      classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
)