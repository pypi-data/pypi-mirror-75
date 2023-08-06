import os
import sys

from . import TAB2


class Travis:
    def __init__(self):
        version = sys.version_info
        self.python_version = f"{version.major}.{version.minor}"

    def config(self, directory):
        filename = os.path.join(directory, ".travis.yml")
        with open(filename, "w") as f:
            f.writelines(
                [
                    "language: python\n",
                    "python:\n",
                    f"{TAB2}- {self.python_version}\n",
                    "install:\n",
                    f"{TAB2}- pip install -r requirements-dev.txt\n",
                    "script:\n",
                    f"{TAB2}- flake8\n",
                ]
            )
