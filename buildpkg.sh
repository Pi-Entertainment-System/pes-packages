#!/bin/bash

#
#    This file is part of the Pi Entertainment System (PES).
#
#    PES provides an interactive GUI for games console emulators
#    and is designed to work on the Raspberry Pi.
#
#    Copyright (C) 2020-2022 Neil Munday (neil@mundayweb.com)
#
#    PES is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PES is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PES.  If not, see <http://www.gnu.org/licenses/>.
#

function die {
	echo $1
	exit 1
}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR/packages

if [ -z $KEY ]; then
	die "KEY environment variable not set"
fi

if [ -z $1 ]; then
	die "package not given"
fi

if [ ! -f "$1/PKGBUILD" ]; then
	die "$1/PKGBUILD does not exist"
fi

cd $1
makepkg -c -C -f --sign --key $KEY
if [ $? != 0 ]; then
	die "build failed!"
fi
pkg=`ls -1 ./*.tar.xz`
mv ./*.tar.xz* $DIR/repo/

cd $DIR/repo
repo-add --sign --key $KEY pes.db.tar.gz "$pkg"

