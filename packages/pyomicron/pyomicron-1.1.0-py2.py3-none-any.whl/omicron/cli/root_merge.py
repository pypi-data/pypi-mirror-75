#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Louisiana State University (2016, 2017)
#               Cardiff University (2017-2020)
#
# This file is part of PyOmicron.
#
# PyOmicron is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyOmicron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyOmicron.  If not, see <http://www.gnu.org/licenses/>.

"""Merge multiple Omicron ROOT files into one
"""

import os.path
import argparse

from omicron import (io, __version__)

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


def create_parser():
    """Create a command-line parser for this entry point
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=__version__,
    )
    parser.add_argument(
        'filename',
        nargs='+',
        help='file to merge',
    )
    parser.add_argument(
        'output',
        help='output file name',
    )
    parser.add_argument(
        '-d',
        '--remove-input',
        action='store_true',
        default=False,
        help='remove input files after writing output',
    )
    parser.add_argument(
        '-s',
        '--strict',
        action='store_true',
        default=False,
        help='only merge contiguous data',
    )
    return parser


def main(args=None):
    """Run the merge tool
    """
    parser = create_parser()
    args = parser.parse_args(args=args)
    io.merge_root_files(args.filename, args.output, strict=args.strict)

    # remove input files
    if args.remove_input:
        for f in args.filename:
            if os.path.samefile(f, args.output):
                continue
            os.remove(f)


if __name__ == "__main__":
    main()
