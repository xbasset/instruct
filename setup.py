from setuptools import setup, find_packages
from pathlib import Path
import pkg_resources

setup(
    name='instruct',
    version='0.1',
    packages=find_packages(),
    description="Craft, Run, Evaluate Instructions for Large Language Models",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    python_requires=">=3.10",
    author="Xavier Basset",
    url="https://github.com/xbasset/instruct",
    license="MIT",
      entry_points={
        "console_scripts": ["instruct=main:cli",],
    },
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            Path(__file__).with_name("requirements.txt").open()
        )
    ],
    
)
