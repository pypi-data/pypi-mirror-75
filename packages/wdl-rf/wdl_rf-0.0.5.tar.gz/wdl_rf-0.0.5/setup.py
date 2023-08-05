import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wdl_rf", # Replace with your own username
    version="0.0.5",
    author="xhj,zqm",
    author_email="2641931752@qq.com",
    description="Create molecular fingerprint features of Ligands and predicting Bioactivities Acting with G Protein-coupled Receptors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)