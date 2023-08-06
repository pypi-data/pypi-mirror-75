import json
from urllib import request
from pkg_resources import parse_version
from setuptools import setup


def versions():
    url = f'https://pypi.python.org/pypi/lgt-data/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


last_version = round(float(versions()[0]) + 0.1, 1) if versions() else 0.0

setup(name='lgt-data',
      version=f'{last_version}',
      description='LGT data builds',
      packages=['lgt_data'],
      include_package_data=True,
      install_requires=[
          'wheel',
          'pymongo',
          'python-dateutil',
          'nameparser'
      ],
      author_email='alexander.grin1997@gmail.com',
      zip_safe=False)

