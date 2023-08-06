from __future__ import division, print_function, absolute_import
from distutils.core import setup, Extension
import os


version = "0.1.2"

with open("README.md", "r") as file:
    long_description = file.read()


def main():
    print("setting up src_manip3 version: " + version)

    setup(name="src_manip3",
          version=version,
          description="Python - C interface for manipulating source code, but faster.",
          long_description=long_description,
          long_description_content_type="text/markdown",
          author="skyzip",
          author_email="skyzip96@gmail.com",
          url="https://gitlab.com/Skyzip/src_manip3",
          ext_modules=[
              Extension("src_manip.comment_remover.comment_remover", [
                  "comment_remover/comment_remover.c",
                  "comment_remover/_comment_remover.c"
              ]),
              Extension("src_manip.code_cleaner.code_cleaner", [
                  "code_cleaner/code_cleaner.c",
                  "code_cleaner/_code_cleaner.c"
              ])
          ],
          packages=[
              "src_manip",
              "src_manip.comment_remover",
              "src_manip.code_cleaner"
          ],
          package_dir={
              "src_manip": ".",
              "src_manip.comment_remover": "comment_remover",
              "src_manip.code_cleaner": "code_cleaner"
          },
          package_data={
              "src_manip": ["__init__.py", "README.md"],
              "src_manip.comment_remover": [
                  "__init__.py",
                  "js_comment_remover.py",
                  "comment_remover.h"
              ],
              "src_manip.code_cleaner": [
                  "__init__.py",
                  "code_cleaner.py",
                  "code_cleaner.h"
              ]
          },
          license="GPL",
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
