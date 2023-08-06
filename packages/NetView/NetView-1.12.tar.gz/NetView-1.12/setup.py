import setuptools
from setuptools import setup,Extension


setup(
    name = "NetView",
    version = 1.12,
    packages= ["netview","sample","graph","templates"],
    description='Network Grapher',
    install_requires=["networkx","Django","matplotlib"],
    entry_points =
    { 'console_scripts':
        [
            'runmyserver = sample.run:main',
            'initmigrate = sample.init:main',
        ]
    },
)