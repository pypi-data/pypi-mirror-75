import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="se4ai-group4-common-utils", # Replace with your own username
    version="0.3.7",
    author="Daniel Biales",
    author_email="dbiales@andrew.cmu.edu",
    description="A package for common utility functions that our project needs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmu-seai/group-project-se4ai-group-4",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['wheel','boto3','psycopg2-binary','sqlalchemy','surprise']
)
