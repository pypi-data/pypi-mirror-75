from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="ramachandranplot",
    version="1.0.5",
    description="A Python package to get ramachandranplot for any pdb.",
    long_description=readme(),
    long_description_content_type="text/markdown",
	packages=["ramachandranplot"],
	package_data={'ramachandranplot': ['data/*.data']},
    url="https://github.com/sagarhm/Ramachandranplot",
    author="Sagar H M",
    author_email="sagarhm032000@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "ramachandranplot=Ramachandranplot.cli:main",
        ]
    },
)