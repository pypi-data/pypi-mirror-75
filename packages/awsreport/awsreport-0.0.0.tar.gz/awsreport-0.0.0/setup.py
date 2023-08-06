import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='awsreport',
    author="Gabriel 'bsd0x' Dutra",
    author_email="gmdutra.bsd@gmail.com",
    description="AWSReport is a tool for analyzing amazon resources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsd0x/awsreport",
    packages=['awsreport.core', 'awsreport.awsresources'],
    keywords=["aws", "report", "amazon"],
    install_requires = [
        'boto3',
        'colorama'
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email"
    ],
)
