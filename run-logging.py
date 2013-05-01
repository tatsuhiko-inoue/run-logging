#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import with_statement

import sys
import subprocess
import os
import os.path
import time
import getopt
import datetime
import subprocess

def usage(f=sys.stdout):
    print("""usage:
    %s [-d logdir] [-s] command [args...]

 -d logdir       the directory where this create log file.
 -s              command is script. This appends first argument to log filename.
 """ % sys.argv[0], file=f)

def die(msg):
    print("%s: %s" % (os.path.basename(sys.argv[0]), msg), file=sys.stderr)
    usage(sys.stderr)
    sys.exit(1)

def main():
    isscript = False
    logdir   = "."
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:sh", [])
    except getopt.GetoptError as err:
        die(str(err))

    for o, a in opts:
        if o == '-d':
            logdir = a
        elif o == '-s':
            isscript = True
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    if len(args) < 1:
        die('no spawned command.')

    cmd = args[0]
    if isscript and len(args) >= 2:
        cmd = '%s-%s' % (args[0], args[1])

    if not os.path.isdir(logdir):
        die('%s is not directory.' % logdir)

    now = datetime.datetime.now()
    logfilename = '%s-%s.%06d-%d.log' % (cmd, now.strftime('%Y-%m-%d-%H%M%S'), now.microsecond, os.getpid())
    logfilename = os.path.join(logdir, logfilename)

    with open(logfilename, 'w') as f:
        print('# command: %s' % " ".join(args), file=f)
        print('# date: %s' % now, file=f)
        print('# wd: %s' % os.getcwd(), file=f)
        f.flush()

        begin = time.time()
        p = subprocess.Popen(args, stdout=f, stderr=f)
        p.wait()
        end = time.time()

        print('# status: %d' % p.returncode, file=f)
        print('# realtime: %s' % (end - begin), file=f)

    sys.exit(p.returncode)

if __name__ == '__main__':
    main()
