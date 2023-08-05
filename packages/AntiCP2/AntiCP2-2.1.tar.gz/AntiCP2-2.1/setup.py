import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AntiCP2", # Replace with your own username
    version="2.01",
    author="Raghava Group",
    author_email="raghavagps@gmail.com",
    description="A package for calculating anticancer peptides",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://webs.iiitd.edu.in/raghava/anticp2/",
    keywords='Prediction Anticancer Peptides',
    install_requires=['scikit-learn'],
    package_data={
        'aac_extra_model': ['aac_extra_model'],
        'dpc_extra_model': ['dpc_extra_model'],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

