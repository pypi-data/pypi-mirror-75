#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

from click.testing import CliRunner

from tangoctl.cli import cli

from test_tangoctl import tango, _ls_members


def test_help():
    result = CliRunner().invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert '--help  Show this message and exit.' in result.output


def test_device_list(tango):
    result = CliRunner().invoke(cli, ['device', 'list'])
    assert result.exit_code == 0
    res = _ls_members(result.output)
    assert res == ['sys/database/2', 'sys/tg_test/1', 'sys/tg_test/2']


def test_device_tree(tango):
    result = CliRunner().invoke(cli, ['device', 'tree'])
    assert result.exit_code == 0
    tree = result.output
    tree_lines = [l for l in tree.split('\n') if l.strip()]
    assert tree_lines[0] == 'acme:10000'
    assert 'sys' in tree_lines[1]
    assert 'database' in tree_lines[2]
    assert '2' in tree_lines[3]
    assert 'tg_test' in tree_lines[4]
    assert '1' in tree_lines[5]
    assert '2' in tree_lines[6]
    assert len(tree_lines) == 7


def test_device_attribute_list(tango):
    result = CliRunner().invoke(cli, ['device', 'attribute', 'list', '-d' 'sys/tg_test/1'])
    assert result.exit_code == 0
    assert result.output.strip() == 'double_scalar  status\nstate'

    result = CliRunner().invoke(cli, ['device', 'attribute', 'list', '-d' 'sys/tg_test/1', '--nb-cols', '1'])
    assert result.exit_code == 0
    assert result.output.strip() == 'double_scalar\nstate\nstatus'


def test_server_list(tango):
    result = CliRunner().invoke(cli, ['server', 'list'])
    assert result.exit_code == 0
    res = _ls_members(result.output)
    assert res == ['DataBaseds/2', 'TangoTest/test1', 'TangoTest/test2']


def test_server_instance_list(tango):
    result = CliRunner().invoke(cli, ['server', 'ilist', '-t', 'TangoTest'])
    assert result.exit_code == 0
    res = _ls_members(result.output)
    assert res == ['test1', 'test2']


def test_server_ping(tango):
    result = CliRunner().invoke(cli, ['server', 'ping', '--no-color', '-s', 'DataBaseds/2'])
    assert result.exit_code == 0
    assert result.output.strip() == 'DataBaseds/2 546 us'


def test_server_tree(tango):
    result = CliRunner().invoke(cli, ['server', 'tree'])
    assert result.exit_code == 0
    tree = result.output
    tree_lines = [l for l in tree.split('\n') if l.strip()]
    assert tree_lines[0] == 'acme:10000'
    assert 'DataBaseds' in tree_lines[1]
    assert '2' in tree_lines[2]
    assert 'sys/database/2' in tree_lines[3]
    assert 'TangoTest' in tree_lines[4]
    assert 'test1' in tree_lines[5]
    assert 'sys/tg_test/1' in tree_lines[6]
    assert 'test2' in tree_lines[7]
    assert 'sys/tg_test/2' in tree_lines[8]
    assert len(tree_lines) == 9

