import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythonPlus",
    version="1.0",
    author="Dropout1337",
    description="My Personal Python Module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dropout1337/PythonPlus",
    packages=setuptools.find_packages(),
    install_requires=["requests"]
)
