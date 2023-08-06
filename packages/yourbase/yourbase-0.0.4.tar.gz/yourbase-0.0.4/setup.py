import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="yourbase",
    version="0.0.4",
    author="YourBase",
    author_email="ben@yourbase.io",
    description="Test acceleration usable in the YourBase CI",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/yourbase/yourbase-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
        "Framework :: Pytest",
    ],
    python_requires=">=3.6",
    install_requires=["coverage"],
    # Register hooks with pytest:
    entry_points={"pytest11": ["yourbase = yourbase.pytest"]},
)
