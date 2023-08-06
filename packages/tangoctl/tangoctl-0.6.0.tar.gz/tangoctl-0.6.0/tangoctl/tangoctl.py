# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

import sys
import socket
import struct
import fnmatch
import logging
import functools
import collections

import gevent
import tango.gevent

import colorful


Database = tango.Database
Device = tango.gevent.DeviceProxy
Attribute = tango.gevent.AttributeProxy

ServerInfo = collections.namedtuple(
    "ServerInfo", ("name", "type", "instance", "host", "devices")
)
DeviceInfo = collections.namedtuple(
    "DeviceInfo", ("name", "server", "klass", "alias", "exported")
)
DatabaseInfo = collections.namedtuple(
    "DatabaseInfo", ("name", "host", "port", "servers", "devices", "aliases")
)


log = logging.getLogger("tangoctl")


def tango_error_str(exc_value, verbose=False, stack_message=-1):
    if verbose:
        msg = "\n".join(
            reversed(
                [
                    "{} @ {}: {}".format(err.reason, err.origin, err.desc)
                    for err in exc_value
                ]
            )
        )
    else:
        err = exc_value.args[stack_message]
        msg = "{}: {}".format(err.reason, err.desc)
    return msg


class ErrorHandler(object):
    def build_message(self, exc_type, exc_value, traceback):
        if issubclass(exc_type, tango.DevFailed):
            msg = tango_error_str(exc_value, verbose=self.verbose)
        else:
            msg = repr(exc_value)
        return msg

    def __init__(self, echo=None, verbose=False):
        if echo is None:
            echo = functools.partial(print, file=sys.stderr)
        self.echo = echo
        self.verbose = verbose

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            msg = self.build_message(exc_type, exc_value, traceback)
            self.echo(msg)
        return True


@functools.lru_cache(maxsize=4)
def _get_db(db_name=None):
    if db_name is None:
        return Database()
    return Database(db_name)


def get_db(db=None):
    if db is None or isinstance(db, str):
        return _get_db(db)
    return db


def get_db_name(db):
    return "{}:{}".format(db.get_db_host(), db.get_db_port())


def _get_server_devices(server_id, db=None):
    db = get_db(db)
    class_list = db.get_device_class_list(server_id)
    return {
        name: DeviceInfo(name, server_id, klass, alias=None, exported=None)
        for name, klass in zip(class_list[::2], class_list[1::2])
    }


def _build_db_standard(db=None):
    db = get_db(db)
    all_servers, all_devices = {}, {}
    for server_id in db.get_server_list():
        server_type, server_instance = server_id.split("/", 1)
        devices = _get_server_devices(server_id, db=db)
        all_devices.update(devices)
        device_names = {device_name for device_name in devices}
        server = ServerInfo(server_id, server_type, server_instance, None, device_names)
        all_servers[server_id] = server
    host, port = db.get_db_host(), db.get_db_port_num()
    name = "{}:{}".format(host, port)
    return DatabaseInfo(
        servers=all_servers,
        devices=all_devices,
        host=host,
        port=port,
        aliases=set(),
        name=name,
    )


def _build_db_quick(db_dev):
    all_servers, all_devices = {}, {}
    query = "SELECT name, alias, exported, host, server, class FROM device"
    r = db_dev.DbMySqlSelect(query)
    row_nb, column_nb = r[0][-2:]
    data = r[1]
    assert row_nb == len(data) // column_nb
    all_servers, all_devices, aliases = {}, {}, {}
    for row in range(row_nb):
        idx = row * column_nb
        cells = data[idx : idx + column_nb]
        dev_name, dev_alias, exported, host, server_id, klass = cells
        # handle garbage:
        if not server_id or server_id.count("/") != 1:
            continue
        if not dev_name or dev_name.count("/") != 2:
            print("skip", dev_name)
            continue
        if not dev_alias:
            dev_alias = None
        else:
            aliases[dev_alias] = dev_name
        device = DeviceInfo(dev_name, server_id, klass, dev_alias, bool(int(exported)))
        server = all_servers.get(server_id)
        if server is None:
            server_type, server_instance = server_id.split("/", 1)
            server = ServerInfo(server_id, server_type, server_instance, host, set())
            all_servers[server_id] = server
        server.devices.add(dev_name)
        all_devices[dev_name.lower()] = device
    db = db_dev.get_device_db()
    host, port = db.get_db_host(), db.get_db_port_num()
    name = "{}:{}".format(host, port)
    return DatabaseInfo(
        servers=all_servers,
        devices=all_devices,
        aliases=aliases,
        host=host,
        port=port,
        name=name,
    )


