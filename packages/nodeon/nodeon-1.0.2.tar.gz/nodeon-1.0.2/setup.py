from setuptools import setup

setup(
    name="nodeon",
    version="1.0.2",
    description="A program to create Node.js virtual environments.",
    author="Finn",
    url="https://github.com/Shu-Ji/nodeon",
    py_modules=['nodeon'],
    install_requires=['requests', 'plumbum'],
)
