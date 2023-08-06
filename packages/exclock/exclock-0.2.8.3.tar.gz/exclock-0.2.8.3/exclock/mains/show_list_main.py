#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from exclock.util import get_clock_basenames


def main(stdout=sys.stdout) -> None:
    for basename in get_clock_basenames():
        print(basename, file=stdout)