def _build_db(db=None):
    db = get_db(db)
    db_dev_name = "{}/{}".format(get_db_name(db), db.dev_name())
    db_dev = Device(db_dev_name)
    if hasattr(db_dev, "DbMySqlSelect"):
        return _build_db_quick(db_dev)
    else:
        return _build_db_standard(db=db)


# TODO: consider creating a timestamped ~/.cache/tangoctl/db_name.pkl with db_info

DB_INFO = {}


def get_db_info(db=None):
    global DB_INFO
    db = get_db(db)
    db_name = get_db_name(db)
    db_info = DB_INFO.get(db_name)
    if db_info is None:
        DB_INFO[db_name] = db_info = _build_db(db)
    return db_info


IOR = collections.namedtuple(
    "IOR",
    "first dtype_length dtype nb_profile tag "
    "length major minor wtf host_length ip port body",
)


def _ascii_to_bytes(s):
    convert = lambda x: struct.Struct(">B").pack(int(x, 16))
    return b"".join(convert(s[i : i + 2]) for i in range(0, len(s), 2))


def _parse_ior(encoded_ior):
    assert encoded_ior[:4] == "IOR:"
    ior = _ascii_to_bytes(encoded_ior[4:])
    dtype_length = struct.unpack_from("II", ior)[-1]
    form = "II{:d}sIIIBBHI".format(dtype_length)
    host_length = struct.unpack_from(form, ior)[-1]
    form = "II{:d}sIIIBBHI{:d}sH0I".format(dtype_length, host_length)
    values = struct.unpack_from(form, ior)
    values += (ior[struct.calcsize(form) :],)
    strip = lambda x: x[:-1] if isinstance(x, bytes) else x
    return IOR(*map(strip, values))


TYPE_MAP = {
    tango.CmdArgType.DevVoid: "void",
    tango.CmdArgType.DevState: "state",
    tango.CmdArgType.DevEnum: "enum",
    tango.CmdArgType.DevEncoded: "(str, bytes)",
    tango.CmdArgType.DevBoolean: "bool",
    tango.CmdArgType.DevUChar: "bytes",
    tango.CmdArgType.DevString: "str",
    tango.CmdArgType.DevShort: "int16",
    tango.CmdArgType.DevUShort: "uint16",
    tango.CmdArgType.DevLong: "int32",
    tango.CmdArgType.DevLong64: "int64",
    tango.CmdArgType.DevULong: "uint32",
    tango.CmdArgType.DevULong64: "uint64",
    tango.CmdArgType.DevFloat: "float32",
    tango.CmdArgType.DevDouble: "float64",
    tango.CmdArgType.DevVarStringArray: "[str]",
    tango.CmdArgType.DevVarBooleanArray: "[bool]",
    tango.CmdArgType.DevVarCharArray: "[bytes]",
    tango.CmdArgType.DevVarDoubleArray: "[float64]",
    tango.CmdArgType.DevVarDoubleStringArray: "[float64, str]",
    tango.CmdArgType.DevVarFloatArray: "[float32]",
    tango.CmdArgType.DevVarLong64Array: "[int64]",
    tango.CmdArgType.DevVarLongArray: "[int32]",
    tango.CmdArgType.DevVarLongStringArray: "[int32, str]",
    tango.CmdArgType.DevVarShortArray: "[int16]",
    tango.CmdArgType.DevVarStateArray: "[state]",
    tango.CmdArgType.DevVarULong64Array: "[uint64]",
    tango.CmdArgType.DevVarULongArray: "[uint32]",
    tango.CmdArgType.DevVarUShortArray: "[uint16]",
}


