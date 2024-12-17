from setuptools import setup, find_packages


setup(
    name='PyMultiHelper',
    version='1.1.15',
    packages=find_packages(),
    description='Several common helpers for Python coding',
    author='Anderson',
    author_email='anderbytes@gmail.com',
    url='https://github.com/anderbytes/PyMultiHelper',

    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),

    install_requires=[
        "requests~=2.32.3",
        "pytz~=2024.2",
        "pandas~=2.2.3",
        "speedtest-cli~=2.1.3",
        "beautifulsoup4~=4.12.3"
    ]
)
