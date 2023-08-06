import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="argusvision",
    version="1.0.3",
    description="Downloads pretrained Argus Vision models",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["torch>=1.2.0", "azure-storage-blob","azure-identity", "tqdm"],
)