def type_str(t, format=None):
    if isinstance(t, int):
        t = tango.CmdArgType.values[t]
    tstr = TYPE_MAP[t]
    if format == tango.AttrDataFormat.SPECTRUM:
        tstr = "[{}]".format(tstr)
    elif format == tango.AttrDataFormat.IMAGE:
        tstr = "[[{}]]".format(tstr)
    return tstr


NULL = (
    "Not specified",
    "No description",
    "No unit",
    "No standard unit",
    "No display unit",
)


def value_str(v):
    return "---" if v in NULL else str(v)


def attr_value_str_color(v):
    if v["has_failed"]:
        err = v["error"][0]
        value_str = "{}: {}".format(err.reason, err.desc)
        fg = "bright_red"
        return value_str, fg
    quality = v["quality"]
    if quality == tango.AttrQuality.ATTR_INVALID:
        value_str = "---"
    else:
        value_str = str(v["value"])
    unit = v["unit"]
    unit = "" if unit == "No unit" else " " + unit
    fg = None
    if quality == tango.AttrQuality.ATTR_INVALID:
        fg = "bright_red"
    elif quality == tango.AttrQuality.ATTR_WARNING:
        fg = "yellow"
    elif quality == tango.AttrQuality.ATTR_ALARM:
        fg = "red"
    elif quality == tango.AttrQuality.ATTR_CHANGING:
        fg = "bright_blue"
    return "{}{}".format(value_str, unit), fg


def access_str(access):
    if access == tango.AttrWriteType.READ:
        return "R"
    elif access == tango.AttrWriteType.WRITE:
        return "W"
    elif access == tango.AttrWriteType.READ_WRITE:
        return "RW"
    elif access == tango.AttrWriteType.READ_WITH_WRITE:
        return "RWW"
    return "?"


def fnmatch_any(name, patterns, case_insensitive=False):
    """helper that returns True if name matches any in the list of patterns"""
    if not patterns:
        return True
    if isinstance(patterns, str):
        patterns = (patterns,)
    if case_insensitive:
        name = name.lower()
        patterns = [p.lower() for p in patterns]
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def style(msg, fg=None, bg=None, bold=None, underlined=None, inversed=None):
    st = []
    bold and st.append("bold")
    underlined and st.append("underlined")
    inversed and st.append("inversed")
    fg and st.append(fg)
    bg and st.append("on_" + bg)
    f = getattr(colorful, "_".join(st))
    return f(msg)


# ----- API -----


def iter_devices(
    device=None, server=None, klass=None, host=None, exclude_dserver=True, db=None
):
    db = get_db(db)
    db_info = get_db_info(db=db)

    devs, servers = db_info.devices, db_info.servers
    devices = (devs[dname] for dname in sorted(devs))
    if exclude_dserver:
        devices = (d for d in devices if d.klass != "DServer")
    devices = (
        d
        for d in devices
        if fnmatch_any(d.name, device, case_insensitive=True)
        or (d.alias and fnmatch_any(d.alias, device, case_insensitive=True))
    )
    devices = (d for d in devices if fnmatch_any(d.klass, klass))
    devices = (d for d in devices if fnmatch_any(d.server, server))
    devices = (
        d
        for d in devices
        if fnmatch_any(servers[d.server], host, case_insensitive=True)
    )
    return devices


def iter_servers(server=None, server_type=None, server_instance=None, db=None):
    db_info = get_db_info(db=db)
    servers = db_info.servers
    servs = (servers[sname] for sname in sorted(servers))
    servs = (s for s in servs if fnmatch_any(s.name, server))
    servs = (s for s in servs if fnmatch_any(s.type, server_type))
    servs = (s for s in servs if fnmatch_any(s.instance, server_instance))
    return servs


