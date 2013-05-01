==============
run-logging.py
==============

This script executes the specified command, logging stdout and stderr 
to the suitable file.

usage::

    ./run-logging.py [-d logdir] [-s] command [args...]

-d logdir       the directory where this create log file.
-s              command is script. This appends first argument to log filename.
