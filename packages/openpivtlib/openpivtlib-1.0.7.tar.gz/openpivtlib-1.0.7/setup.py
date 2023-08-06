import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = []

test_require = [
    'pytest >= 5.0.1',
    'pytest-cov >= 2.7.1',
    'codecov >= 2.0.15',
]

setup(
    name='openpivtlib',
    version='1.0.7',
    description='A library containing common elements to openpivt and PIVT apps built on top of openpivt',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    author='Eric Frechette',
    author_email='eric@softwarefactorylabs.com',
    # url='',
    # keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': test_require,
    },
    install_requires=requires,
    python_requires='>= 3.7',
)