def server_tree(
    server_name=None,
    server_type=None,
    server_instance=None,
    compact=False,
    server_only=False,
    exclude_dserver=True,
    db=None,
):
    import treelib

    db_info = get_db_info(db=db)
    db_name = db_info.name

    tree = treelib.Tree()
    db_node = tree.create_node(db_name)
    servers = iter_servers(
        server=server_name,
        server_type=server_type,
        server_instance=server_instance,
        db=db,
    )

    if compact:
        for serv in servers:
            serv_inst_node = tree.create_node(serv.name, parent=db_node)
            if not server_only:
                for device in sorted(serv.devices):
                    dlower = device.lower()
                    if exclude_dserver and dlower.startswith("dserver/"):
                        continue
                    device_info = db_info.devices[dlower]
                    text = "{} ({})".format(device, device_info.klass)
                    tree.create_node(text, parent=serv_inst_node)
    else:
        # group servers by type
        serv_map = collections.defaultdict(dict)
        for serv in servers:
            serv_map[serv.type][serv.instance] = serv

        for serv_type in sorted(serv_map):
            instances = serv_map[serv_type]
            serv_type_node = tree.create_node(serv_type, parent=db_node)
            for serv_inst in sorted(instances):
                serv = instances[serv_inst]
                serv_inst_node = tree.create_node(serv_inst, parent=serv_type_node)
                if not server_only:
                    for device in sorted(serv.devices):
                        dlower = device.lower()
                        if exclude_dserver and dlower.startswith("dserver/"):
                            continue
                        device_info = db_info.devices[dlower]
                        text = "{} ({})".format(device, device_info.klass)
                        tree.create_node(text, parent=serv_inst_node)
    return tree


def server_info(name, db=None):
    dserver = "dserver/" + name
    r = device_info(dserver, db=db)
    r.pop("class")
    r["name"] = r.pop("server")
    return r


def expr_to_iservers(expr, db=None):
    db = get_db(db)
    servers = db.get_server_list()
    f = lambda server: fnmatch_any(server, expr)
    return filter(f, servers)


def server_ping(server_names):
    def ping(server):
        try:
            r = Device("dserver/" + server).ping()
        except Exception as err:
            r = err
        return server, r

    ping_tasks = [gevent.spawn(ping, server_name) for server_name in server_names]
    for result in gevent.iwait(ping_tasks):
        yield result.get()


def server_stop(server_names):
    def stop(server):
        try:
            r = Device("dserver/" + server).Kill()
        except Exception as err:
            r = err
        return server, r

    stop_tasks = [gevent.spawn(stop, server_name) for server_name in server_names]
    for result in gevent.iwait(stop_tasks):
        yield result.get()


def server_add(server, devices, db=None):
    db = get_db(db)
    for dev_class, dev_name in devices:
        dev_info = tango.DbDevInfo()
        dev_info.name = dev_name
        dev_info._class = dev_class
        dev_info.server = server
        db.add_device(dev_info)
        yield server, "{}:{}".format(dev_class, dev_name)


def server_delete(server, db=None):
    db = get_db(db)
    db.delete_server(server)


device_add = server_add


def device_delete(devices, db=None):
    db = get_db(db)
    for device in devices:
        db.delete_device(str(device))


def expr_to_idevices(expr, exclude_dserver=True, db=None):
    db = get_db(db)
    db_info = get_db_info(db=db)

    devs = db_info.devices
    devices = (devs[dname] for dname in sorted(devs))
    if exclude_dserver:
        devices = (d for d in devices if d.klass != "DServer")
    f = lambda dev: fnmatch_any(dev.name.lower(), expr, case_insensitive=True)
    return filter(f, devices)


def device_ping(device_names, exclude_dserver=True):
    def ping(device_name):
        try:
            r = Device(device_name).ping()
        except Exception as err:
            r = err
        return device_name, r

    ping_tasks = [gevent.spawn(ping, device_name) for device_name in device_names]
    for result in gevent.iwait(ping_tasks):
        yield result.get()


def device_info(name, db=None):
    db = get_db(db)
    info = db.get_device_info(name)
    ior = _parse_ior(info.ior)
    try:
        host = socket.gethostbyaddr(ior.ip)[0]
    except:
        host = ""
    r = {
        "class": info.class_name,
        "server": info.ds_full_name,
        "exported": info.exported,
        "name": info.name,
        "pid": info.pid,
        "last started": info.started_date,
        "last stopped": info.stopped_date,
        "version": info.version,
        "ip": ior.ip.decode(),
        "port": ior.port,
        "host": host,
    }
    return r


