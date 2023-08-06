from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
  name = 'bluetooth_battery',
  packages = ['bluetooth_battery'],
  version = '1.2.0',
  license='GPL-3.0',
  description = 'A python script to get battery level from Bluetooth headsets',
  long_description_content_type='text/markdown',
  long_description=long_description, 
  author = 'TheWeirdDev',
  author_email = 'alireza6677@gmail.com',
  url = 'https://github.com/TheWeirdDev/Bluetooth_Headset_Battery_Level',
  download_url = 'https://github.com/TheWeirdDev/Bluetooth_Headset_Battery_Level/archive/v1.2.0.zip',
  keywords = [ "bluetooth", "bluetooth-headsets", "bluetooth-devices", "battery-level", "battery-percentage", "battery", "headset", "linux", "socket", "python", "at-command", "bluetooth-socket", "bluetooth-speaker", "bluez", "headphones", "bluetooth-headphones", "python-script"],
  install_requires=[
          'PyBluez'
      ],
  entry_points = {
        'console_scripts': ['bluetooth_battery=bluetooth_battery.bluetooth_battery:main'],
    },
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
  ],
)
