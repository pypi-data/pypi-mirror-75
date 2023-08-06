#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "opentreplib" for configuration "Debug"
set_property(TARGET opentreplib APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(opentreplib PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/libopentrep.0.07.7.dylib"
  IMPORTED_SONAME_DEBUG "@rpath/libopentrep.0.07.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS opentreplib )
list(APPEND _IMPORT_CHECK_FILES_FOR_opentreplib "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/lib/libopentrep.0.07.7.dylib" )

# Import target "opentrep-indexerbin" for configuration "Debug"
set_property(TARGET opentrep-indexerbin APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(opentrep-indexerbin PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/opentrep-indexer"
  )

list(APPEND _IMPORT_CHECK_TARGETS opentrep-indexerbin )
list(APPEND _IMPORT_CHECK_FILES_FOR_opentrep-indexerbin "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/opentrep-indexer" )

# Import target "opentrep-searcherbin" for configuration "Debug"
set_property(TARGET opentrep-searcherbin APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(opentrep-searcherbin PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/opentrep-searcher"
  )

list(APPEND _IMPORT_CHECK_TARGETS opentrep-searcherbin )
list(APPEND _IMPORT_CHECK_FILES_FOR_opentrep-searcherbin "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/opentrep-searcher" )

# Import target "opentrep-dbmgrbin" for configuration "Debug"
set_property(TARGET opentrep-dbmgrbin APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(opentrep-dbmgrbin PROPERTIES
  IMPORTED_LOCATION_DEBUG "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/opentrep-dbmgr"
  )

list(APPEND _IMPORT_CHECK_TARGETS opentrep-dbmgrbin )
list(APPEND _IMPORT_CHECK_FILES_FOR_opentrep-dbmgrbin "/Users/darnaud/dev/geo/opentrep/_skbuild/macosx-10.15-x86_64-3.8/cmake-install/bin/opentrep-dbmgr" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
