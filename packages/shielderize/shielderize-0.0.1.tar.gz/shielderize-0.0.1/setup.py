from setuptools import find_packages, setup

with open('README.md', "r") as readme:
    long_description = readme.read()

setup(
    name="shielderize",
    version="0.0.1",
    author="Kimball Leavitt",
    author_email="kimbo@kimballleavitt.com",
    description="Turn text into shields",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/kimbo/shielderize",
    package_data={'': ['README.md', 'LICENSE']},
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'shielderize = shielderize:main',
        ],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
