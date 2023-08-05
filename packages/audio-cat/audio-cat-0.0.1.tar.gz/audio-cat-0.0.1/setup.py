import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_requirements():
    with open('requirements.txt') as requirements:
        req = requirements.read().splitlines()
    return req

setuptools.setup(
    name="audio-cat",
    version="0.0.1",
    author="Nathaniel Cherian",
    author_email="nathaniel@sylica.com",
    description="audio splitter and labeler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nathanielCherian/audio-cat",
    download_url = 'https://github.com/nathanielCherian/audio-cat/archive/v0.0.1.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.6',
    install_requires= get_requirements(),
    entry_points = {
        'console_scripts': ['audio-cat=supervisor.command_line:main'],
    }

)