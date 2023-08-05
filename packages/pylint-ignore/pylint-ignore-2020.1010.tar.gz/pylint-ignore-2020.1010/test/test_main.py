# -*- coding: utf-8 -*-
# pylint:disable=redefined-outer-name ; pytest.fixture ignore_file

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys
import shutil

import pytest
import pathlib2 as pl

from pylint_ignore.__main__ import main

PROJECT_DIR = pl.Path(__file__).parent.parent

FIXTURES_DIR = PROJECT_DIR / "fixtures"


@pytest.fixture()
def ignore_file():
    ignore_file = FIXTURES_DIR / "pylint-ignore.md"
    stat_before = ignore_file.stat()

    backup_file = FIXTURES_DIR / "pylint-ignore.md.backup"
    shutil.copyfile(str(ignore_file), str(backup_file))
    yield ignore_file

    if stat_before != ignore_file.stat():
        shutil.copyfile(str(backup_file), str(ignore_file))
    backup_file.unlink()


def test_selftest_no_ignore_update(ignore_file, capsys):
    if sys.version < "3.7":
        return

    os.chdir(str(PROJECT_DIR))

    stat_before = ignore_file.stat()

    args = [
        "--rcfile=setup.cfg",
        "--score=no",
        "fixtures/",
        "--ignorefile",
        "fixtures/pylint-ignore.md",
    ]
    exitcode = main(args)
    assert exitcode == 0

    stat_after = ignore_file.stat()
    assert stat_before.st_mtime == stat_after.st_mtime

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_selftest_ignore_update_noop(ignore_file, capsys):
    if sys.version < "3.7":
        return

    os.chdir(str(PROJECT_DIR))

    stat_before = ignore_file.stat()

    args = [
        "--rcfile=setup.cfg",
        "--score=no",
        "fixtures/",
        "--ignorefile=fixtures/pylint-ignore.md",
        "--update-ignorefile",
    ]
    exitcode = main(args)
    assert exitcode == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    stat_after = ignore_file.stat()
    assert stat_before.st_mtime == stat_after.st_mtime
