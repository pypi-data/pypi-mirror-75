derivatives = [ "sdist", "build", "install" ]

from skbuild.command.sdist import sdist as _skbuild_command_sdist
from skbuild.command.bdist import bdist as _skbuild_command_bdist
from skbuild.command.bdist_wheel import bdist_wheel as _skbuild_command_bdist_wheel
from skbuild.command.build import bdist as _skbuild_command_build
from skbuild.command.build_ext import bdist as _skbuild_command_build_ext
from skbuild.command.build_py import bdist as _skbuild_command_build_py
from skbuild.command.clean import bdist as _skbuild_command_clean


_, name, is_pkg = list(pkgutil.iter_modules(setuptools.__path__))[5]
