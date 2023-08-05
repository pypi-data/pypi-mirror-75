from distutils.core import setup
with open("README") as file:
    readme=file.read()

setup(
    name='Dentistry',
    version='0.0.1',
    packages=['dentistry'],
    url='https://testpypi.python.org/pypi/dentistry',
    license='LICENSE.txt',
    description='Analysing data in Dentistry',
    long_description=readme,
    author='Alex MH CHAU',
    author_email='himcmh@yahoo.com'
)
