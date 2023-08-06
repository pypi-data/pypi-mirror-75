import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='note-shell',
    version='1.4.0',
    author='Nirabhra Tapaswi',
    author_email='nirabhratapaswi@gmail.com',
    description='Command line tool for making notes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nirabhratapaswi/nShells',
    packages=['note'],
    install_requires=[
        'readchar',
        'tabulate',
        'PyInquirer',
        'pysqlite3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': ['note=note.main:main'],
    },
    include_package_data=True
)
