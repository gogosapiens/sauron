from setuptools import setup, find_packages

setup(
    name='sauron',
    version='0.1.2',
    description='Description of your package',
    packages=find_packages(),
    install_requires=[
        'carlo @ git+https://github.com/gogosapiens/carlo'
    ],
    dependency_links=[
        'git+https://github.com/gogosapiens/carlo#egg=carlo'
    ]
)