from setuptools import setup, find_packages

setup(
    name='Python Multi Helper',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    description='Several common helpers for Python coding',
    author='Anderson',
    author_email='anderbytes@gmail.com',
    url='https://github.com/anderbytes/PyMultiHelper',

    long_description_content_type="text/markdown",
    long_description=open('README.md').read()
)