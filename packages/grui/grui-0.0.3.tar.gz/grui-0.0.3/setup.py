import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("version", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="grui",
    version=version,
    author="SECRET Olivier",
    author_email="pypi-package-grui@devo.live",
    description="An ready to use exposer from services oriented code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/olive007/grui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
