#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "pyopentreplib" for configuration "Debug"
set_property(TARGET pyopentreplib APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(pyopentreplib PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pyopentrep/pyopentrep.0.07.7.so"
  IMPORTED_SONAME_DEBUG "@rpath/pyopentrep.0.07.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS pyopentreplib )
list(APPEND _IMPORT_CHECK_FILES_FOR_pyopentreplib "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/python3.8/site-packages/pyopentrep/pyopentrep.0.07.7.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
