"""Python setup script for bluepy"""

from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_ext import build_ext
from setuptools import setup
import subprocess
import shlex
import sys
import os


def pre_install():
    """
    Make sure bluez submodule is cloned, clean, and compile bluepy
    """
    try:
        print("Working dir is " + os.getcwd())
        for cmd in ["git submodule update --init",
                    "./bluez/bootstrap",
                    "./bluez/configure",
                    "make -C ./bluepy clean",
                    "make -C bluepy -j1"]:
            print("execute " + cmd)
            msgs = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("Failed to compile bluepy-helper. Exiting install.")
        print("Command was " + repr(cmd) + " in " + os.getcwd())
        print("Return code was %d" % e.returncode)
        print("Output was:\n%s" % e.output)
        sys.exit(1)

def post_install():
    """Post installation tasks"""
    pass

def setup_command(command_subclass):
    """Decorator for customizing setuptools.command subclasses"""
    orig_run = command_subclass.run
    def custom_run(self):

        pre_install()        
        orig_run(self)
        post_install()

    command_subclass.run = custom_run
    return command_subclass

@setup_command
class BluepyInstall(install):
    pass

@setup_command
class BluepyDevelop(develop):
    pass

@setup_command
class BluepyBuildExt(build_ext):
    pass

setup_cmdclass = {
    'install': BluepyInstall,
    'develop': BluepyDevelop,
    'build_ext': BluepyBuildExt,
}

# Force package to be *not* pure Python
# Discusssed at issue #158

try:
    from wheel.bdist_wheel import bdist_wheel

    class BluepyBdistWheel(bdist_wheel):
        def finalize_options(self):
            bdist_wheel.finalize_options(self)
            self.root_is_pure = False

    setup_cmdclass['bdist_wheel'] = BluepyBdistWheel
except ImportError:
    pass


setup (
    name='bluepy',
    version='1.1.2',
    description='Python module for interfacing with BLE devices through Bluez',
    author='Ian Harvey',
    author_email='website-contact@fenditton.org',
    url='https://github.com/IanHarvey/bluepy',
    download_url='https://github.com/IanHarvey/bluepy/tarball/v/1.1.2',
    keywords=[ 'Bluetooth', 'Bluetooth Smart', 'BLE', 'Bluetooth Low Energy' ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['bluepy'],
    package_data={
        'bluepy': ['bluepy-helper', '*.json', 'bluez-src.tgz', 'bluepy-helper.c', 'Makefile']
    },
    cmdclass=setup_cmdclass,
    entry_points={
        'console_scripts': [
            'thingy52=bluepy.thingy52:main',
            'sensortag=bluepy.sensortag:main',
            'blescan=bluepy.blescan:main',
        ]
    }
)



