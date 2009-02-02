# -*- coding: utf-8 -*-

# daemon/lockfile.py
#
# Copyright © 2008–2009 Ben Finney <ben@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the Python Software Foundation License, version 2 or
# later as published by the Python Software Foundation.
# No warranty expressed or implied. See the file LICENSE.PSF-2 for details.

""" Lockfile behaviour implemented via Unix PID files.
    """

import os
import sys
import errno


def pidfile_exists(pidfile_name):
    """ Return True if the named PID file exists on the filesystem.
        """
    result = os.path.exists(pidfile_name)
    return result


def read_pid_from_pidfile(pidfile_name):
    """ Read the PID recorded in the named PID file.

        Read and return the numeric PID recorded as text in the named
        PID file. If the PID file cannot be read, return ``None``.

        """
    try:
        pidfile = file(pidfile_name, 'r')
        pid = int(pidfile.read().strip())
        pidfile.close()
    except IOError:
        pid = None

    return pid


def abort_if_existing_pidfile(pidfile_name):
    """ Exit the program if the named PID file exists.

        The presence of the specified PID file indicates another
        instance of this daemon program is already running, so we exit
        this program in that case.

        """
    if pidfile_exists(pidfile_name):
        mess = (
            "Aborting: PID file '%(pidfile_name)s' exists.\n"
            ) % vars()
        sys.stderr.write(mess)
        sys.exit(1)


def abort_if_no_existing_pidfile(pidfile_name):
    """ Exit the program if the named PID file does not exist.

        The specified PID file should be created when we start and
        should continue to be readable while the daemon runs, so
        failure indicates a fatal error.

        """
    if not pidfile_exists(pidfile_name):
        mess = (
            "Aborting: could not read PID file '%(pidfile_name)s'.\n"
            ) % vars()
        sys.stderr.write(mess)
        sys.exit(1)


def write_pid_to_pidfile(pidfile_name):
    """ Write the PID in the named PID file.

        Get the numeric process ID (“PID”) of the current process
        and write it to the named file as a line of text.

        """
    pidfile = file(pidfile_name, 'w')

    pid = os.getpid()
    line = "%(pid)d\n" % vars()
    pidfile.write(line)


def remove_existing_pidfile(pidfile_name):
    """ Remove the named PID file if it exists.

        Removing a PID file that doesn't already exist puts us in the
        desired state, so we ignore the condition if the file does not
        exist.

        """
    try:
        os.remove(pidfile_name)
    except OSError, exc:
        if exc.errno == errno.ENOENT:
            pass
        else:
            raise