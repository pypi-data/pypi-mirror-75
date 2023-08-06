from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name='maximshumilo_tools',
    version='0.1.13',
    packages=['ms_tools', 'ms_tools.flask'],
    url='https://t.me/MaximShumilo',
    license='',
    author='Maxim Shumilo',
    author_email='shumilo.mk@gmail.com',
    install_requires=['flask', 'requests', 'marshmallow', 'mongoengine', 'boto3'],
    include_package_data=True,
    long_description=long_description,
)
