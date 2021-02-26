from setuptools import find_packages, setup

# https://stackoverflow.com/questions/50155464/using-pytest-with-a-src-layer
setup(
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
