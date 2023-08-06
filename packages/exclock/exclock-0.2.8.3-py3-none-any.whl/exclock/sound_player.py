#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path
from subprocess import DEVNULL, Popen
from typing import List

from ycontract import in_contract


@dataclass
class Player:
    sound_filename: str
    pid: str = ""
    started: bool = False
    _proc: Popen = Popen("echo", stdout=DEVNULL, stderr=DEVNULL)

    @property  # type: ignore
    @in_contract(lambda self: Path(self.sound_filename).exists())
    def play_commands(self) -> List[str]:
        commands = ["mplayer", self.sound_filename]
        return commands

    @property
    def play_command(self) -> str:
        return " ".join(self.play_commands)

    def play(self) -> None:
        self._proc = Popen(self.play_commands, stdout=DEVNULL, stderr=DEVNULL)
        self.started = True
        self.pid = str(self._proc.pid)


if __name__ == '__main__':
    from sys import argv, exit, stderr

    if len(argv) != 2:
        print("Usage: python {prog} {filename}", file=stderr)
        exit(1)

    filename = argv[1]
    player = Player(filename)
    player.play()
