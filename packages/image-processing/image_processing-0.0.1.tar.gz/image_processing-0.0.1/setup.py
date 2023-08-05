from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing",
    version="0.0.1",
    author="Karina Tiemi",
    description="Image processing package using skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiemi/image-processing-package",
    packages=find_packages(),
    package_data = {
        "image_processing": ["sample_images/*.jpg"]
    },
    include_package_data = True,
    install_requires=requirements,
    python_requires='>=3.5',
)