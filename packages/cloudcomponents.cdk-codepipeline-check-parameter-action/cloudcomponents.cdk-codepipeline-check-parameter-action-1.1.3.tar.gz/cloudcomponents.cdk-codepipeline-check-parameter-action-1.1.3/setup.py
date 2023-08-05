import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudcomponents.cdk-codepipeline-check-parameter-action",
    "version": "1.1.3",
    "description": "Cdk component that checks if system parameters are set correctly",
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
        "cloudcomponents.cdk_codepipeline_check_parameter_action",
        "cloudcomponents.cdk_codepipeline_check_parameter_action._jsii"
    ],
    "package_data": {
        "cloudcomponents.cdk_codepipeline_check_parameter_action._jsii": [
            "cdk-codepipeline-check-parameter-action@1.1.3.jsii.tgz"
        ],
        "cloudcomponents.cdk_codepipeline_check_parameter_action": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-codepipeline>=1.54.0, <2.0.0",
        "aws-cdk.aws-codepipeline-actions>=1.54.0, <2.0.0",
        "aws-cdk.aws-iam>=1.54.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.54.0, <2.0.0",
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
