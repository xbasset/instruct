from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
import pkg_resources

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self._post_install()

    def _post_install(self):
        instruct_dir = Path.home() / ".instruct"
        models_yaml = instruct_dir / "models.yaml"

        # Create the directory if it doesn't exist
        instruct_dir.mkdir(parents=True, exist_ok=True)

        # Create the file if it doesn't exist
        if not models_yaml.exists():
            with models_yaml.open("w") as file:
                file.write("# models.yaml\n")


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
        "console_scripts": ["instruct=instruct.main:cli",],
    },
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            Path(__file__).with_name("requirements.txt").open()
        )
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    
)

