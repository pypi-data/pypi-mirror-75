from setuptools import setup, find_packages

setup(
    name='vtex',
    version='0.1',
    license="MIT",
    description='VTEX API Wrapper for Python',
    author='Leandro Meili',
    author_email='leandro.meili@gmail.com',
    packages=find_packages(exclude=("test",)),
    install_requires=['requests'],
)
