#!/bin/bash
# ----------------------------------------------------------------------
# |
# |  build_linux.sh
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-09-06 17:58:02
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-22
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
set -e                                      # Exit on error
set -x                                      # statements

# Builds graphviz
#
#   Docker command:
#       [Linux host]    docker run -it --rm -v `pwd`:/local centos:6.8 bash /local/build_linux.sh 2.38.0
#       [Windows host]  docker run -it --rm -v %cd%:/local centos:6.8 bash /local/build_linux.sh 2.38.0

if [[ "$1" == "2.38.0" ]]
then
    VERSION=2.38.0
else
    echo "Invalid graphviz version; expected (2.38.0)"
    exit
fi

InstallEPEL() {
    rpm -Uvh http://mirrors.kernel.org/fedora-epel/6/i386/epel-release-6-8.noarch.rpm
}

UpdateEnvironment() {
    set +x
    echo "# ----------------------------------------------------------------------"
    echo "# |"
    echo "# |  Updating Development Environment"
    echo "# |"
    echo "# ----------------------------------------------------------------------"
    set -x

    yum groupinstall -y 'Development Tools'

    yum install -y \
        freetype-2.3.11 \
        fontconfig-2.8.0 \
        freeglut-2.6.0 \
        gdk-pixbuf2-2.24.1 \
        libjpeg-turbo-1.2.1 \
        libpng-1.2.49 \
        librsvg2-2.26.0 \
        pango-1.28.1 \
        p7zip
}

BuildGraphviz() {
    set +x
    echo "# ----------------------------------------------------------------------"
    echo "# |"
    echo "# |  Building Graphviz"
    echo "# |"
    echo "# ----------------------------------------------------------------------"
    set -x

    tar -xf /local/v${VERSION}/graphviz-${VERSION}.tar.gz

    pushd graphviz-${VERSION}               # +src dir

    ./configure \
        --prefix=/opt/CommonCppCommon/graphviz/${VERSION} \
        --enable-perl=no \
        --enable-static \
        LDFLAGS='-Wl,-rpath,\$$ORIGIN/../lib'

    make
    make install

    popd > /dev/null                        # -src dir

    pushd /opt/CommonCppCommon/graphviz/${VERSION}      # +install dir

    [[ ! -e /local/v${VERSION}/Linux/Install.7z ]] || rm /local/v${VERSION}/Linux/Install.7z
    7za a /local/v${VERSION}/Linux/Install.7z *

    popd > /dev/null                                    # -installdir
}

[[ -d /src ]] || mkdir "/src"
pushd /src > /dev/null                      # +/src

InstallEPEL
UpdateEnvironment
BuildGraphviz

popd > /dev/null                            # -/src

set +x
echo DONE!
