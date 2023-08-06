import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_requirements = list()

with open("_setup_requirements.txt", 'r') as fh:
    for line in fh.readlines():
        requirement = line.strip("\n")
        setup_requirements.append(requirement)

setuptools.setup(
    name="client_agreement_api",
    version="0.0.1",
    author="Abdullah Abid",
    author_email="abdullahabid3691@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abdullahabid3691/ClientAgreement-Api",
    packages=setuptools.find_packages(),
    install_requires=setup_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
