from setuptools import setup

setup(
    name='VidekClient',
    version='0.1dev',
    packages=['videkrestclient',],
    scripts=['videk-client'],
    data_files=[('/etc/videk', ['api.key', 'conf'])],
    install_requires=[
    'requests',
    'netifaces'
    ]
)
