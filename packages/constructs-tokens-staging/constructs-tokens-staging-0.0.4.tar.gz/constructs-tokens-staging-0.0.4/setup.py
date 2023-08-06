import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "constructs-tokens-staging",
    "version": "0.0.4",
    "description": "constructs-tokens-staging",
    "license": "Apache-2.0",
    "url": "https://github.com/iliapolo/constructs-tokens",
    "long_description_content_type": "text/markdown",
    "author": "Eli Polonsky<eli.polonsky@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/iliapolo/constructs-tokens"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "constructs_tokens_staging",
        "constructs_tokens_staging._jsii"
    ],
    "package_data": {
        "constructs_tokens_staging._jsii": [
            "constructs-tokens-staging@0.0.4.jsii.tgz"
        ],
        "constructs_tokens_staging": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
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
