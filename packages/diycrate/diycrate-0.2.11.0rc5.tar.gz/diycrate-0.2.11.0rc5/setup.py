import os
from itertools import chain

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(file_name):
    """
    Return the contents of the file at the file_name
    :param file_name:
    :return:
    """
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


def get_packages_from_file_name(pkg_file_name):
    with open(pkg_file_name) as f:
        packages_in_file = [item.strip() for item in f if item and item.strip()]
    return packages_in_file


package_file_names = ["./requirements.txt"]

packages = list(chain.from_iterable((get_packages_from_file_name(pkg_f_name) for pkg_f_name in package_file_names)))


setup(
    name="diycrate",
    version="0.2.11.0rc5",
    author="Jason Held",
    author_email="jasonsheld@gmail.com",
    description="box.com for linux -- unofficial, based on python SDK",
    license="MIT",
    keywords="cloud storage box.com sdk linux box",
    url="https://github.com/jheld/diycrate",
    install_requires=packages,
    scripts=['diycrate_app', ],
    packages=['diycrate', ],
    long_description='box.com for linux\n'
                     'We now support SSL (self signed cert\'s yo)!'
                     'Unfortunately, this means getting openssl, ffi,'
                     'and python dev libraries installed, beforehand.'
                     'Also, you will need redis, but I do supply that '
                     'inside the source code, so all you have to do is '
                     'run "make" and "sudo make install" on the [untar\'d] redis directory.'
                     'I have not documented explicitly how to get this thing running, yet, '
                     'so please give me time, or make an Issue on this project '
                     'to let me know someone is actually trying to use it. '
                     'If we want, I can even try packaging this up as deb and rpm to make the setup easier.',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.5',
)
