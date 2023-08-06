import setuptools

with open("READMESETUP.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyunitgen",  # Replace with your own username
    version="0.0.1a2",
    author="Fangnikoue Evarist",
    author_email="malevae@gmail.com",
    description="A python unittest generator for all your python files.",
    long_description=long_description,
    url="https://github.com/eirtscience/pyunitgen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'faker',
        'autopep8'
    ],
    python_requires='>=3.5',
)
