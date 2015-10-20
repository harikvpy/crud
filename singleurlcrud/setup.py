from setuptools import setup, find_packages

setup(
    name="singleurlcrud",
    version="0.1",
    packages=find_packages(),

    # dependent packages
    install_requires=['django-bootstrap3'],

    package_data = {
        '': ['*.rst'],
        },

    # project meta information
    author="Hari Mahadevan",
    author_email="hari@hari.xyz",
    description="A Django app that provides a table CRUD view using a single view and URL",
    license="PSF",
    keywords="django crud",
    url="http://www.github.com/harikvpy/singleurlcrud",
    )




