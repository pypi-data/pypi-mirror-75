import setuptools
from setuptools import setup

setup(name='ondine_laser_control',
      version='0.1.21',
      description='Control laser attachment on OpenTrons robot',
      author='Caden Keese',
      author_email='ckeese@ondinebio.com',
      license='MIT',
      packages=setuptools.find_packages(),
      instalrequires=[
          'opentrons>=3.19.0',
          'pyserial>=3.4',
          'pydantic>=1.5.1'
      ],
      include_package_data=True,
      zip_safe=False)
