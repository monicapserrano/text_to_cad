from setuptools import find_namespace_packages, setup

setup(
    name="text_to_cad",
    packages=find_namespace_packages(where="python"),
    package_dir={"": "python"},
    version="1.0.0",
    install_requires=[ #TODO(@monicapserrano)
        # List your package dependencies here, e.g.,
        # "numpy>=1.18.0",
    ],
    author="Monica Perez Serrano",
    author_email="monicapserrano@outlook.com",
    description="Text to CAD.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/monicapserrano/text_to_cad/training_data_generation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    scripts=["scripts/run_text_to_cad.py"],
)