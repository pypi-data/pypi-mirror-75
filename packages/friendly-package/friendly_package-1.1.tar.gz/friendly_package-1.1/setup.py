from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name='friendly_package',
    version='1.1    ',
    packages=[''],
    url='',
    license='GPLv2',
    author='leo',
    author_email='l.ricker93@web.de',
    description='this package does nothing, its purpose lies solely in ensuring pypis upload policy',
    long_description = long_description
)
