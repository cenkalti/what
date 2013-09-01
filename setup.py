import os
import re
from setuptools import setup


def read(*fname):
    with open(os.path.join(os.path.dirname(__file__), *fname)) as f:
        return f.read()


def get_version():
    for line in read('what', '__init__.py').splitlines():
        m = re.match(r"""__version__\s*=\s'(.*)'""", line)
        if m:
            return m.groups()[0].strip()
    raise Exception('Cannot find version')


setup(
    name='What',
    version=get_version(),
    author='Cenk Alti',
    author_email='cenkalti@gmail.com',
    keywords='unittest process subprocess',
    url='http://github.com/cenkalti/what',
    packages=['what'],
    description='A helper for testing process output',
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
)