def device_command(name, command, arg=None):
    device = Device(name)
    if arg is None:
        return device.command_inout(command)
    else:
        return device.command_inout(command, arg)


def device_attribute_read(name, attribute):
    device = Device(name)
    return device.read_attribute(attribute)


def _attr_to_dict(config=None, value=None):
    result = {}
    if value:
        result.update({k: getattr(value, k) for k in dir(value)})
        if value.has_failed:
            result["error"] = value.get_err_stack()
    if config:
        result.update({k: getattr(config, k) for k in dir(config)})
    return result


def expr_to_iattrs(expr, attribute_names):
    f = lambda name: fnmatch_any(name, expr, case_insensitive=True)
    return filter(f, attribute_names)


def attributes_read(dev_attr_map):
    def read(device_name, attrs):
        try:
            d = Device(device_name)
            attrs = tuple(expr_to_iattrs(attrs, d.get_attribute_list()))
            values = {value.name: value for value in d.read_attributes(attrs)}
            r = [
                _attr_to_dict(config, values[config.name])
                for config in d.get_attribute_config_ex(attrs)
            ]
        except Exception as err:
            r = err
        return device_name, r

    read_tasks = [
        gevent.spawn(read, name, attrs) for name, attrs in dev_attr_map.items()
    ]
    for result in gevent.iwait(read_tasks):
        yield result.get()


def device_attribute_write(name, attribute, value):
    device = Device(name)
    attr_info = device.get_attribute_config(attribute)
    if attr_info.data_type != tango.CmdArgType.DevString:
        value = eval(value)
    device.write_attribute(attribute, value)


def device_attribute_info(name, attribute):
    device = Device(name)
    return device.get_attribute_config(attribute)


def device_attributes(dev_name, attribute=None):
    device = Device(dev_name)
    attrs = device.attribute_list_query_ex()
    f = lambda attr: fnmatch_any(attr.name, attribute, case_insensitive=True)
    attrs = filter(f, attrs)
    return sorted(attrs, key=lambda a: a.name)


def device_commands(dev_name, command=None):
    device = Device(dev_name)
    cmds = device.command_list_query()
    f = lambda cmd: fnmatch_any(cmd.cmd_name, command, case_insensitive=True)
    attrs = filter(f, cmds)
    return sorted(cmds, key=lambda a: a.cmd_name)


def device_command_info(name, command):
    device = Device(name)
    return device.get_command_config(command)


def expr_to_iprops(expr, prop_names):
    f = lambda name: fnmatch_any(name, expr)
    return filter(f, prop_names)


def device_properties_read(dev_name, properties, db=None):
    db = get_db(db)
    props = tuple(db.get_device_property_list(dev_name, "*"))
    props = tuple(expr_to_iprops(properties, props))
    return db.get_device_property(dev_name, props)


def device_property_write(dev_name, property, value, db=None):
    db = get_db(db)
    return db.put_device_property(dev_name, {str(property): str(value)})


def device_property_list(dev_name, db=None):
    db = get_db(db)
    return tuple(db.get_device_property_list(dev_name, "*"))


def device_alias_list(dev_name, db=None):
    db = get_db(db)
    return tuple(db.get_device_alias_list(dev_name))


def alias_from_device(dev_name, db=None):
    db = get_db(db)
    return db.get_alias_from_device(dev_name)


def set_device_alias(dev_name, alias, db=None):
    db = get_db(db)
    db.put_device_alias(dev_name, alias)


def remove_device_alias(alias, db=None):
    db = get_db(db)
    db.delete_device_alias(alias)


def starter_names(db=None):
    db = get_db(db)
    return [s.split("/", 1)[-1] for s in db.get_server_list("Starter/*")]


