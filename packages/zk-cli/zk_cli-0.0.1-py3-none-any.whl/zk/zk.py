#! /usr/bin/python3
from abc import abstractmethod
import argparse
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from subprocess import call
from typing import Iterable


class FileAlreadyExistsException(Exception):
    pass


@dataclass
class ZKProject:
    home: Path
    timestamp: datetime

    @property
    def notes(self) -> Path:
        return self.home / "notes"

    @property
    def bib(self) -> Path:
        return self.home / "bib"

    @property
    def config(self) -> Path:
        return self.home / "zk.conf"

    def init(self):
        self.notes.mkdir()
        self.bib.mkdir()
        self.config.touch()

    def _new_file(self, file_type: type, name: str):
        file = file_type(self, name)
        file.touch()
        return file

    def new_note(self, name: str):
        return self._new_file(Note, name)

    def new_bib(self, name: str):
        return self._new_file(Bib, name)


def _fmt_date(date: datetime):
    return date.strftime("%Y%m%d%H%M")


class File:
    def __init__(self, project: ZKProject, name: str):
        self.project = project
        self.file_name = f"{_fmt_date(project.timestamp)} {name}.md"

    @abstractmethod
    def path(self) -> Path:
        pass

    def touch(self):
        if self.path().exists():
            raise FileAlreadyExistsException
        self.path().touch()

    def edit(self):
        call(["nvim", self.path().absolute()])


class Note(File):
    def path(self) -> Path:
        return self.project.notes / self.file_name


class Bib(File):
    def path(self) -> Path:
        return self.project.bib / self.file_name


def main():
    parser = argparse.ArgumentParser(
        description="A command line utility for Zettelkasten."
    )
    subparsers = parser.add_subparsers(dest="command")
    init_parser = subparsers.add_parser("init")
    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("name", nargs="*")
    bib_parser = subparsers.add_parser("bib")
    bib_parser.add_argument("name", nargs="*")
    args = parser.parse_args()

    home = os.getenv("ZK_HOME", "~/zk")
    project = ZKProject(Path(home), datetime.utcnow())
    if args.command is None:
        parser.print_help()
    elif args.command == "init":
        project.init()
    elif args.command in ("new", "bib"):
        fn = getattr(project, f"{args.command}_note")
        file = fn(" ".join(args.name))
        file.edit()

