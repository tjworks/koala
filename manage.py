#!/usr/bin/env python
import os
import sys

#we can change this one!
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koala.settings")
    #commnet in the midddle from master
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
