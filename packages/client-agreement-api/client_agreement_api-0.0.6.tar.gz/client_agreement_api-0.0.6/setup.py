import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_requirements = list()

# with open("_setup_requirements.txt", 'r') as fh:
#     for line in fh.readlines():
#         requirement = line.strip("\n")
#         setup_requirements.append(requirement)

requirements = [
    "connexion==2.7.0",
    "flask==1.1.1",
    "Flask-SQLAlchemy==2.4.4",
    "flask-marshmallow",
    "marshmallow",
    "marshmallow-sqlalchemy",
    "Werkzeug",
]

setuptools.setup(
    name="client_agreement_api",
    version="0.0.6",
    author="Abdullah Abid",
    author_email="abdullahabid3691@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abdullahabid3691/ClientAgreement-Api",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
