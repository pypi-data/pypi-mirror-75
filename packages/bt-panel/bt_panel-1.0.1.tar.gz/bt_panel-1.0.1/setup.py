import shutil
from pkg_resources import Requirement, resource_filename
try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup,find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="bt_panel",
    packages=find_packages(),
    version='1.0.1',
    description='this project is btpanel',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zhaoheng12/bt_panel/',
    author='zhaohengping',
    author_email='18438697706@163.com',
    install_requires=[""],
    entry_points={
                  'console_scripts': [
                      'bt_panel=bt_panel.__init__:main',
                  ],
              },
    package_data={
            '': ['*.rst'],
        }

)