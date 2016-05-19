from setuptools import setup, find_packages

import singleurlcrud

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

version = singleurlcrud.__version__

setup(
    name='singleurlcrud',
    description='Django CRUD using a single view and hence a single URL.',
    long_description=readme + '\n\n' + history,
    version=version,
    author='Hari Mahadevan',
    author_email='hari@hari.xyz',
    url='https://www.github.com/harikvpy/crud/',
    packages=[
        'singleurlcrud',
        ],
    include_package_data=True,
    install_requires=[
        'django-pure-pagination',
        'django-bootstrap3'
        ],
    license='BSD-3',
    keywords=[
        'django',
        'crud',
        'singleurlcrud',
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        ],
    )
