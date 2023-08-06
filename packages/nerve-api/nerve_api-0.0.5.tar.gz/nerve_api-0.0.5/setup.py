from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()

setup(
    name="nerve_api",
    version="0.0.5",
    author="TTTech Industrial Automation AG",
    author_email="hannes.brantner@tttech-industrial.com",
    description="Package that exposes the Nerve API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://git.tttech.com/projects/BUIENG/repos/nerve-examples/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
