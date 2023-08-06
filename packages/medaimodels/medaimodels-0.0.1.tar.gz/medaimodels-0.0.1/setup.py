import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medaimodels", # Replace with your own username
    version="0.0.1",
    author="Travis Clarke",
    author_email="travisjonathanclarke@gmail.com",
    description="A libarary for creating med-ai models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Travis-Med-AI/med-ai-models",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)