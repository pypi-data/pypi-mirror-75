from __future__ import division, print_function, absolute_import
from distutils.core import setup
import os


version = "0.1.0"

with open("README.md", "r") as file:
    long_description = file.read()


def main():
    print("setting up bpelib version: " + version)

    setup(name="bpelib",
          version=version,
          description="Byte Pair Encoding for Natural Language Processing.",
          long_description=long_description,
          long_description_content_type="text/markdown",
          author="skyzip",
          author_email="skyzip96@gmail.com",
          url="https://gitlab.com/Skyzip/bpelib",
          packages=[
              "bpelib",
              "bpelib.bpe"
          ],
          package_dir={
              "bpelib": ".",
              "bpelib.bpe": "bpe"
          },
          package_data={
              "bpelib": ["__init__.py", "README.md"],
              "bpelib.bpe": ["__init__.py", "bpe.py"]
          },
          install_requires=[
              "numpy",
              "tqdm"
          ],
          license="MIT",
          classifiers=[
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
          ]
          )


if __name__ == '__main__':
    try:
        if os.environ.get('CI_COMMIT_TAG'):
            print("Getting CI_COMMIT_TAG.")
            version = os.environ['CI_COMMIT_TAG']
        else:
            version = os.environ['CI_JOB_ID']
            print("Getting CI_JOB_ID.")
    except KeyError:
        print("Unable to get environment variable.")
        print("Setting version manually to: " + str(version))

    main()
