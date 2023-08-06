import setuptools
from setuptools import setup,Extension

extensions = [Extension("libnetview",
                       ["graph/csv_parser.cpp"],
                       include_dirs=["src"],
              ),
]

setup(
    name = "NetView",
    version = 1.11,
    packages= ["netview","sample","graph","templates"],
    description='Network Grapher',
    install_requires=["networkx","Django","matplotlib"],
    ext_modules=extensions,
    entry_points =
    { 'console_scripts':
        [
            'runmyserver = sample.run:main',
            'initmigrate = sample.init:main',
        ]
    },
)