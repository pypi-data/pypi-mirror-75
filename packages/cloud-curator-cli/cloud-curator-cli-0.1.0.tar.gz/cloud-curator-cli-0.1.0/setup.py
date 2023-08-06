from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cloud-curator-cli',
    version='0.1.0',
    description='AWS Cloud tool for reports',
    long_description=readme,
    author='Joseph Hissong',
    author_email='hissong.joseph@gmail.com',
    url='',
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