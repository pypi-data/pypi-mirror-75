#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
from datetime import datetime
from os import getenv
from pathlib import Path
from sys import exit, stderr
from typing import List, Optional

from ycontract import out_contract

from exclock.sound_player import Player
from exclock.util import (
    DEFAULT_RING_FILENAME,
    convert_specific_time_to_time_delta,
    get_real_sound_filename,
    get_specific_time_from_str,
    get_time_delta_from_str,
    is_specific_time_str,
    is_time_delta_str,
    notify_all,
)


@out_contract(lambda res: res is None or res >= 0)
def get_spend_sec(time_: str) -> Optional[int]:
    if is_specific_time_str(time_):
        now_ = datetime.now()
        time_info = get_specific_time_from_str(time_)
        return convert_specific_time_to_time_delta(
            time_info, (now_.hour, now_.minute, now_.second))
    elif is_time_delta_str(time_):
        return get_time_delta_from_str(time_)

    return None


def get_ring_filename(ring_sound_filename: Optional[str]) -> str:

    def _get_ring_filename() -> str:
        ring_filename_in_sys = getenv('EXCLOCK_RING_FILENAME')
        if ring_sound_filename is None and ring_filename_in_sys is None:
            return DEFAULT_RING_FILENAME
        elif ring_sound_filename is None:
            return str(ring_filename_in_sys)
        else:
            return str(ring_sound_filename)

    return get_real_sound_filename(_get_ring_filename())


def main(opt: optparse.Values, args: List[str]) -> None:
    spend_sec = get_spend_sec(opt.time)
    if spend_sec is None:
        print("time format is illegal.", file=stderr)
        exit(1)

    try:
        ring_sound_filename = get_ring_filename(opt.ring_filename)
        if not Path(ring_sound_filename).exists():
            print("Ring filename is not found.", file=stderr)
            exit(1)

        message = f"Specified time is passed(sec={spend_sec})."
        notify_all(title="⏰ Exclock ⏰", message=message, spend_sec=spend_sec, is_first=False)

        p = Player(ring_sound_filename)
        p.play()
    except KeyboardInterrupt:
        ...
    finally:
        print('bye')
