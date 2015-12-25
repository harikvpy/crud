from setuptools import setup, find_packages

setup(
    name="singleurlcrud",
    description="Django CRUD using a single view, and hence single URL, for all CRUD operations",
    long_description=open('README.md').read(),
    version="0.5",
    author="Hari Mahadevan",
    author_email="hari@hari.xyz",
    url="http://www.github.com/harikvpy/singleurlcrud",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-bootstrap3'],
    license="BSD2",
    keywords="django crud",
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Approved :: BSD2 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        ],
    )
