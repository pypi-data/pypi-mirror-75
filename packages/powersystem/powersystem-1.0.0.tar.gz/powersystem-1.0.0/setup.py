import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="powersystem", # Replace with your own username
    version="1.0.0",
    author="Venkataswamy R",
    author_email="venkataswamy.r@gmail.com",
    description="Power System Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/venkataswamyr/python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)