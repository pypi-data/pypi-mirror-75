import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-simple-attachments",
    version="0.1.1",
    author="ChanMo",
    author_email="chan.mo@outlook.com",
    description="Django Simple Attachment Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChanMo/django-simple-attachments",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
