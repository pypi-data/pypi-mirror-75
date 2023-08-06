import setuptools

with open('README.md', mode='r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name="py_ewf_mount",
    version="1.0.0",
    author="Florian Wahl",
    author_email="florian.wahl.developer@gmail.com",
    description="A cli wrapper script to mount EWF files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wahlflo/pyEWFmount",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    install_requires=[
       'cli-formatter'
    ],
    entry_points={
        "console_scripts": [
            "pyEWFmount=ewf_mount.script:main",
            "pyMountEWF=ewf_mount.script:main"
        ],
    }
)