def starter_device_name(host, db=None):
    db = get_db(db)
    dev_class_name = db.get_device_class_list("Starter/{}".format(host))
    for d, k in zip(dev_class_name[::2], dev_class_name[1::2]):
        if k == "Starter":
            return d


def human_starter_server_state(state):
    if state == "FAULT":
        return "NOT running"
    elif state == "ON":
        return "Running"
    elif state == "MOVING":
        return "Starting/Stopping"


class Starter:
    def __init__(self, name, db=None):
        self._log = log.getChild(name)
        self.name = name
        self.db = get_db(db)
        self.device_name = starter_device_name(name, db=db)
        self._device = None

    @property
    def starter_device(self):
        if self._device is None:
            self._device = Device(self.device_name)
        return self._device

    def _filtered_servers(self, filt):
        return {k: s for k, s in self.servers.items() if filt(s)}

    @property
    def running_servers(self):
        return self._filtered_servers(lambda s: s["state"] == "ON")

    @property
    def transition_servers(self):
        return self._filtered_servers(lambda s: s["state"] == "MOVING")

    @property
    def stopped_servers(self):
        return self._filtered_servers(lambda s: s["state"] == "FAULT")

    @property
    def controlled_servers(self):
        return self._filtered_servers(lambda s: s["controlled"])

    @property
    def servers(self):
        db_info = get_db_info(db=self.db)
        db_servers = db_info.servers
        servers = {}
        starter_servers = self.starter_device["servers"].value or []
        for server in starter_servers:
            name, state, controlled, level, *_ = server.split()
            level = int(level)
            servers[name] = dict(
                name=name,
                state=state,
                controlled=controlled,
                level=level,
                info=db_servers[name],
            )
        return servers

    def __getitem__(self, name):
        return self.servers[name]

    def __contains__(self, name):
        return name in self.servers

    def wait_for_state(self, name, cond):
        while True:
            state = self[name]["state"]
            if cond(state):
                return state
            gevent.sleep(0.2)

    def kill_server(self, name, dry_run=False):
        state = self[name]["state"]
        if state == "FAULT":
            self._log.info(
                "skipped killing %r (%s)", name, human_starter_server_state(state)
            )
            return True
        self._log.info("killing %r...", name)
        if not dry_run:
            try:
                self.starter_device.HardKillServer(name)
            except tango.DevFailed as err:
                err = err.args[0].desc
                state = self[name]["state"]
                if state == "FAULT":
                    self._log.warning(
                        "server %r was killed but reported: %s", name, err
                    )
                    return True
                else:
                    self._log.error("failed to kill %r: %s", name, err)
                    return False
            state = self.wait_for_state(name, lambda s: s in ("MOVING", "FAULT"))
            if not state:
                self._log.warn("failed to wait to kill %r", name)
                return False
            if state == "FAULT":
                self._log.info("killed %r", name)
                return True
            state = self.wait_for_state(name, lambda s: s == "FAULT")
            if not state:
                self._log.warn("failed to kill %r", name)
                return False
        self._log.info("killed %r", name)
        return True

    def stop_server(self, name, dry_run=False):
        server = self[name]
        state, level = server["state"], server["level"]
        if state == "FAULT":
            self._log.info(
                "skipped stopping %r (%s) (level %d)",
                name,
                human_starter_server_state(state),
                level,
            )
            return True
        self._log.info("stopping %r (level %d)...", name, level)
        if not dry_run:
            try:
                self.starter_device.DevStop(name)
            except tango.DevFailed as err:
                err = err.args[0].desc
                self._log.warning("failed to stop on %r (%r)", name, err)
                return False
            state = self.wait_for_state(name, lambda s: s in ("MOVING", "FAULT"))
            if not state:
                self._log.warn("failed to wait to stop %r", name)
                return False
            if state == "FAULT":
                self._log.info("stopped %r", name)
                return True
            state = self.wait_for_state(name, lambda s: s == "FAULT")
            if not state:
                self._log.warn("failed to stop %r", name)
                return False
        self._log.info("stopped %r", name)
        return True

    def stop_kill_server(self, name, timeout=5, dry_run=False):
        task = gevent.spawn(self.stop_server, name, dry_run=dry_run)
        stopped = False
        try:
            stopped = task.get(timeout=timeout)
        except gevent.Timeout:
            self._log.warning("timeout trying to stop %s. Performing a kill", name)
            stopped = False
            task.kill()
        if not stopped:
            self.kill_server(name, dry_run=dry_run)

    def start_server(self, name, dry_run=False):
        state = self[name]["state"]
        if state == "ON":
            self._log.info(
                "skipped starting %r (%s)", name, human_starter_server_state(state)
            )
            return True
        self._log.info("starting %r", name)
        if not dry_run:
            self.starter_device.DevStart(name)
            state = self.wait_for_state(name, lambda s: s in ("MOVING", "ON"))
            if not state:
                self._log.warn("failed to start %r", name)
                return False
            if state == "ON":
                self._log.info("started %r", name)
                return True
            state = self.wait_for_state(name, lambda s: s == "ON")
            if not state:
                self._log.warn("failed to start %r", name)
                return False
        self._log.info("started %r", name)
        return True

    def restart_server(self, name):
        self.stop_server(name)
        self.start_server(name)


