hedm-conda-recipes
==================

Conda recipes for high-energy diffraction microscopy
----------------------------------------------------
===============================================================================
This is a collection of recipes to build Conda packages for software used to
analyze high-energy diffraction microscopy data. Detailed information about
Conda packaging can be found in the
[official documentation](http://conda.pydata.org/docs/building/build.html).

In time, each of these Conda recipes could be contributed upstream and become
part of the official source code for each software package. However, many of
these software projects still use the Subversion revision control system and 
may soon migrate to the more modern and accessible git revision control system.
So for now, you build conda packages by obtaining a copy of this repository
(either a git clone, or a simple copy using github's
[download zip button](https://github.com/praxes/hedm-conda-recipes/archive/master.zip)),
open a terminal (If you are building software that requires a C compiler, on
windows you need to open a visual studio 2008 command prompt and execute
"vcvarsall.bat amd64" before changing to the hedm-conda-recipes project
directory), navigate to the hedm-conda-recipes directory, and build a Conda
package for the package in the "foo" directory by executing

```
conda build foo
```

This assumes you have installed the "conda-build" conda package.

Once Conda is finished building the package, it will report where to find the
result. You can now upload that result to anaconda.org to share it with
everyone. For example:

```
anaconda upload -u chess /path/to/foo-1.0.0.tar.bz2
```

would upload the package to the CHESS organization's collection of software
on anaconda.org. Users who have added the CHESS organization as a source of
conda packages would then be able to install the package by running

```
conda install foo
```

or upgrade using

```
conda upgrade foo
```

For more information about distributing packages via anaconda.org, see the
[official documentation](http://conda.pydata.org/docs/build_tutorials/pkgs.html?highlight=anaconda%20upload#optional-upload-packages-to-anaconda-org).
