from setuptools import setup, find_packages

setup(
    name='axentx-product',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    tests_require=[],
    package_data={'': ['*.py']},
    include_package_data=True,
)
