from setuptools import setup, find_packages

setup(
    name='group_stratifier',
    version='0.1.1',
    author='Yigit Ozen',
    packages=find_packages(),
    install_requires=['numpy>=1.17.0', 'pyeasyga'],
)
