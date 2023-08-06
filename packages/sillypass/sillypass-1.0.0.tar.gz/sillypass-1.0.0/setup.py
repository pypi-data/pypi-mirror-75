from setuptools import find_packages, setup


setup(
    name="sillypass",
    version="1.0.0",
    description=(
        "Generate random passwords following silly rules like 1 letter,"
        " 1 number, 1 symbol"
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rjmorris/sillypass",
    author="Joey Morris",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">= 3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "sillypass=sillypass.__main__:main",
        ],
    },
)
