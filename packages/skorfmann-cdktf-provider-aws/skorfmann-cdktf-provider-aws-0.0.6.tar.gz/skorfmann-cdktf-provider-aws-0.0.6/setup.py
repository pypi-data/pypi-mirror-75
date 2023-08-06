import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "skorfmann-cdktf-provider-aws",
    "version": "0.0.6",
    "description": "Prebuilt AWS Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/skorfmann/cdktf-provider-aws.git",
    "long_description_content_type": "text/markdown",
    "author": "Sebastian Korfmann<sebastian@korfmann.net>",
    "project_urls": {
        "Source": "https://github.com/skorfmann/cdktf-provider-aws.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "skorfmann_cdktf_provider_aws",
        "skorfmann_cdktf_provider_aws._jsii"
    ],
    "package_data": {
        "skorfmann_cdktf_provider_aws._jsii": [
            "cdktf-provider-aws@0.0.6.jsii.tgz"
        ],
        "skorfmann_cdktf_provider_aws": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "cdktf>=0.0.13, <0.0.14",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
