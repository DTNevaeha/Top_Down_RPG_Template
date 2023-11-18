from setuptools import find_packages
from setuptools import setup

setup(
    name='rpg-template',
    version='1.0.0',
    description='RPG Template',
    author='Blake Ellsworth',
    author_email='DTNevaeha@gmail.com',
    url='https://github.com/DTNevaeha/top_down_RPG',
    packages=find_packages(),
    entry_point={
        'console_scripts': [
            'rpg-template-cli = top_down_rpg.main:main',
        ]
    }
)
