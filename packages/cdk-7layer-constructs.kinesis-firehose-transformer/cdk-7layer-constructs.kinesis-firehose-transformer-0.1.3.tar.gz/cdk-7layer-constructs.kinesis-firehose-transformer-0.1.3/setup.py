import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-7layer-constructs.kinesis-firehose-transformer",
    "version": "0.1.3",
    "description": "Kinesis Firehose Transformer to automatically convert JSON data sent to Firehose to Parquet",
    "license": "Apache-2.0",
    "url": "https://github.com/randyridgley/cdk-7layer-constructs",
    "long_description_content_type": "text/markdown",
    "author": "Randy Ridgley",
    "project_urls": {
        "Source": "https://github.com/randyridgley/cdk-7layer-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_7layer_constructs.kinesis_firehose_transformer",
        "cdk_7layer_constructs.kinesis_firehose_transformer._jsii"
    ],
    "package_data": {
        "cdk_7layer_constructs.kinesis_firehose_transformer._jsii": [
            "kinesis-firehose-transformer@0.1.3.jsii.tgz"
        ],
        "cdk_7layer_constructs.kinesis_firehose_transformer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-glue>=1.56.0, <2.0.0",
        "aws-cdk.aws-iam>=1.56.0, <2.0.0",
        "aws-cdk.aws-kinesisfirehose>=1.56.0, <2.0.0",
        "aws-cdk.aws-kms>=1.56.0, <2.0.0",
        "aws-cdk.aws-logs>=1.56.0, <2.0.0",
        "aws-cdk.aws-s3>=1.56.0, <2.0.0",
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
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
