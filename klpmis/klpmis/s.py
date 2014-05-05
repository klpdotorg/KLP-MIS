#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
PROJECT_ROOT1 = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT1,
                               os.path.pardir))
PYTHON_PATH = 'python'  # os.path.abspath(os.path.join(PROJECT_ROOT, os.path.pardir))+'/bin/python'
print PROJECT_ROOT
