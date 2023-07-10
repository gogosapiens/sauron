from setuptools import setup, find_packages

setup(
    name='carloapps',
    version='0.1.0',
    description='Description of your package',
    packages=find_packages(),
    install_requires=[
        'git+https://github.com/gogosapiens/carlo',
    ],
)