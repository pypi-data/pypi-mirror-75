import setuptools

setuptools.setup(
   name='medis',
   version='0.0.1',
   description='MKID Exoplanet Direct Imaging Simulator',
   author='R. Dodkins, K. Davis',
   author_email='dodkins@ucsb.edu',
   url="https://github.com/MazinLab/MEDIS",
   packages=setuptools.find_packages(),
   install_requires=['bar', 'greek'], #external packages as dependencies
)