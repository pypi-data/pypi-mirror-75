from setuptools import setup

with open("README.rst") as rst:
    description = rst.read()

setup(
    name="postgresql-api",
    version="1.0.7",
    packages=["postgresql_api"],
    url="https://github.com/AlexDev-py/postgresql_api.git",
    license="MIT",
    author="AlexDev",
    author_email="aleks.filiov@yandex.ru",
    description="API for postgresql",
    long_description=description,
    install_requires=['psycopg2'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)

# sdist
# twine register dist/postgresql-api-1.0.7.tar.gz
# twine upload dist/postgresql-api-1.0.7.tar.gz
# -r testpypi
