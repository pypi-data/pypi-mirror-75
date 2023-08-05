import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
        name="pathomap",
        version="1.0.0",
        author="Abhijit Raj",
        author_email="abhijit18231@iiitd.ac.in",
        description="The Pathomap package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Br34th7aking/Pathomap",
        include_package_data=True,
        install_requires=[
            'pandas',
        ],
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
)
