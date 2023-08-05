import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="thirties",
    version="0.0.2",
    author="Vitalii Abetkin",
    author_email="abvit89@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
)