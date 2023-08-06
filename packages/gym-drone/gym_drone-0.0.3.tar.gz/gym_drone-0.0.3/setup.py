import setuptools
from pathlib import Path

setuptools.setup(
    name='gym_drone',
    version='0.0.3',
    description="A OpenAI Gym Env for drone",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="gym_drone*"),
    install_requires=['gym']  # And any other dependencies foo needs
)
