import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="odi-token-contracts", # Replace with your own username
    version="0.0.4",
    author="Prajwol Gyawali",
    author_email="mail.prajwolgyawali@gmail.com",
    description="Implementation of Mintable, Burnable, Capped, Pausable and Snapshot IRC2 token that can be used as standard token equivalent to ERC20 for ICON blockchain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenDevICON/odi-contracts/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
