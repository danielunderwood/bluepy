"""Python setup script for bluepy"""

from setuptools.command.build_py import build_py
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
        for cmd, path in [("git submodule update --init", ""),
                          ("./bootstrap", "./bluez"),
                          ("./configure", "./bluez"),
                          ("make -C ./bluepy clean", ""),
                          ("make -C bluepy -j1", "")]:
            print("execute " + cmd)
            msgs = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, cwd=path or os.getcwd())
    except subprocess.CalledProcessError as e:
        print("Failed to compile bluepy-helper. Exiting install.")
        print("Command was " + repr(cmd) + " in " + os.getcwd())
        print("Return code was %d" % e.returncode)
        print("Output was:\n%s" % e.output)
        sys.exit(1)

class my_build_py(build_py):
    def run(self):
        pre_install()
        build_py.run(self)

setup_cmdclass = {
    'build_py' : my_build_py,
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

setup(
    name='bluepy',
    version='1.1.3',
    description='Python module for interfacing with BLE devices through Bluez',
    author='Ian Harvey, Daniel Underwood',
    author_email='website-contact@fenditton.org, daniel.underwood13@gmail.com',
    url='https://github.com/danielunderwood/bluepy',
    keywords=['Bluetooth', 'Bluetooth Smart', 'BLE', 'Bluetooth Low Energy'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['bluepy'],
    
    package_data={
        'bluepy': ['bluepy-helper', '*.json', 'bluepy-helper.c', 'Makefile']
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

