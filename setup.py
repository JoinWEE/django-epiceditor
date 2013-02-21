import os
from os import path
from setuptools import setup
from subprocess import check_call
from distutils.command.build import build
from distutils.dir_util import copy_tree, remove_tree
from setuptools.command.develop import develop

def get_submodules_and_fix_paths():
    if path.exists('.git'):
        check_call(['rm', '-rf', 'epiceditor/static/epiceditor'])
        check_call(['git', 'reset', '--hard'])
        check_call(['git', 'submodule', 'init'])
        check_call(['git', 'submodule', 'update'])
        # Move contents of pagedown and remove .git
        dst = "epiceditor/static/epiceditor/"
        src = "epiceditor/static/epiceditor/epiceditor/"
        copy_tree(src, dst)
        remove_tree(src)

class build_with_submodules(build):
    def run(self):
        get_submodules_and_fix_paths()
        build.run(self)

class develop_with_submodules(develop):
    def run(self):
        get_submodules_and_fix_paths()
        develop.run(self)


setup(
  name = "django-epiceditor",
  version = "0.2.0",
  author = "Remi Barraquand",
  author_email = "dev@remibarraquand.com",
  url = "https://github.com/barraq/django-epiceditor",
  description = ("A django app that allows the easy addition of EpicEditor markdown editor to a django form field, whether in a custom app or the Django Admin."),
  long_description=open('README.md').read(),
  packages=['epiceditor'],
  include_package_data=True,
  install_requires=[
    "Django >= 1.3",
  ],
  license='LICENSE.txt',
  cmdclass={"build": build_with_submodules, "develop": develop_with_submodules},
)