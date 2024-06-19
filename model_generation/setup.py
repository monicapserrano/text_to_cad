from setuptools import find_namespace_packages, setup

setup(
    name="model_generation",
    packages=find_namespace_packages(where="python"),
    package_dir={"": "python"},
    version="1.0.0",
    install_requires=["pytorch", "python3-text-to-cad-common"],
    author="Monica Perez Serrano",
    author_email="monicapserrano@outlook.com",
    description="Train and generate the model: text to parameter.",
    url="https://github.com/monicapserrano/text_to_cad/training_data_generation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    scripts=["scripts/train_model.py"],
)