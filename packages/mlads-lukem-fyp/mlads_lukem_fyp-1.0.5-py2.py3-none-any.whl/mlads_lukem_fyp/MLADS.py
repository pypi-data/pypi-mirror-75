#!/usr/bin/env python

# Imports
from mlads_lukem_fyp import ui
import os
from os.path import split, dirname, abspath, join, exists

HOME = split(dirname(__file__))[0]
CSVDIR = abspath(join(HOME, 'csvs'))
SAVEDIR = abspath(join(HOME, 'model'))
DBDIR = abspath(join(HOME, 'sqlite'))
CONFIG_FILE = abspath(join(HOME, 'mlads.cfg'))
README_FILE = abspath(join(HOME, 'README.txt'))


def pre_checks():
    """
    Check appropriate directories and files exist before running the program.
    """
    default_config = ["# Alerting Credentials:\nusername=\npassword=\napikey=\n\n",
                      "# KNN attributes\nneighbours=5\nweights=uniform\n\n",
                      "# Database location\ndatabase=mlads_db.db"]

    if not exists(CSVDIR):
        os.mkdir(CSVDIR)
    if not exists(SAVEDIR):
        os.mkdir(SAVEDIR)
    if not exists(DBDIR):
        os.mkdir(DBDIR)

    if not exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'w') as cfg:
                for line in default_config:
                    cfg.write(line)
        except IOError:
            pass

    if not exists(README_FILE):
        try:
            with open(README_FILE, 'w') as rdme:
                rdme.write("MLADS Final Year Project")
        except IOError:
            pass


def start_mlads():
    """
    Start the program.
    """
    pre_checks()
    ui.GUI()


if __name__ == "__main__":
    start_mlads()
