#
# Config file for the OpenTREP Python package.
# It defines the following variables:
#  OPENTREP_VERSION         - version of OpenTREP
#  OPENTREP_PY_LIBRARY_DIRS - Python library directories for OpenTrep
#  OPENTREP_PY_LIBRARIES    - Python libraries to link against
#  OPENTREP_PY_EXECUTABLES  - Python binaries/executables
#

# Tell the user project where to find OpenTREP Python libraries
set (OPENTREP_VERSION "0.07.7")
set (OPENTREP_PY_LIBRARY_DIRS "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pyopentrep")

# Library dependencies for OpenTrep (contains definitions for the OpenTREP
# IMPORTED targets)
include ("/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/share/opentrep/CMake/opentrep-python-library-depends.cmake")

# These are the OpenTREP IMPORTED targets, created by
# opentrep-python-library-depends.cmake
set (OPENTREP_PY_LIBRARIES pyopentreplib)
set (OPENTREP_PY_EXECUTABLES pyopentrep)

