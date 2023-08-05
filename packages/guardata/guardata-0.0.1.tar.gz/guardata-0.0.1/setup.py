import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guardata",
    version="0.0.1",
    author="BitLogiK",
    author_email="contact@bitlogik.fr",
    description="Desktop client for a modern and trustless data cloud storage service",
    license = "GPLv3",
    keywords = "cloud data storage sharing cryptography",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Topic :: Communications :: File Sharing",
        "Topic :: Office/Business",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Archiving :: Backup",
    ],
    python_requires='>=3.6',
)