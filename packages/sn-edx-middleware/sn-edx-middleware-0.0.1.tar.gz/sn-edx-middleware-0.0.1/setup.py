import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sn-edx-middleware",
    version="0.0.1",
    author="James Reeve",
    author_email="james.reeve@ibm.com",
    description="middleware for Skills Network deployments of openedx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ibm.com/skills-network-portals/sn-edx-middleware",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
