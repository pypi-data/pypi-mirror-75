import setuptools
import sys
import os

with open("README.md", "r") as fh:
  long_description = fh.read()

if sys.platform == 'linux':
  mamba_script = os.path.join("./bin/linux/mamba")
elif sys.platform == 'darwin':
  mamba_script = os.path.join("./bin/osx/mamba")
else:
  mamba_script = 'mamba.py'

setuptools.setup(
  name='akc-mamba',
  version='0.0.2',
  # scripts=[mamba_script],
  author="akaChain",
  author_email="admin@akachain.io",
  description="A production ready, complete experience in deploying a Hyperledger Fabric",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Akachain/akc-mamba",
  packages=setuptools.find_packages(),
  package_data={
    'mamba': [mamba_script],
  },
  # include_package_data=True,
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
