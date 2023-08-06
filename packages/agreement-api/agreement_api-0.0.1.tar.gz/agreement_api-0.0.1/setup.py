from setuptools import setup, find_packages

requirements = [
    "connexion==2.7.0",
    "flask==1.1.1",
    "Flask-SQLAlchemy==2.4.4",
    "flask-marshmallow",
    "marshmallow",
    "marshmallow-sqlalchemy",
    "Werkzeug",
]

setup(
    name="agreement_api",
    version="0.0.1",
    author="Abdullah Abid",
    author_email="abdullahabid3691@gmail.com",
    description="Provides an Api powered by flask and connexion.",
    long_description="Provides an Api powered by flask and connexion.",
    long_description_content_type="text/markdown",
    url="https://github.com/Abdullahabid3691/user_agreement_flask_api",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
