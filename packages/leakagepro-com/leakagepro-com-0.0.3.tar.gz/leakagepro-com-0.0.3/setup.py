from setuptools import setup, find_packages
import os

if "GITHUB_REF" in os.environ:
      version = os.environ["GITHUB_REF"].split("/")[-1]
else:
      version = "0.0.1"

setup(name='leakagepro-com',
      version=version,
      description='python bindings for leakagePro communication',
      url='https://github.com/pieye/leakagePro-com',
      author='Markus Proeller',
      author_email='markus.proeller@pieye.org',
      license='GPLv3',
      include_package_data=True,
      install_requires=["pandas"
      ],
      packages=find_packages(),
      zip_safe=False)