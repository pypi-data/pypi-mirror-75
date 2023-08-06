import stat
import os
import sys
import shutil
from distutils.command.install_data import install_data
import pathlib
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
import struct

BITS = struct.calcsize("P") * 8
PACKAGE_NAME = "cosmotool"

class CMakeExtension(Extension):
    """
    An extension to run the cmake build

    This simply overrides the base extension class so that setuptools
    doesn't try to build your sources for you
    """

    def __init__(self, name, sources=["python/dummy.c"]):

        super().__init__(name = name, sources = sources)

        self.SOURCE_DIR = str(pathlib.Path().absolute())

class InstallCMakeLibsData(install_data):
    """
    Just a wrapper to get the install data into the egg-info

    Listing the installed files in the egg-info guarantees that
    all of the package files will be uninstalled when the user
    uninstalls your package through pip
    """

    def run(self):
        """
        Outfiles are the libraries that were built using cmake
        """

        # There seems to be no other way to do this; I tried listing the
        # libraries during the execution of the InstallCMakeLibs.run() but
        # setuptools never tracked them, seems like setuptools wants to
        # track the libraries through package data more than anything...
        # help would be appriciated

        self.outfiles = self.distribution.data_files

class InstallCMakeLibs(install_lib):
    """
    Get the libraries from the parent distribution, use those as the outfiles

    Skip building anything; everything is already built, forward libraries to
    the installation step
    """

    def run(self):
        """
        Copy libraries from the bin directory and place them as appropriate
        """

        self.announce("Moving library files", level=3)
#        print(self.build_temp)
#
#        self.distribution.bin_dir = CosmoTool_extension.bin_dir
#
#        # We have already built the libraries in the previous build_ext step
#
#        self.skip_build = True
#
#        # Depending on the files that are generated from your cmake
#        # build chain, you may need to change the below code, such that
#        # your files are moved to the appropriate location when the installation
#        # is run
#
#        libs = [os.path.join(bin_dir, _lib) for _lib in 
#                os.listdir(bin_dir) if 
#                os.path.isfile(os.path.join(bin_dir, _lib)) and 
#                os.path.splitext(_lib)[1] in [".dll", ".so"]
#                and not (_lib.startswith("python") or _lib.startswith(PACKAGE_NAME))]
#
#        for lib in libs:
#
#            shutil.move(lib, os.path.join(self.build_dir,
#                                          os.path.basename(lib)))
#
#        # Mark the libs for installation, adding them to 
#        # distribution.data_files seems to ensure that setuptools' record 
#        # writer appends them to installed-files.txt in the package's egg-info
#        #
#        # Also tried adding the libraries to the distribution.libraries list, 
#        # but that never seemed to add them to the installed-files.txt in the 
#        # egg-info, and the online recommendation seems to be adding libraries 
#        # into eager_resources in the call to setup(), which I think puts them 
#        # in data_files anyways. 
#        # 
#        # What is the best way?
#
#        # These are the additional installation files that should be
#        # included in the package, but are resultant of the cmake build
#        # step; depending on the files that are generated from your cmake
#        # build chain, you may need to modify the below code
#
#        self.distribution.data_files = [os.path.join(self.install_dir, 
#                                                     os.path.basename(lib))
#                                        for lib in libs]
#        print(self.distribution.data_files)
#
#        # Must be forced to run after adding the libs to data_files

        self.distribution.run_command("install_data")

        super().run()

