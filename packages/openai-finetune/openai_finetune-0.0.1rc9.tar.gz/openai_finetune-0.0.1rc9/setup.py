import os

from setuptools import find_packages, setup

version_contents = {}
with open(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "openai_finetune/version.py"
    )
) as f:
    exec(f.read(), version_contents)

setup(
    name="openai_finetune",
    description="Python client library for the OpenAI Fine-tuning API",
    version=version_contents["VERSION"],
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
        "numpy",
        "transformers < 3.0.0",
        "blobfile>=0.11.0",
        "openai>=0.2.3",
    ],
    python_requires=">=3.6",
    scripts=["bin/openai-ft"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    # package_data={"openai": ["data/ca-certificates.crt"]},
    author="OpenAI",
    author_email="support@openai.com",
    url="https://github.com/openai/openai-finetune",
)
