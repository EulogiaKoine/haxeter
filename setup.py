from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="haxeter_package",
    version="0.0.1",
    author="Eulogia Koinē",
    author_email="elruien0604@gmail.com",
    description="Haxeter RPG's internal Model/Manager for Jupyter Notebook-IPython or Google Colaboratory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EulogiaKoine/haxeter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    package_data={"resources": ["*.txt"], "db": "*.json"},
    include_package_data=True
)