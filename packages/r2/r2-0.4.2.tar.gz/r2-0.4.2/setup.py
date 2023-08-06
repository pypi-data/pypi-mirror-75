import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

with open("../VERSION", "r") as vr:
    version_number = vr.read()

with open("../requirements.txt", "r") as req:
    requirements = []
    for l in req.readlines():
        requirements.append(l.rstrip())

setuptools.setup(
    name="r2",
    version=version_number,
    author="Nex Sabre",
    author_email="nexsabre@protonmail.com",
    description="Software 'r2' is designed to record and replay responses (to mock) from REST API services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NexSabre/r2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'r2 = r2.main:main'
        ],
    },
)
