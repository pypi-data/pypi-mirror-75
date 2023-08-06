import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="icecoal", # Replace with your own username
    version="1.0.5",
    author="Prakash Maria Liju P",
    author_email="ppml38@gmail.com",
    description="Lightweight SQL database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ppml38/icecoal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
