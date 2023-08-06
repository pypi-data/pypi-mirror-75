#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

"""Tests for `tangoctl` package."""


import types
from unittest import mock

import pytest

import tango
import tangoctl.tangoctl

AttributeInfoEx = tango.AttributeInfoEx
DataFormat = tango.AttrDataFormat
ArgType = tango.CmdArgType
Quality = tango.AttrQuality

# Cannot set tango.CommandInfo members so we create one here
class CommandInfo:
    pass


IOR = 'IOR:010000001700000049444c3a54616e676f2f4465766963655f353a312e3000000100000000000000a1000000010102000e0000003139322e3136382e34332e35380010270800000064617461626173650300000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100025454413d000000010000000c000000546961676f4c656e6f766f00250000002f746d702f6f6d6e692d74616e676f2f3030303030333231332d3135343238303034313400'

@pytest.fixture
def tango():
    state = AttributeInfoEx()
    state.name = 'state'
    state.data_format = DataFormat.SCALAR
    state.data_type = ArgType.DevState
    status = AttributeInfoEx()
    status.name = 'status'
    status.data_format = DataFormat.SCALAR
    status.data_type = ArgType.DevString
    double_scalar = AttributeInfoEx()
    double_scalar.name = 'double_scalar'
    double_scalar.data_format = DataFormat.SCALAR
    double_scalar.data_type = ArgType.DevDouble

    init = CommandInfo()
    init.cmd_name = 'Init'
    init.in_type = ArgType.DevVoid
    init.out_type = ArgType.DevVoid

    with mock.patch('tangoctl.tangoctl.Device') as DeviceProxy, \
         mock.patch('tangoctl.tangoctl.Database') as Database:
        dp = DeviceProxy.return_value
        dp.name.return_value = 'sys/database/2'
        dp.ping.return_value = 546
        dp.attribute_list_query_ex.return_value = [state, status, double_scalar]
        dp.command_list_query.return_value = [init]
        dp.DbMySqlSelect.return_value = [
            [1, 0, 1, 1, 1, 1,
             1, 0, 1, 1, 1, 1,
             1, 0, 1, 1, 1, 1, 3, 6],
            ['sys/database/2', '', '1', 'acme', 'DataBaseds/2', 'DataBase',
             'sys/tg_test/1', '', '1', 'acme', 'TangoTest/test1', 'TangoTest',
             'sys/tg_test/2', '', '0', 'acme', 'TangoTest/test2', 'TangoTest'
            ]
        ]
        db = Database.return_value
        db.get_server_list.return_value = ['DataBaseds/2', 'TangoTest/test1',
                                           'TangoTest/test2']
        db.get_db_host.return_value = 'acme'
        db.get_db_port.return_value = '10000'
        db.get_db_port_num.return_value = 10000
        dev_info = mock.Mock(class_name='DataBase', ds_full_name='DataBaseds/2',
                             exported=1, pid=12345,
                             started_date='21st November 2018 at 12:40:14',
                             stopped_date='', version=5, ior=IOR)
        dev_info.name = 'sys/database/2'
        db.get_device_info.return_value = dev_info

        dp.get_device_db.return_value = db
        yield tango
        # todo reset mock


def _ls_members(text):
    lines = [line.split() for line in text.split('\n')]
    cols = max(map(len, lines))
    result = []
    for col in range(cols):
        result.extend([line[col] for line in lines if len(line) > col])
    return result


_data_types = (
    (ArgType.DevVoid, 'void'),
    (ArgType.DevState, 'state'),
    (ArgType.DevString, 'str'),
    (ArgType.DevBoolean, 'bool'),
    (ArgType.DevFloat, 'float32'),
    (ArgType.DevDouble, 'float64'),
    (ArgType.DevShort, 'int16'),
    (ArgType.DevUShort, 'uint16'),
    (ArgType.DevLong, 'int32'),
    (ArgType.DevULong, 'uint32'),
    (ArgType.DevLong64, 'int64'),
    (ArgType.DevULong64, 'uint64'),
    (ArgType.DevEncoded, '(str, bytes)'),
    (ArgType.DevUChar, 'bytes')
)
_data_formats = [DataFormat.SCALAR, DataFormat.SPECTRUM, DataFormat.IMAGE]


