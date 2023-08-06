#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from pathlib import Path
from sys import exit, stderr

from ycontract import disable_contract

from exclock import __VERSION__
from exclock.mains.play_clock_main import main as play_clock_main
from exclock.mains.show_list_main import main as show_list_main
from exclock.mains.specified_time_main import main as specified_time_main
from exclock.util import executable


def get_option_parser():
    usage = "exclock [options] {clock-filename}"
    parser = OptionParser(usage=usage, version=__VERSION__)
    parser.add_option(
        "-l",
        "--list",
        action="store_true",
        default=False,
        dest="show_list",
        help="show clock names in your PC and exit",
    )
    parser.add_option(
        "-t",
        "--time",
        dest="time",
        action="store",
        help="Time which spends until or to specified",
    )
    parser.add_option(
        "-r",
        "--ring-filename",
        dest="ring_filename",
        action="store",
        help="filename which is used for alarm",
    )
    parser.add_option(
        "--trace",
        "--traceback",
        default=False,
        action="store_true",
        dest="with_traceback",
        help="show traceback",
    )

    return parser


def main() -> None:
    if not (Path(__file__).parent.parent / ".git").exists():
        disable_contract()

    if not executable("xmessage") and not executable("terminal-notifier"):
        print("both xmessage and terminal-notifier not found.", file=stderr)
        exit(1)

    if not executable("mplayer"):
        print("mplayer not found.", file=stderr)
        exit(1)

    opt, args = get_option_parser().parse_args()

    if opt.show_list:
        show_list_main()
    elif opt.time is not None:
        specified_time_main(opt, args)
    else:
        play_clock_main(opt, args)


if __name__ == '__main__':
    main()
