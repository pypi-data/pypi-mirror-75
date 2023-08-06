"""
Tests for `shtab`.

Currently runnable via nosetests, e.g.:
    shtab$ nose tests -d -v
"""
import logging
import subprocess
from argparse import ArgumentParser

import pytest

import shtab
from shtab.main import get_main_parser, main

SUPPORTED_SHELLS = "bash", "zsh"
fix_shell = pytest.mark.parametrize("shell", SUPPORTED_SHELLS)


class Bash(object):
    def __init__(self, init_script=""):
        self.init = init_script

    def test(self, test="1", failure_message=""):
        """Equivalent to `bash -c '{init}; [[ {test} ]]'`."""
        init = self.init + "\n" if self.init else ""
        proc = subprocess.Popen(
            ["bash", "-c", "{init}[[ {test} ]]".format(init=init, test=test)]
        )
        stdout, stderr = proc.communicate()
        assert (
            0 == proc.wait()
        ), """\
{}
{}
=== stdout ===
{}=== stderr ===
{}""".format(
            failure_message, test, stdout or "", stderr or ""
        )

    def compgen(
        self, compgen_cmd, word, expected_completions, failure_message=""
    ):
        self.test(
            '"$(echo $(compgen {} -- "{}"))" = "{}"'.format(
                compgen_cmd, word, expected_completions
            ),
            failure_message,
        )


@pytest.mark.parametrize(
    "init,test", [("export FOO=1", '"$FOO" -eq 1'), ("", '-z "$FOO"')]
)
def test_bash(init, test):
    shell = Bash(init)
    shell.test(test)


def test_bash_compgen():
    shell = Bash()
    shell.compgen('-W "foo bar foobar"', "fo", "foo foobar")


def test_choices():
    assert "x" in shtab.Optional.FILE
    assert "" in shtab.Optional.FILE

    assert "x" in shtab.Required.FILE
    assert "" not in shtab.Required.FILE


@fix_shell
def test_main(shell, caplog):
    with caplog.at_level(logging.INFO):
        main(["-s", shell, "shtab.main.get_main_parser"])

    assert not caplog.record_tuples


@fix_shell
def test_prog_override(shell, caplog, capsys):
    with caplog.at_level(logging.INFO):
        main(["-s", shell, "--prog", "foo", "shtab.main.get_main_parser"])

    captured = capsys.readouterr()
    assert not captured.err
    if shell == "bash":
        assert "complete -o nospace -F _shtab_shtab foo" in captured.out

    assert not caplog.record_tuples


@fix_shell
def test_prefix_override(shell, caplog, capsys):
    with caplog.at_level(logging.INFO):
        main(["-s", shell, "--prefix", "foo", "shtab.main.get_main_parser"])

    captured = capsys.readouterr()
    assert not captured.err
    if shell == "bash":
        shell = Bash(captured.out)
        shell.compgen('-W "$_shtab_foo_options_"', "--h", "--help")

    assert not caplog.record_tuples


@fix_shell
def test_complete(shell, caplog):
    parser = get_main_parser()
    with caplog.at_level(logging.INFO):
        completion = shtab.complete(parser, shell=shell)
    print(completion)

    if shell == "bash":
        shell = Bash(completion)
        shell.compgen('-W "$_shtab_shtab_options_"', "--h", "--help")

    assert not caplog.record_tuples


@fix_shell
def test_positional_choices(shell, caplog):
    parser = ArgumentParser(prog="test")
    parser.add_argument("posA", choices=["one", "two"])
    with caplog.at_level(logging.INFO):
        completion = shtab.complete(parser, shell=shell)
    print(completion)

    if shell == "bash":
        shell = Bash(completion)
        shell.compgen('-W "$_shtab_test_commands_"', "o", "one")

    assert not caplog.record_tuples
