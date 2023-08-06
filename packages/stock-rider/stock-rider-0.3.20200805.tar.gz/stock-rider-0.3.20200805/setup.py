import os
from datetime import datetime

import sys
from setuptools import find_packages, setup

dependencies = ['click', 'yfinance', 'pandas', 'numpy', 'tqdm', 'sqlalchemy', 'praw']

# 'setup.py publish-test' shortcut
if sys.argv[-1] == 'publish-test':
    os.system('rm -r dist/*')
    os.system('python setup.py sdist')
    os.system('twine upload -r pypitest dist/*')
    sys.exit()
# 'setup.py publish' shortcut
if sys.argv[-1] == 'publish':
    os.system('rm -r dist/*')
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()

version = datetime.now().strftime("%Y%m%d")

# Get the long description from the relevant file
try:
    # in addition to pip install pypandoc, might have to: apt install -y pandoc
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError) as e:
    print("Error converting README.md to rst:", str(e))
    long_description = open('README.md').read()

setup(
    name='stock-rider',
    version='0.3.' + version,
    url='https://github.com/namuan/stock-rider',
    license='MIT',
    author='DeskRiders Dev',
    author_email='me@deskriders.dev',
    description='Stock Rider',
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    setup_requires=['wheel'],
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'stock-rider = krider.main:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