STARTERS = {}


def starters(db=None):
    global STARTERS
    db = get_db(db)
    if db not in STARTERS:
        s = {name: Starter(name, db=db) for name in starter_names(db=db)}
        STARTERS[db] = s
    return STARTERS[db]


def iter_starters(starter_name=None, db=None):
    result = iter(starters(db=db).values())
    result = (s for s in result if fnmatch_any(s.name, starter_name))
    return result


def iter_starter_servers(
    servers, server_name=None, server_type=None, server_instance=None
):
    servers = (s for s in servers if fnmatch_any(s["info"].name, server_name))
    servers = (s for s in servers if fnmatch_any(s["info"].type, server_type))
    servers = (s for s in servers if fnmatch_any(s["info"].instance, server_instance))
    return servers


def find_starter_for_server(server_name, db=None):
    for starter in starters(db=db).values():
        try:
            if server_name in starter:
                return starter
        except tango.DevFailed:
            continue
    return None


def find_starters_for_servers(names, db=None):
    starters_map = starters(db=db).values()
    result = collections.defaultdict(list)
    for starter, servers in starters_servers(*starters_map).items():
        servers = servers or {}
        for name in names:
            if name in servers:
                result[starter].append(servers[name])
    return result


def find_starters_for_filtered_servers(
    starter_name=None,
    server_name=None,
    server_type=None,
    server_instance=None,
    filter_func=None,
    db=None,
):
    starters_seq = iter_starters(starter_name, db=db)
    result = {}
    for starter, servers in starters_servers(*starters_seq).items():
        servers = servers.values() if servers else ()
        servers = iter_starter_servers(
            servers,
            server_name=server_name,
            server_type=server_type,
            server_instance=server_instance,
        )
        if filter_func:
            servers = filter(filter_func, servers)
        servers = list(servers)
        if servers:
            result[starter] = servers
    return result


def find_starters_levels_for_filtered_servers(
    starter_name=None,
    server_name=None,
    server_type=None,
    server_instance=None,
    filter_func=None,
    db=None,
):

    starters_map = find_starters_for_filtered_servers(
        starter_name=starter_name,
        server_name=server_name,
        server_type=server_type,
        server_instance=server_instance,
        filter_func=filter_func,
        db=db,
    )
    # group by levels
    levels = collections.defaultdict(lambda: collections.defaultdict(list))
    for starter, servers in starters_map.items():
        for server in servers:
            level_starters = levels[server["level"]]
            level_starters[starter].append(server)
    return levels


def starters_servers(*starters):
    starter_servers = {}

    def fetch_servers(s):
        try:
            servers = s.servers
        except tango.DevFailed:
            servers = None
        starter_servers[s] = servers

    tasks = [gevent.spawn(fetch_servers, s) for s in starters]
    gevent.joinall(tasks)
    return starter_servers


def stop_server(name, db=None):
    starter = find_starter_for_server(name, db=db)
    if starter is None:
        next(server_stop([name]))
    starter.stop_server(name)


