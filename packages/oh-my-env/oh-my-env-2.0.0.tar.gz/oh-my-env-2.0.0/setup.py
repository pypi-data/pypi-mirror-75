from setuptools import setup, find_packages
import sys, os

version = '2.0.0'

setup(name='oh-my-env',
      version=version,
      description="",
      long_description="""\
""",
      keywords='',
      author='torpedoallen',
      author_email='torpedoallen@gmail.com',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
      ],
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'envparse==0.2.0',
          'cryptography==3.0.0',
          'ujson>=3.0.0',
          'six>=1.11.0',
          'pytest<5.0.0',
      ],
      extras_require={
        'testing': ['pytest'],
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
