import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seciva",
    version="0.1.1",
    author="Евгений Ковалевич",
    author_email="evgen.kovalevich@gmail.com",
    description="Реализация многослойной нейронной сети на python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kovalevich/seciva",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

