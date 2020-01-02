// ----------------------------------------------------------------------
// |
// |  FileAttributes.in.h
// |
// |  David Brownell <db@DavidBrownell.com>
// |      2019-10-16 10:46:03
// |
// ----------------------------------------------------------------------
// |
// |  Copyright David Brownell 2019-20
// |  Distributed under the Boost Software License, Version 1.0. See
// |  accompanying file LICENSE_1_0.txt or copy at
// |  http://www.boost.org/LICENSE_1_0.txt.
// |
// ----------------------------------------------------------------------
#pragma once

// This code is based on code by halex2005, available at https://raw.githubusercontent.com/halex2005/CMakeHelpers/master/VersionInfo.in,
// which is distributed under the MIT license (https://github.com/halex2005/CMakeHelpers/blob/master/LICENSE).

#ifndef PRODUCT_VERSION_MAJOR
#   define PRODUCT_VERSION_MAJOR            @PRODUCT_VERSION_MAJOR@
#endif

#ifndef PRODUCT_VERSION_MINOR
#   define PRODUCT_VERSION_MINOR            @PRODUCT_VERSION_MINOR@
#endif

#ifndef PRODUCT_VERSION_PATCH
#   define PRODUCT_VERSION_PATCH            @PRODUCT_VERSION_PATCH@
#endif

#ifndef PRODUCT_VERSION_SUFFIX
#   define PRODUCT_VERSION_SUFFIX           "@PRODUCT_VERSION_SUFFIX@"
#endif

#ifndef FILE_VERSION_MAJOR
#   define FILE_VERSION_MAJOR               @PRODUCT_VERSION_MAJOR@
#endif

#ifndef FILE_VERSION_MINOR
#   define FILE_VERSION_MINOR               @PRODUCT_VERSION_MINOR@
#endif

#ifndef FILE_VERSION_PATCH
#   define FILE_VERSION_PATCH               @PRODUCT_VERSION_PATCH@
#endif

#ifndef FILE_VERSION_SUFFIX
#   define FILE_VERSION_SUFFIX              "@PRODUCT_VERSION_SUFFIX@"
#endif

#ifndef __TO_STRING
#   define __TO_STRING_IMPL(x)              #x
#   define __TO_STRING(x)                   __TO_STRING_IMPL(x)
#endif

#define PRODUCT_VERSION_MAJOR_MINOR_STR                 __TO_STRING(PRODUCT_VERSION_MAJOR) "." __TO_STRING(PRODUCT_VERSION_MINOR)
#define PRODUCT_VERSION_MAJOR_MINOR_PATCH_STR           PRODUCT_VERSION_MAJOR_MINOR_STR "." __TO_STRING(PRODUCT_VERSION_PATCH)
#define PRODUCT_VERSION_FULL_STR                        PRODUCT_VERSION_MAJOR_MINOR_PATCH_STR PRODUCT_VERSION_SUFFIX
#define PRODUCT_VERSION_RESOURCE                        PRODUCT_VERSION_MAJOR,PRODUCT_VERSION_MINOR,PRODUCT_VERSION_PATCH,0
#define PRODUCT_VERSION_RESOURCE_STR                    PRODUCT_VERSION_FULL_STR "\0"

#define FILE_VERSION_MAJOR_MINOR_STR        __TO_STRING(FILE_VERSION_MAJOR) "." __TO_STRING(FILE_VERSION_MINOR)
#define FILE_VERSION_MAJOR_MINOR_PATCH_STR  FILE_VERSION_MAJOR_MINOR_STR "." __TO_STRING(FILE_VERSION_PATCH)
#define FILE_VERSION_FULL_STR               FILE_VERSION_MAJOR_MINOR_PATCH_STR FILE_VERSION_SUFFIX
#define FILE_VERSION_RESOURCE               FILE_VERSION_MAJOR,FILE_VERSION_MINOR,FILE_VERSION_PATCH,0
#define FILE_VERSION_RESOURCE_STR           FILE_VERSION_FULL_STR "\0"

#ifndef PRODUCT_ICON
#   define PRODUCT_ICON                     "@PRODUCT_ICON@"
#endif

#ifndef PRODUCT_COMMENTS
#   define PRODUCT_COMMENTS                 "@PRODUCT_COMMENTS@\0"
#endif

#ifndef PRODUCT_COMPANY_NAME
#   define PRODUCT_COMPANY_NAME             "@PRODUCT_COMPANY_NAME@\0"
#endif

#ifndef PRODUCT_COPYRIGHT
#   define PRODUCT_COPYRIGHT                "@PRODUCT_COPYRIGHT@\0"
#endif

#ifndef PRODUCT_FILE_DESCRIPTION
#   define PRODUCT_FILE_DESCRIPTION         "@PRODUCT_FILE_DESCRIPTION@\0"
#endif

#ifndef PRODUCT_INTERNAL_NAME
#   define PRODUCT_INTERNAL_NAME            "@PRODUCT_NAME@\0"
#endif

#ifndef PRODUCT_ORIGINAL_FILENAME
#   define PRODUCT_ORIGINAL_FILENAME        "@PRODUCT_ORIGINAL_FILENAME@\0"
#endif

#ifndef PRODUCT_BUNDLE
#   define PRODUCT_BUNDLE                   "@PRODUCT_BUNDLE@\0"
#endif
