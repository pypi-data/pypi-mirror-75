from setuptools import find_packages, setup

setup(
    name='talos-python3',
    version='0.0.2',
    author='huyumei',
    author_email='huyumei@xiaomi.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cffi',
        'python-snappy',
        'atomic'
    ],
)

