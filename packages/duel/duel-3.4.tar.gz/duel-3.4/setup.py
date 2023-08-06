import pathlib
from setuptools import setup
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="duel",
    version="3.4",
    description="Locally Multiplayer Dueling game",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexisDougherty13/Duel",
    author="Pythson Buds",
    author_email="zachary.s1110@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=  setuptools.find_packages(),
    package_dir = {'duel' : 'duel'},
    install_requires=["pygame==2.0.0.dev10"],
    entry_points={
        "console_scripts": [
            "duel=duel.__main__:main",
        ]
    },
    package_data = {'duel': ['Resources/Images/*.png', 'Resources/Images/Buttons/*.png', 'Resources/*.ttf', 'Resources/*.wav', 'Resources/*.txt']}
)
