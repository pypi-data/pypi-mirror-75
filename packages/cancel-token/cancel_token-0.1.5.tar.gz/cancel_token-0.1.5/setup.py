from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cancel_token",
    version="0.1.5",
    author="Maciej Nowak",
    description="Simple CancellationToken",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Novakov/py-cancel-token",
    packages=['cancel_token'],
    package_data={
        'cancel_token': ['py.typed']
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities"
    ],
    include_package_data=True
)