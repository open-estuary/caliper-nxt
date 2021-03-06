#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#

import os
import tempfile

from avocado import Test
from avocado import main
from avocado.utils import archive
from avocado.utils import process
from avocado.utils import build
from avocado.utils import distro
from avocado.utils.software_manager import SoftwareManager

class Scimark(Test):

    def setUp(self):
        smm = SoftwareManager()
        if not smm.check_installed("gcc") and not smm.install("gcc"):
            self.error("Gcc is needed for the test to be run")
        data_dir = os.path.abspath(self.datadir)
        self.srcdir = os.path.join(data_dir, 'source_code')

        os.chdir(self.srcdir)
        d_distro = distro.detect()
        arch = d_distro.arch
        if arch == 'aarch32':
            build.make(self.srcdir, extra_args='CC=gcc \'CFLAGS=-mfloat-abi=hard -mfpu=vfpv4 -mcpu=cortex-a15\' ')
        elif arch == 'aarch64':
            build.make(self.srcdir, extra_args='CC=gcc')
        elif arch == 'x86_64':
            build.make(self.srcdir, extra_args='CC=gcc')
        else:
            build.make(self.srcdir, extra_args='')

        exec_path = os.path.join(self.srcdir, 'bin')
        if not os.path.exists(exec_path):
            try:
                os.mkdir(exec_path)
            except:
                print "Failed to create bin folder"
                return -1

        process.run('cp scimark2 ./bin/scimark2')
        process.run('make CC=$GCC clean')

    def test(self):

        path = os.path.join(self.srcdir, 'bin')
        os.chdir(path)

        start_log = "%%%%%%         scimark2 test start       %%%%%% \n"
        echo_cmd = "echo '%s' " % start_log
        process.run(echo_cmd)
        echo_cmd = "echo '<<BEGIN TEST>>>'"
        process.run(echo_cmd)
        try:
            process.run('./scimark2')
        except Exception:
            status = 'FAIL'
        else:
            status = 'PASS'
        echo_cmd = "echo '[status]: %s' " % status
        process.run(echo_cmd)
        echo_cmd = "echo '<<<END>>>'"
        process.run(echo_cmd)
        echo_cmd = "echo '%%%%%% test_end %%%%%%'"
        process.run(echo_cmd)
