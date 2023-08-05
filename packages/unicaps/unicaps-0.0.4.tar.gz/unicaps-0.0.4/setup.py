import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unicaps",
    version="0.0.4",
    author="Sergey Totmyanin",
    author_email="STotmyanin@gmail.com",
    description="Universal CAPTCHA Solver for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergey-scat/unicaps",
    packages=setuptools.find_packages(),
    install_requires=["requests", "dataclasses>=0.7; python_version == '3.6'"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires='>=3.6',
)