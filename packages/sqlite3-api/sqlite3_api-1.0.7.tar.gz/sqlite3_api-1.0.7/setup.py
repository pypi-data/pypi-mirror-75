from setuptools import setup

with open("README.rst") as rst:
    description = rst.read()

setup(
    name="sqlite3_api",
    version="1.0.7",
    packages=['sqlite3_api', 'sqlite3_api.example'],
    url="https://github.com/AlexDev-py/sqlite3-api.git",
    license="MIT",
    author="AlexDev",
    author_email="aleks.filiov@yandex.ru",
    description="API for sqlite3",
    long_description=description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8"
    ]
)

# sdist
# twine register dist/sqlite3_api-1.0.7.tar.gz
# twine upload dist/sqlite3_api-1.0.7.tar.gz
# -r testpypi
