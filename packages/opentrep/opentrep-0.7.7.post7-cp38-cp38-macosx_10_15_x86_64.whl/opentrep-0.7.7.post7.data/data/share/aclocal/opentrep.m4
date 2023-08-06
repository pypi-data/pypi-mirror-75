#
# Configure paths and flags for the OpenTREP library.
# Denis Arnaud <denis_arnaud at users dot sourceforge dot net>, July 2008
#
# Note: the OPENTREP library depends upon BOOST to build.
# Your configure.ac must therefore define appropriately the BOOST
# variables (i.e., BOOST_CFLAGS, BOOST_LIBS, BOOST_DATE_TIME_LIB).
#
# Variables set by this macro:
#  * OPENTREP_VERSION
#  * OPENTREP_CFLAGS
#  * OPENTREP_LIBS
#

AC_DEFUN([AM_PATH_OPENTREP],
[
AC_LANG_SAVE
AC_LANG([C++])

##
AC_ARG_WITH(opentrep,
	[ --with-opentrep=PFX Prefix where OpenTREP is installed (optional) ],
	    opentrep_dir="$withval",
	    opentrep_dir="")

  if test "x${OPENTREP_CONFIG+set}" != xset ; then
     if test "x$opentrep_dir" != x ; then
         OPENTREP_CONFIG="$opentrep_dir/bin/opentrep-config"
     fi
  fi

  AC_PATH_PROG(OPENTREP_CONFIG, opentrep-config, no)

  ## Check whether Boost flags and libraries are defined
  # General Boost compilation flags
  AC_MSG_CHECKING(for BOOST_CFLAGS environment variable)
  if test x"${BOOST_CFLAGS}" = x; then
	AC_MSG_RESULT([Warning: OpenTREP needs Boost, and the BOOST_CFLAGS environment variable does not appear to be set. It may not be a problem, though, if your Unix distribution is standard, that is, if Boost is installed in /usr. Otherwise, the OpenTREP will fail to compile.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_CFLAGS})])
  fi

  # Boost Date-Time library
  AC_MSG_CHECKING(for BOOST_DATE_TIME_LIB environment variable)
  if test x"${BOOST_DATE_TIME_LIB}" = x; then
	AC_MSG_RESULT([Warning: OpenTREP needs the Boost Date-Time library, and the BOOST_DATE_TIME_LIB environment variable does not appears to be set. The OpenTREP may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_DATE_TIME_LIB})])
  fi

  # Boost Program Options library
  AC_MSG_CHECKING(for BOOST_PROGRAM_OPTIONS_LIB environment variable)
  if test x"${BOOST_PROGRAM_OPTIONS_LIB}" = x; then
	AC_MSG_RESULT([Warning: OpenTREP needs the Boost Program Options library, and the BOOST_PROGRAM_OPTIONS_LIB environment variable does not appears to be set. The OpenTREP may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_PROGRAM_OPTIONS_LIB})])
  fi

  # Boost File System library
  AC_MSG_CHECKING(for BOOST_FILESYSTEM_LIB environment variable)
  if test x"${BOOST_FILESYSTEM_LIB}" = x; then
	AC_MSG_RESULT([Warning: OpenTREP needs the Boost Date-Time library, and the BOOST_FILESYSTEM_LIB environment variable does not appears to be set. The OpenTREP may fail to link.])
  else
	AC_MSG_RESULT([ok (set to ${BOOST_FILESYSTEM_LIB})])
  fi

  ## OpenTREP version
  min_opentrep_version=ifelse([$1], ,0.1.0,$1)
  AC_MSG_CHECKING(for OpenTREP - version >= $min_opentrep_version)
  no_opentrep=""
  if test "${OPENTREP_CONFIG}" = "no" ; then
     no_opentrep=yes
     AC_MSG_RESULT([no])
  else
     OPENTREP_VERSION=`${OPENTREP_CONFIG} --version`
     OPENTREP_CFLAGS=`${OPENTREP_CONFIG} --cflags`
     OPENTREP_CFLAGS="${BOOST_CFLAGS} ${OPENTREP_CFLAGS}"
     OPENTREP_LIBS=`${OPENTREP_CONFIG} --libs`
     OPENTREP_LIBS="${BOOST_LIBS} ${BOOST_DATE_TIME_LIB} ${OPENTREP_LIBS}"

     AC_SUBST([OPENTREP_VERSION])
     AC_SUBST([OPENTREP_CFLAGS])
     AC_SUBST([OPENTREP_LIBS])

    opentrep_major_version=`echo ${OPENTREP_VERSION} | sed 's/^\([[0-9]]*\).*/\1/'`
    if test "x${opentrep_major_version}" = "x" ; then
       opentrep_major_version=0
    fi

    opentrep_minor_version=`echo ${OPENTREP_VERSION} | \
						sed 's/^\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\).*/\2/'`
    if test "x${opentrep_minor_version}" = "x" ; then
       opentrep_minor_version=0
    fi

    opentrep_micro_version=`echo ${OPENTREP_VERSION} | \
          sed 's/^\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\)\.\{0,1\}\([[0-9]]*\).*/\3/'`
    if test "x${opentrep_micro_version}" = "x" ; then
       opentrep_micro_version=0
    fi

    ## Simple test of compilation and link
    SAVED_CPPFLAGS="${CPPFLAGS}"
    SAVED_LDFLAGS="${LDFLAGS}"
    CPPFLAGS="${CPPFLAGS} ${BOOST_CFLAGS} ${OPENTREP_CFLAGS}"
    LDFLAGS="${LDFLAGS} ${OPENTREP_LIBS}"


    AC_COMPILE_IFELSE(
		[AC_LANG_PROGRAM([[#include <opentrep/OPENTREP_Service.hpp>
				]],
				[[int i=0;]]
		)]
		,

    	[AC_MSG_RESULT([yes (${OPENTREP_VERSION})])],

	[AC_MSG_ERROR([We could not compile a simple OpenTREP example. See config.log.])]
    )

    CPPFLAGS="${SAVED_CPPFLAGS}"
    LDFLAGS="${SAVED_LDFLAGS}"

  fi

AC_LANG_RESTORE
])
