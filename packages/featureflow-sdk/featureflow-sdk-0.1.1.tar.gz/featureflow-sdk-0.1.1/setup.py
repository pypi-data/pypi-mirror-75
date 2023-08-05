import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="featureflow-sdk",
    version="0.1.1",
    author="Featureflow",
    author_email="featureflow@featureflow.io",
    description="Python 3 SDK for the featureflow feature management platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/featureflow/featureflow-python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'Faker'
    ],
    python_requires='>=3.6',
)
