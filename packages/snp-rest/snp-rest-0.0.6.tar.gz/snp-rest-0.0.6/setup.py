import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snp-rest", 
    version="0.0.6",
    author="Kevin Pulley",
    author_email="kpulley@imaginecommunications.com",
    description="Simple REST interface to the Selenio Network Processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UndyingScroll",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       "requests-ntlm",
   ],
    python_requires='>=3.6',
)
