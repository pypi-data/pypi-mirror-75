import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudcomponents.cdk-codecommit-backup",
    "version": "1.0.37",
    "description": "Backup CodeCommit repositories to S3",
    "license": "MIT",
    "url": "https://github.com/cloudcomponents/cdk-constructs",
    "long_description_content_type": "text/markdown",
    "author": "hupe1980",
    "project_urls": {
        "Source": "https://github.com/cloudcomponents/cdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudcomponents.cdk_codecommit_backup",
        "cloudcomponents.cdk_codecommit_backup._jsii"
    ],
    "package_data": {
        "cloudcomponents.cdk_codecommit_backup._jsii": [
            "cdk-codecommit-backup@1.0.37.jsii.tgz"
        ],
        "cloudcomponents.cdk_codecommit_backup": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-codebuild>=1.54.0, <2.0.0",
        "aws-cdk.aws-codecommit>=1.54.0, <2.0.0",
        "aws-cdk.aws-events>=1.54.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.54.0, <2.0.0",
        "aws-cdk.aws-iam>=1.54.0, <2.0.0",
        "aws-cdk.aws-s3>=1.54.0, <2.0.0",
        "aws-cdk.aws-s3-assets>=1.54.0, <2.0.0",
        "aws-cdk.core>=1.54.0, <2.0.0"
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
