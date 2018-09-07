from setuptools import setup

setup(
    name='VidekClient',
    version='0.1dev',
    packages=['videkrestclient'],
    scripts=['videk-client', 'set-hostname'],
    data_files=[('/etc/videk', 'conf')],
    install_requires=[
    'requests',
    'netifaces'
    ]
)
