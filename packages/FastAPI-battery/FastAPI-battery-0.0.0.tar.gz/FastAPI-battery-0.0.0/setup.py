import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FastAPI-battery",
    version="0.0.0",
    author="d_mok",
    author_email="unknown@gmail.com",
    description="Some private battery for FastAPI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=['FastApp'],
    license='MIT',
    install_requires=['fastapi','itsdangerous','aiofiles','SQLAlchemy','sqltap'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