class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
        """

        for extension in self.extensions:

            if extension.name == 'cosmotool':
                self.package = 'cosmotool'

                self.build_cmake(extension)

        super().run()

    def build_cmake(self, extension: Extension):
        """
        The steps required to build the extension
        """

        self.announce("Preparing the build environment", level=3)

        package_dir = os.path.abspath(os.path.join(self.build_lib, 'cosmotool'))


        extension.build_dir = pathlib.Path(self.build_temp)
        extension.bin_dir = str(pathlib.Path(os.path.join(extension.build_dir, 'private_install')).absolute())
        SOURCE_DIR = extension.SOURCE_DIR
        build_dir = extension.build_dir

        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        cython_code = os.path.join(str(build_dir.absolute()),'mycython')
        with open(cython_code, mode="wt") as ff:
          ff.write(f"#!{sys.executable}\n"
                    "from Cython.Compiler.Main import setuptools_main\n"
                    "setuptools_main()")
        os.chmod(cython_code, stat.S_IXUSR|stat.S_IWUSR|stat.S_IRUSR|stat.S_IRGRP)

        # Now that the necessary directories are created, build

        self.announce("Configuring cmake project", level=3)

        # Change your cmake arguments below as necessary
        # Below is just an example set of arguments for building Blender as a Python module

        self.spawn(['cmake', '-H'+SOURCE_DIR, '-B'+self.build_temp,
                    '-DENABLE_OPENMP=ON','-DINTERNAL_BOOST=ON','-DINTERNAL_EIGEN=ON',
                    '-DINTERNAL_HDF5=ON','-DINTERNAL_NETCDF=ON',
                    '-DBUILD_PYTHON=ON', '-DINSTALL_PYTHON_LOCAL=OFF',
                    '-DCOSMOTOOL_PYTHON_PACKAGING=ON',
                    f"-DCYTHON={cython_code}",
                    f"-DPYTHON_SITE_PACKAGES={build_dir.absolute()}/private_install",
                    f"-DPYTHON_EXECUTABLE={sys.executable}"])


        self.announce("Building binaries", level=3)

        self.spawn(["cmake", "--build", self.build_temp, "--target", "install",
                      "--config", "Release"])

        # Build finished, now copy the files into the copy directory
        # The copy directory is the parent directory of the extension (.pyd)

        self.announce("Moving built python module", level=3)

        bin_dir = extension.bin_dir
        self.distribution.bin_dir = bin_dir

        pyd_path=[]
        top_level_len = len(pathlib.Path(bin_dir).parts)
        for root,_,_pyds in os.walk(bin_dir):
          for _pyd in _pyds:
            print(_pyd)
            _pyd=os.path.join(root,_pyd)
            if os.path.isfile(_pyd):
               _pyd_top = pathlib.Path(_pyd).parts[top_level_len:]
               if  _pyd_top[0].startswith(PACKAGE_NAME):
                   if os.path.splitext(_pyd)[1] in [".pyd", ".so"] or _pyd_top[-1] == 'config.py':
                     pyd_path.append((_pyd_top,_pyd))
               

        for top,p in pyd_path:
           _,n = os.path.split(p)
           n,e = os.path.splitext(n)
           if n != "_cosmo_bispectrum" and n != 'config':
             new_p = pathlib.Path(self.get_ext_fullpath(n))
           else:
             print(f"package_dir is {package_dir}")
             new_p = pathlib.Path(os.path.join(package_dir,n+e))
           self.announce(f"Moving {p} to {new_p}", level=3)
           shutil.move(p, new_p)

CosmoTool_extension = CMakeExtension(name="cosmotool")

setup(name='cosmotool',
      version='1.0.0a6',
      packages=["cosmotool"],
      package_dir={'cosmotool': 'python/cosmotool'},
      install_requires=['numpy','cffi','numexpr','pyfftw','h5py'],
      setup_requires=['cython','cffi','numpy','numexpr'],
      ext_modules=[CosmoTool_extension],
      description='A small cosmotool box of useful functions',
      long_description=open("./README.md", 'r').read(),
      long_description_content_type="text/markdown",
      keywords="cosmology, interpolation, cmake, extension",
      classifiers=["Intended Audience :: Developers",
                   "License :: OSI Approved :: "
                   "GNU Lesser General Public License v3 (LGPLv3)",
                   "Natural Language :: English",
                   "Programming Language :: C",
                   "Programming Language :: C++",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: Implementation :: CPython"],
      license='CeCILL-v2',
      cmdclass={
          'build_ext': BuildCMakeExt,
          'install_data': InstallCMakeLibsData,
          'install_lib': InstallCMakeLibs,
          },
      python_requires='>=3.6'
)
