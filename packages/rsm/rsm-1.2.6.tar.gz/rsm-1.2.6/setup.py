from setuptools import setup, find_namespace_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rsm',
    version='1.2.6',
    packages=find_namespace_packages(include='rsm.*'),
    url='https://github.com/antoinethebuilder/realsiemplify',
    license='MIT',
    author='Antoine',
    author_email='64340767+antoinethebuilder@users.noreply.github.com',
    description="Let's simplify things for real, shall we? ",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
