import io
import pathlib

from setuptools import setup, find_packages

version_data = {}
version_file = pathlib.Path(__file__).parent / 'dbrdemo/version.py'
with version_file.open('r') as f:
    exec(f.read(), version_data)

setup(name="dbrdemo",
      version=version_data['__version__'],
      packages=find_packages(exclude=["tests", "*tests.*", "*tests"]),
      python_requires=">=3.10",
      install_requires=["databricks-labs-blueprint==0.4.3", "databricks-sdk==0.23.0"],
      entry_points = {
        'console_scripts': [
            'dbrdemo-foobar=dbrdemo.cli:cli_foobar'
        ]
      },
      extras_require={"dev": ["databricks-connect==14.3.1", "pytest==7.4.3", "pytest-cov==4.1.0", "pytest-xdist==3.5.0", "pytest-mock",
                              "yapf", "pycodestyle", "autoflake", "isort", "wheel",
                              "pytest-approvaltests==0.2.4", "pylint==3.0.3", "tabulate==0.9.0" ]
                        },
      author="Grzegorz Rusin",
      author_email="grzegorz.rusin@databricks.com",
      description="Databricks Demo VSCode Project",
      long_description=io.open("README.md", encoding="utf-8").read(),
      long_description_content_type='text/markdown',
      keywords="dbr demo vscode project",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Operating System :: OS Independent"])
