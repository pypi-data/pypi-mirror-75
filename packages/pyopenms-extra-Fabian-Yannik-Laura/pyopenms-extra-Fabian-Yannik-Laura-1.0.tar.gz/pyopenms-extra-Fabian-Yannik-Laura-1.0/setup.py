import setuptools

with open("pyopenms-extra/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyopenms-extra-Fabian-Yannik-Laura", # Replace with your own username
    version="1.0",
    author="Fabian Rosner",
    author_email="fabian@rosner.email",
    description="Teamprojekt SS20 Yannik Haller Fabian Rosner Laura Schöneberg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://fabian1567.github.io/Teamprojekt-SS20-Laura-Yannik-Fabian/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)