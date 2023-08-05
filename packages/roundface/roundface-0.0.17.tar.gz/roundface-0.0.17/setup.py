import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="roundface",
    version="0.0.17",
    author="Edward Kigozi",
    description="Detect Faces In Images and Generate Profile Photos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Edward-K1/roundface",
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords = "face detect roundface profile photo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts':[
            'roundface = roundface.roundface:execute'

        ]
    }
)