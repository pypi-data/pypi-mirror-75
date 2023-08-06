import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="continuum",
    version="0.1.4",
    author="Arthur Douillard, Timothée Lesort",
    author_email="ar.douillard@gmail.com",
    description="A clean and simple library for Continual Learning in PyTorch.",
    license='MIT',
    url="https://github.com/Continvvm/continuum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
