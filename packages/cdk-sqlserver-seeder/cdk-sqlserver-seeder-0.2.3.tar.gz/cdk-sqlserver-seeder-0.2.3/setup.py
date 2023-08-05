import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-sqlserver-seeder",
    "version": "0.2.3",
    "description": "A simple CDK seeder for SQL Server RDS databases.",
    "license": "MIT",
    "url": "https://github.com/kolomied/cdk-sqlserver-seeder#readme",
    "long_description_content_type": "text/markdown",
    "author": "Dmitry Kolomiets<kolomied@amazon.co.uk>",
    "project_urls": {
        "Source": "https://github.com/kolomied/cdk-sqlserver-seeder.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "Talnakh.SqlServerSeeder",
        "Talnakh.SqlServerSeeder._jsii"
    ],
    "package_data": {
        "Talnakh.SqlServerSeeder._jsii": [
            "cdk-sqlserver-seeder@0.2.3.jsii.tgz"
        ],
        "Talnakh.SqlServerSeeder": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.8.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-lambda>=1.49.1, <2.0.0",
        "aws-cdk.aws-rds>=1.49.1, <2.0.0",
        "aws-cdk.aws-s3>=1.49.1, <2.0.0",
        "aws-cdk.aws-s3-deployment>=1.49.1, <2.0.0",
        "aws-cdk.aws-secretsmanager>=1.49.1, <2.0.0",
        "aws-cdk.core>=1.49.1, <2.0.0",
        "aws-cdk.custom-resources>=1.49.1, <2.0.0",
        "constructs>=3.0.4, <4.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
