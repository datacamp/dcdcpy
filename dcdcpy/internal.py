#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Non-user-facing functionality.
"""

from datetime import datetime

def is_yyyymmdd(x):
    try:
        return bool(datetime.strptime(x, "%Y-%m-%d"))
    except ValueError:
        return False
    except TypeError:
        return False