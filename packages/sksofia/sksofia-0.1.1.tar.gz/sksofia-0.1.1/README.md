# sksofia: a sklearn wrapper for sofia-ml

[`sofia-ml`](https://code.google.com/archive/p/sofia-ml/) was an interesting project released by [d. sculley](https://www.eecs.tufts.edu/~dsculley/), providing a number of variations on linear classification and regression models with some really cool twists that primarily boil down to how training examples are sampled. The specific motivation for packaging this up is my interest in "rank-based" optimization, targeting AUC, etc specifically.

The original library is in very highly optimized c++ and is extremely fast. This package provides a [scikit-learn classifier interface](https://scikit-learn.org/stable/modules/generated/sklearn.base.ClassifierMixin.html#sklearn.base.ClassifierMixin) to this excellent library. This functionality primarily works by writing  the sklearn numpy array inputs into temp files in the format that `sofia-ml` model consume. With `sofia-ml`,  trained, a model is written to disk, whereby this library slurps up the binary version which is stored internally as bytes. This allows for compatibility with normal python serialization. When subsequent classification is needed, this model representaton is written back out to a temp file. 

Usage:
------

The script includes a shell script (`build.sh`) that can be used to install the library into a virtualenv as well as compile the requisite `sofia-ml` binary and place it in `~/bin`. This script can be modified to suit your needs and how you will use the library. Currently, there is a version of this library in pypi, but installing via pip doesn't provide the `sofia-ml` binary which needs to be on the `$PATH`. The C++ code for `sofia-ml` is included, look at `build.sh` for pointers on how to build it.


Todo:
-----
- build with nix
- figure how to build and install `sofia-ml` with pip
- documenting usage, docstrings
