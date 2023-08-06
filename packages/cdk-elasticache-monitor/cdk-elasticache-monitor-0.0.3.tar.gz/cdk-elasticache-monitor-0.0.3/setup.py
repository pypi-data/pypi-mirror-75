import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-elasticache-monitor",
    "version": "0.0.3",
    "description": "ElasticacheAutoMonitor allows you to send email, sms, slack, or trigger aws lambda when an alarm occurs.",
    "license": "Apache-2.0",
    "url": "https://github.com/jialechan/cdk-elasticache-monitor.git",
    "long_description_content_type": "text/markdown",
    "author": "Jiale Chan<jiale.chan@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/jialechan/cdk-elasticache-monitor.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk-elasticache-monitor",
        "cdk-elasticache-monitor._jsii"
    ],
    "package_data": {
        "cdk-elasticache-monitor._jsii": [
            "cdk-elasticache-monitor@0.0.3.jsii.tgz"
        ],
        "cdk-elasticache-monitor": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudwatch>=1.55.0, <2.0.0",
        "aws-cdk.aws-cloudwatch-actions>=1.55.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.55.0, <2.0.0",
        "aws-cdk.aws-sns>=1.55.0, <2.0.0",
        "aws-cdk.aws-sns-subscriptions>=1.55.0, <2.0.0",
        "aws-cdk.core>=1.55.0, <2.0.0",
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
