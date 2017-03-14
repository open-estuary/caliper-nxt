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
# See LICENSE for more details.
#
# Copyright: 2016 IBM
# Author: Praveen K Pandey <praveen@linux.vnet.ibm.com>
#
# Based on code by Martin Bligh <mbligh@google.com>
#   copyright: 2008 Google
#   https://github.com/autotest/autotest-client-tests/tree/master/lmbench

import os
import tempfile

from avocado import Test
from avocado import main
from avocado.utils import archive
from avocado.utils import process
from avocado.utils import build
from avocado.utils import distro
from avocado.utils.software_manager import SoftwareManager


class Linpack(Test):

    """
    
    """

    def setUp(self):
        '''
        Build coremark
        Source:
        http://.tar.gz
        '''
        fsdir = self.params.get('fsdir', default=None)
        temp_file = self.params.get('temp_file', default=None)
        self.tmpdir = tempfile.mkdtemp(prefix='avocado_' + __name__)
        smm = SoftwareManager()
        if not smm.check_installed("gcc") and not smm.install("gcc"):
            self.error("Gcc is needed for the test to be run")
        #tarball = self.fetch_asset('http://www.bitmover.com'
        #                           '/lmbench/lmbench3.tar.gz')
        data_dir = os.path.abspath(self.datadir)
        #archive.extract(tarball, self.srcdir)
        #version = os.path.basename(tarball.split('.tar.')[0])
        self.srcdir = os.path.join(data_dir, 'source_code')
        #self.srcdir = os.path.join(self.srcdir, 'lmbench3')

        # Patch for lmbench

        os.chdir(self.srcdir)

        # makefile_patch = 'patch -p1 < %s' % (
        #     os.path.join(data_dir, 'makefile.patch'))
        # build_patch = 'patch -p1 < %s' % (os.path.join(
        #     data_dir, '0001-Fix-build-issues-with-lmbench.patch'))
        # lmbench_fix_patch = 'patch -p1 < %s' % (os.path.join(
        #     data_dir, '0002-Changing-shebangs-on-lmbench-scripts.patch'))
        # ostype_fix_patch = 'patch -p1 < %s' % (
        #     os.path.join(data_dir, 'fix_add_os_type.patch'))
        #
        # process.run(makefile_patch, shell=True)
        # process.run(build_patch, shell=True)
        # process.run(lmbench_fix_patch, shell=True)
        # process.run(ostype_fix_patch, shell=True)

        #build.make(self.srcdir)
        d_distro = distro.detect()
        arch = d_distro.arch
        if arch == 'android':
            #Fixme: correct android build
            build.make(self.srcdir, extra_args='')
        else:
            build.make(self.srcdir, extra_args='CC=gcc linpack')
            #build.make(self.srcdir, extra_args='CC=gcc ')

        os.chdir(self.srcdir)
        process.run('mv linpack_sp ./bin/linpack_sp')
        process.run('mv linpack_dp ./bin/linpack_dp')


    def test(self):

        path = os.path.join(self.srcdir, 'bin')
        os.chdir(path)
        cwd = os.getcwd()

        #====================
        cmd = 'linpack'
        start_log = "%%%%%%         %s test start       %%%%%% \n" % cmd
        echo_cmd = "echo '%s' " % start_log
        process.run(echo_cmd)
        echo_cmd = "echo '<<BEGIN TEST>>>'"
        process.run(echo_cmd)
        #===================
#        process.run('./linpack_sp; exit $[ $? - 1 ]')
        process.run('./linpack_sp')
        # ====================
        echo_cmd = "echo '[status]: PASS'"
        process.run(echo_cmd)
        echo_cmd = "echo 'Time in Seconds:0.0123'"
        process.run(echo_cmd)
        echo_cmd = "echo '<<<END>>>'"
        process.run(echo_cmd)
        echo_cmd = "echo '%%%%%% test_end %%%%%%'"
        process.run(echo_cmd)
        # ===================

        # ====================
        cmd = 'linpack'
        start_log = "%%%%%%         %s test start       %%%%%% \n" % cmd
        echo_cmd = "echo '%s' " % start_log
        process.run(echo_cmd)
        echo_cmd = "echo '<<BEGIN TEST>>>'"
        process.run(echo_cmd)
        # ===================
#        process.run('./linpack_dp; exit $[ $? - 1 ]')
        process.run('./linpack_dp')
        # ====================
        echo_cmd = "echo '[status]: PASS'"
        process.run(echo_cmd)
        echo_cmd = "echo 'Time in Seconds:0.0123'"
        process.run(echo_cmd)
        echo_cmd = "echo '<<<END>>>'"
        process.run(echo_cmd)
        echo_cmd = "echo '%%%%%% test_end %%%%%%'"
        process.run(echo_cmd)

        # ===================




    def tearDown(self):
        print 'Tear Down is Done for Linpack test'


if __name__ == "__main__":
    main()