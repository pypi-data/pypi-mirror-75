from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=["pygame==1.9.6", "wheel==0.34.2"],
    name="flappy_bird_engine",
    version="0.0.4",
    author="Joshua Billson",
    author_email="jmbillson@outlook.com",
    description="A game engine for Flappy Bird powered by Pygame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoshuaBillson/Flappy_Bird_Engine.git",
    packages=["flappy_bird", "src"],
    data_files=[('assets', ['assets/Bird.png', 'assets/pipe.png', 'assets/Ground.png', 'assets/bg.png'])], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
