#!/bin/sh

autoreconf --force --install --symlink \
&& aclocal -I m4 \
&& automake --add-missing \
&& autoconf


