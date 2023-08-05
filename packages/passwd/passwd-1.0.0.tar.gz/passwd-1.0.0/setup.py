import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passwd",
    version="1.0.0",
    author="Benjamin Soyka",
    author_email="bensoyka@icloud.com",
    description="Assorted utilities for gracefully handling and generating passwords",
    long_description=long_description,
    url="https://github.com/bsoyka/passwd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://bsoyka.github.io/passwd",
        "Changelog": "https://github.com/bsoyka/passwd/blob/master/CHANGELOG.md",
    },
    install_requires=["requests~=2.24.0"],
)
