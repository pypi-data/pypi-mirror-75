from setuptools import setup, find_packages, Extension

with open('README.md') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cloud-curator-cli',
    version='0.1.1',
    author='Joseph Hissong',
    author_email='hissong.joseph@gmail.com',
    license=license,
    packages=find_packages(),
    install_requires=[
        'boto3',
        'Click'
    ],
    entry_points='''
        [console_scripts]
        curator=cloud_curator.main:cli
    ''',
)