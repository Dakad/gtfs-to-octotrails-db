import os
from setuptools import setup, find_packages


readme = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="gtfs-to-octotrails-db",
    version="0.1.0",
    author="DakaD",
    description='TRansform GTFS into Qcontrol Format DB.',
    long_description=long_description,
    license='MIT',
    keywords='gtfs',
    url='https://github.com/Dakad/gtfs-to-octotrails-db',
    packages=find_packages()
)
