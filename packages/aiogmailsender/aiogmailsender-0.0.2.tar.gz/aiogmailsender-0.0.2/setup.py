import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aiogmailsender',
    version='0.0.2',
    author='babjo',
    url='https://github.com/babjo/aiogmailsender',
    description='Asynchronous Gmail Client',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=['aiosmtplib>=1.1.3']
)
