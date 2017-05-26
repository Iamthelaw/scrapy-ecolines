from setuptools import setup, find_packages

setup(
    name         = 'zxtiger_ecolines',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = zxtiger_ecolines.settings']},
)
