from setuptools import setup

from os import path
import shutil

if path.isfile('README.md'):
    shutil.copyfile('README.md', 'README')

setup(
    name='systemwatch',
    description='logwatch for systemd/journald',
    version='0.1.0',
    author='John Reese',
    author_email='john@noswap.com',
    url='https://github.com/jreese/systemwatch',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Logging',
        'Topic :: Utilities',
        'Development Status :: 2 - Pre-Alpha',
    ],
    license='MIT License',
    packages=['systemwatch'],
    scripts=['bin/systemwatch'],
    requires=['ent'],
)
