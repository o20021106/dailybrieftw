import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dailybrieftw",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/o20021106/dailynewstw.git",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
