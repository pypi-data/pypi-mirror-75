import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdktf",
    "version": "0.0.13",
    "description": "Cloud Development Kit for Terraform",
    "license": "MPL-2.0",
    "url": "https://github.com/hashicorp/terraform-cdk",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "project_urls": {
        "Source": "https://github.com/hashicorp/terraform-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf",
        "cdktf._jsii"
    ],
    "package_data": {
        "cdktf._jsii": [
            "cdktf@0.0.13.jsii.tgz"
        ],
        "cdktf": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.7.0, <2.0.0",
        "publication>=0.0.3",
        "constructs>=3.0.0, <4.0.0"
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
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
