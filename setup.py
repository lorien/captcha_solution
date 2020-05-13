from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name = 'captcha-solution',
    version = '0.0.5',
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    maintainer='Gregory Petukhov',
    maintainer_email='lorien@lorien.name',
    url='https://github.com/lorien/captcha_solution',
    description = 'Universal interface to captcha solving services',
    long_description = open(os.path.join(ROOT, 'README.md')).read(),
    long_description_content_type = 'text/markdown',
    packages = find_packages(exclude=['test', 'script']),
    download_url='https://github.com/lorien/captcha_solver/releases',
    license = "MIT",
    install_requires = ['urllib3'],
    keywords='captcha antigate rucaptcha 2captcha',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
