import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-serverless-lamp",
    "version": "1.3.5",
    "description": "A JSII construct lib to build AWS Serverless LAMP with AWS CDK",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-serverless-lamp.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<hunhsieh@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-serverless-lamp.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_serverless_lamp",
        "cdk_serverless_lamp._jsii"
    ],
    "package_data": {
        "cdk_serverless_lamp._jsii": [
            "cdk-serverless-lamp@1.3.5.jsii.tgz"
        ],
        "cdk_serverless_lamp": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-apigateway>=1.56.0, <2.0.0",
        "aws-cdk.aws-apigatewayv2>=1.56.0, <2.0.0",
        "aws-cdk.aws-ec2>=1.56.0, <2.0.0",
        "aws-cdk.aws-iam>=1.56.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.56.0, <2.0.0",
        "aws-cdk.aws-rds>=1.56.0, <2.0.0",
        "aws-cdk.aws-secretsmanager>=1.56.0, <2.0.0",
        "aws-cdk.core>=1.56.0, <2.0.0",
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
