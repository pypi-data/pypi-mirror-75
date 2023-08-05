import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssafy", # Replace with your own username
    version="0.0.1",
    author="djohnkang",
    author_email="john@hphk.kr",
    description="A package for SSAFY students",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hp-hk/ssafy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ssafy=ssafy.cli:main'
        ]
    }
)