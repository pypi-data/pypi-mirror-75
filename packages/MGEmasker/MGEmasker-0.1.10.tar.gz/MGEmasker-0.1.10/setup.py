import setuptools
import os
import glob

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name="MGEmasker",
    version="0.1.10",
    author="Anthony Underwood",
    author_email="au3@sanger.ac.uk",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="GPLv3",
    packages=setuptools.find_packages(),
    package_data={'mge_masker': ['mge_patterns.txt', 'tests/data/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mge_masker=mge_masker.run_mge_masker:main'
        ]
    },
    python_requires='>=3',
    install_requires=['biopython'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'coverage']
)