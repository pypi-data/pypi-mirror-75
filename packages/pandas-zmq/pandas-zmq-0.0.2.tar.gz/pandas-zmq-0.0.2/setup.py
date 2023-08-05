import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandas-zmq",
    version="0.0.2",
    author="Ralph Ritoch",
    author_email="rritoch@gmail.com",
    description="Communicate Pandas DataFrame over ZeroMQ connection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rritoch/pandas_zmq",
    packages=['pandas_zmq'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyzmq',
    ],
    python_requires='>=3.3',
)
