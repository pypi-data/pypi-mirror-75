import sys
from setuptools import setup, find_packages


# For some reason Python 2.7 doesn't like the new python_requires format
if sys.version_info.major < 3:
    python_requires = '>=2.7'
else:
    python_requires = '>=2.7, >=3'

setup(
    name='ascid',
    description='Ascid is the Self-referential Cycle IDentifier. It is capable of quickly (in linear time) detecting'
                'the maximum length repeated substrings in text files.',
    url='https://github.com/esultanik/ascid',
    author='Trail of Bits',
    version='0.2.0',
    packages=find_packages(),
    python_requires=python_requires,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ascid = ascid.__main__:main'
        ]
    },
    extras_require={
        "dev": ["flake8", "setuptools"]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Text Processing'
    ]
)
