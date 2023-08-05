#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 21-06-2020 12:31:46
"""
__author__ = "lairuilin"
__email__ = "kalai850531@g.ncu.edu.tw"
__status__ = "Development"

def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `my_fancy_module` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="loggerTest",
        # _also_ in the `nbextension/` namespace
        require="loggerTest/index")]