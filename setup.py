from setuptools import setup, find_packages

setup(
    name='singleurlcrud',
    description='Django CRUD, implemented using a single view and consequently a single URL.',
    long_description=open('README.md').read(),
    version='0.13',
    author='Hari Mahadevan',
    author_email='hari@hari.xyz',
    url='https://www.github.com/harikvpy/crud/tarball/0.13',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-pure-pagination', 'django-bootstrap3'],
    license='BSD-3',
    keywords=['django', 'crud'],
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
