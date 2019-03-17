from setuptools import setup, find_packages

setup(
    name='uwh-display',
    version='2.0.0',
    packages=find_packages(
        'rgbmatrix',
        'Adafruit_LED_Backpack'
    ),
    scripts=['bin/uwhdd'],
)
