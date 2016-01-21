from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='singleurlcrud',
    description='Django CRUD, implemented using a single view and consequently a single URL.',
    long_description=readme,
    version='0.14',
    author='Hari Mahadevan',
    author_email='hari@hari.xyz',
    url='https://www.github.com/harikvpy/crud/tarball/0.14',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-pure-pagination', 'django-bootstrap3'],
    license='BSD-3',
    keywords=['django', 'crud'],
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
