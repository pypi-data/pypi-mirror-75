import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eznotify", # Replace with your own username
    version="0.0.2",
    author="Eshan Nalajala",
    author_email="eshan.nalajala@gmail.com",
    description="eznotify the easiest way to send notifications to windows 10",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/eznotify/",
    packages=setuptools.find_packages(),
    install_requires=[
        'win10toast'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
