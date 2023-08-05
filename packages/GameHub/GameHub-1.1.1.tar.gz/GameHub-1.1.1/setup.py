"""
How to upload new version:
1. Delete dist
2. Up the version number
3. Create dist directory using command: python setup.py sdist bdist_wheel
4. Upload using command: twine upload dist/*
"""
import pathlib
import setuptools
import get_version_number


from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='GameHub',
    version=get_version_number.get_version_number(),
    description='Hub of games to play from',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/bGerma/game_hub',
    author='Brooklyn Germa',
    author_email='brooklyn.germa@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'click-repl', 'click', 'tabulate', 'PyInquirer', 'clint'
    ],
    packages=setuptools.find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    py_modules=['gameHub', 'gameHubCLI'],
    entry_points='''
        [console_scripts]
        gameHub=gameHubCLI:cli
    ''',
    include_package_data=True
)