@pytest.mark.parametrize('dformat', [None]+_data_formats)
@pytest.mark.parametrize('dtype, expected', _data_types)
def test_type_str(dtype, dformat, expected):
    if dformat == DataFormat.SPECTRUM:
        expected = '[{}]'.format(expected)
    elif dformat == DataFormat.IMAGE:
        expected = '[[{}]]'.format(expected)
    assert tangoctl.tangoctl.type_str(dtype, dformat) == expected


_V = lambda value, quality=Quality.ATTR_VALID, unit='No unit': \
    dict(value=value, quality=quality, unit=unit, has_failed=False)

@pytest.mark.parametrize('value,expected',
    [(_V(1.2), ('1.2', None)),
     (_V(1.2, unit='mm'), ('1.2 mm', None)),
     (_V(None, Quality.ATTR_INVALID), ('---', 'bright_red')),
     (_V(1.2, Quality.ATTR_ALARM, 'mm'), ('1.2 mm', 'red')),
     (_V(1.2, Quality.ATTR_WARNING, 'mm'), ('1.2 mm', 'yellow'))],
    ids=['double', 'double-unit', 'invalid', 'alarm', 'warning'])
def test_attr_value_str_color(value, expected):
    assert tangoctl.tangoctl.attr_value_str_color(value) == expected


def test_iter_devices(tango):
    idevs = tangoctl.tangoctl.iter_devices()
    assert isinstance(idevs, types.GeneratorType)
    dev_names = [dev.name for dev in idevs]
    assert dev_names == ['sys/database/2', 'sys/tg_test/1', 'sys/tg_test/2']


def test_iter_servers(tango):
    iservs = tangoctl.tangoctl.iter_servers()
    assert isinstance(iservs, types.GeneratorType)
    serv_names = [s.name for s in iservs]
    assert serv_names == ['DataBaseds/2', 'TangoTest/test1', 'TangoTest/test2']


def test_device_info(tango):
    info = tangoctl.tangoctl.device_info('sys/database/2')
    assert info['class'] == 'DataBase'
    assert info['exported'] == 1
    assert info['pid'] == 12345
    assert info['name'] == 'sys/database/2'
    assert info['server'] == 'DataBaseds/2'


def test_device_attributes(tango):
    result = tangoctl.tangoctl.device_attributes('sys/database/2')
    assert len(result) == 3
    assert result[0].name == 'double_scalar'
    assert result[0].data_type == ArgType.DevDouble
    assert result[0].data_format == DataFormat.SCALAR
    assert result[1].name == 'state'
    assert result[1].data_type == ArgType.DevState
    assert result[1].data_format == DataFormat.SCALAR
    assert result[2].name == 'status'
    assert result[2].data_type == ArgType.DevString
    assert result[2].data_format == DataFormat.SCALAR


def test_device_commands(tango):
    result = tangoctl.tangoctl.device_commands('sys/database/2')
    assert len(result) == 1
    assert result[0].cmd_name == 'Init'


def test_device_ping(tango):
    result = list(tangoctl.tangoctl.device_ping(['sys/database/2']))
    assert len(result) == 1
    assert result[0] == ('sys/database/2', 546)


def test_server_ping(tango):
    result = list(tangoctl.tangoctl.server_ping(['DataBaseds/2']))
    assert len(result) == 1
    assert result[0] == ('DataBaseds/2', 546)


def test_server_info(tango):
    info = tangoctl.tangoctl.server_info('DataBaseds/2')
    assert 'class = DataBase' not in info
    assert info['exported'] == 1
    assert info['pid'] == 12345
    assert info['name'] == 'DataBaseds/2'
