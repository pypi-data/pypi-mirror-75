"""
    Init File for sitecheck

    Sets os.environ['ROOT_DIR'] and than inserts it into path
"""
import os
import sys

os.environ['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ['ROOT_DIR'])
