from setuptools import find_namespace_packages, setup

setup(
    name="training_data_generation",
    packages=find_namespace_packages(where="python"),
    package_dir={"": "python"},
    version="1.0.0",
    install_requires=[text_to_cad_common],
    author="Monica Perez Serrano",
    author_email="monicapserrano@outlook.com",
    description="Generation of training data",
    url="https://github.com/monicapserrano/text_to_cad/training_data_generation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    scripts=["scripts/generate_cylinder_data.py", "scripts/generate_sphere_data.py"],
)
