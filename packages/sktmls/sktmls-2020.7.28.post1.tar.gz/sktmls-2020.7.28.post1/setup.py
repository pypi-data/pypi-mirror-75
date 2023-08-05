import setuptools
import os

SKTMLS_VERSION = os.getenv("SKTMLS_VERSION")
if not SKTMLS_VERSION:
    raise TypeError("NO SKTMLS_VERSION")


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


setuptools.setup(
    name="sktmls",
    version=SKTMLS_VERSION,
    author="Colin",
    author_email="colin@sktai.io",
    description="A package for MLS-Models",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/mls-model-registry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "attrs==19.3.0",
        "boto3==1.13.25",
        "botocore==1.16.26",
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "docutils==0.15.2",
        "idna==2.10",
        "importlib-metadata==1.6.0",
        "jmespath==0.10.0",
        "joblib==0.14.1",
        "lightgbm==2.3.1",
        "Mako==1.1.3",
        "Markdown==3.2.2",
        "MarkupSafe==1.1.1",
        "more-itertools==8.3.0",
        "numpy==1.18.3",
        "packaging==20.4",
        "pandas==1.0.3",
        "pdoc3==0.8.4",
        "pluggy==0.13.1",
        "py==1.8.1",
        "pyparsing==2.4.7",
        "pytest==5.4.2",
        "python-dateutil==2.8.1",
        "pytz==2020.1",
        "requests==2.24.0",
        "s3transfer==0.3.3",
        "scikit-learn==0.22.2.post1",
        "scipy==1.4.1",
        "six==1.15.0",
        "urllib3==1.25.9",
        "wcwidth==0.1.9",
        "xgboost==1.0.2",
        "zipp==3.1.0",
    ],
)