def starter_stop_servers(
    starter_name=None,
    server_name=None,
    server_type=None,
    server_instance=None,
    timeout=None,
    stop_timeout=5,
    dry_run=False,
    db=None,
):

    with gevent.Timeout(timeout):
        levels = find_starters_levels_for_filtered_servers(
            starter_name=starter_name,
            server_name=server_name,
            server_type=server_type,
            server_instance=server_instance,
            filter_func=lambda s: s["level"] > 0,
            db=db,
        )
        for level in sorted(levels, reverse=True):
            level_tasks = []
            for starter, servers in levels[level].items():
                stop = starter.stop_kill_server
                tasks = [
                    gevent.spawn(
                        stop, server["name"], timeout=stop_timeout, dry_run=dry_run
                    )
                    for server in servers
                ]
                level_tasks.extend(tasks)
            log.info("beginning to stop servers at level {}".format(level))
            gevent.joinall(level_tasks)
            log.info("finished stopping level {}".format(level))


def starter_start_servers(
    starter_name=None,
    server_name=None,
    server_type=None,
    server_instance=None,
    timeout=None,
    dry_run=False,
    db=None,
):

    with gevent.Timeout(timeout):
        levels = find_starters_levels_for_filtered_servers(
            starter_name=starter_name,
            server_name=server_name,
            server_type=server_type,
            server_instance=server_instance,
            filter_func=lambda s: s["level"] > 0,
            db=db,
        )
        for level in sorted(levels):
            level_tasks = []
            for starter, servers in levels[level].items():
                stop = starter.start_server
                tasks = [
                    gevent.spawn(stop, server["name"], dry_run=dry_run)
                    for server in servers
                ]
                level_tasks.extend(tasks)
            log.info("beginning to start servers at level {}".format(level))
            gevent.joinall(level_tasks)
            log.info("finished starting servers at level {}".format(level))


def starter_restart_servers(
    starter_name=None,
    server_name=None,
    server_type=None,
    server_instance=None,
    timeout=None,
    dry_run=False,
    db=None,
):

    db = get_db(db)

    with gevent.Timeout(timeout):
        starter_stop_servers(
            starter_name=starter_name,
            server_name=server_name,
            server_type=server_type,
            server_instance=server_instance,
            dry_run=dry_run,
            db=db,
        )
        starter_start_servers(
            starter_name=starter_name,
            server_name=server_name,
            server_type=server_type,
            server_instance=server_instance,
            dry_run=dry_run,
            db=db,
        )


def starter_tree(
    starter_name=None,
    server_name=None,
    server_type=None,
    server_instance=None,
    all=False,
    colored=True,
    db=None,
):

    import treelib

    db_info = get_db_info(db=db)
    db_name = db_info.name

    tree = treelib.Tree()
    db_node = tree.create_node(db_name)
    starters = list(iter_starters(starter_name=starter_name, db=db))
    starters_servers_dict = starters_servers(*starters)
    for starter in starters:
        level_servers = collections.defaultdict(list)
        servers = starters_servers_dict[starter]
        fg = "red2" if servers is None else "green3"
        name = str(style(starter.name, fg=fg)) if colored else starter.name
        starter_node = tree.create_node(name, parent=db_node)
        servers = servers.values() if servers else []
        servers = iter_starter_servers(
            servers, server_name, server_type, server_instance
        )
        for starter_server in servers:
            level = level_servers[starter_server["level"]]
            level.append(starter_server)
        for level in sorted(level_servers):
            if level == 0:
                if not all:
                    continue
                name = "Not controlled"
            else:
                name = "level {}".format(level)
            level_node = tree.create_node(name, parent=starter_node)
            for starter_server in level_servers[level]:
                state = starter_server["state"]
                label = starter_server["name"]
                if colored:
                    if state == "ON":
                        color = "green3"
                    elif state == "FAULT":
                        color = "red2"
                    elif state == "MOVING":
                        color = "royalBlue1"
                    else:
                        color = "magenta"
                    label = str(style(label, fg=color))
                tree.create_node(label, parent=level_node)
    return tree
