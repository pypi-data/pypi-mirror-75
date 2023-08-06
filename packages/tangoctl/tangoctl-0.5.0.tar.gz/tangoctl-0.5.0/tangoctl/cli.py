# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

from __future__ import absolute_import

"""
$ tangoctl server list
$ tangoctl server info -s <server>
$ tangoctl server tree [--filter=<filter>]
$ tangoctl server <start>|<stop>|<status> [<server>]+
$ tangoctl server add -s <server> [-d <class> <device>]+
$ tangoctl server delete [<server>]+
$ tangoctl device list
$ tangoctl device tree [--filter=<filter>]
$ tangoctl device add -s <server> [-d <class> <device>]+ (same as "server add")
$ tangoctl device delete [<device>]+
$ tangoctl device info -d <name>
$ tangoctl device command list -d <device> [--filter=<filter>]
$ tangoctl device command exec -d <device> -c <command> [-p <parameter value>]
$ tangoctl device command info -d <device> -c <command>
$ tangoctl device attribute list -d <device> [--filter=<filter>]
$ tangoctl device attribute read -d <device> -a <attribute>
$ tangoctl device attribute write -d <device> -a <attribute> -v <value>
$ tangoctl device attribute info -d <device> -a <attribute>
$ tangoctl device property read -d <device> -a <attribute> -p <property>
$ tangoctl device property write -d <device> -a <attribute> -p <property> -v <value>
$ tangoctl device property list -d <device>
$ tangoctl starter tree
$ tangoctl starter stop -s <server expr>
$ tangoctl starter start -s <server expr>
$ tangoctl starter restart -s <server expr>
"""

import logging
import itertools
import functools
import collections

import click

import gevent

from . import tangoctl


class error(tangoctl.ErrorHandler):
    def __init__(self, verbose=False):
        echo = functools.partial(click.echo, err=True)
        super(error, self).__init__(echo=echo, verbose=verbose)


pair_class_device = click.option(
    "-d",
    "--device",
    required=True,
    type=(str, str),
    multiple=True,
    help="pair device class and name",
)

device_filter = click.option(
    "-d",
    "--device",
    default=None,
    multiple=True,
    help="filter devices (supports pattern matching *,?,[])",
)

class_filter = click.option(
    "--class",
    "class_",
    default=None,
    multiple=True,
    help="filter devices of classes (supports pattern matching *,?,[])",
)

server_filter = click.option(
    "-s",
    "--server",
    default=None,
    multiple=True,
    help="filter servers (supports pattern matching *,?,[])",
)

starter_filter = click.option(
    "--starter",
    default=None,
    multiple=True,
    help="filter starters (supports pattern matching *,?,[]) " \
    "(multiple values are ORed together)",
)

host_filter = click.option(
    "--host",
    default=None,
    help="filter devices running in hosts (supports pattern matching *,?,[])",
)

nb_cols = click.option(
    "--nb-cols", default=2, show_default=True, help="number of columns"
)

verbose = click.option(
    "-v",
    "--verbose",
    default=False,
    show_default=True,
    is_flag=True,
    help="verbose output",
)

color = click.option(
    "--color/--no-color",
    default=True,
    show_default=True,
    is_flag=True,
    help="colored output",
)

timeout = click.option(
    "--timeout",
    type=float,
    default=None,
    show_default=True,
    help="operation timeout (s)",
)

stop_timeout = click.option(
    "--stop-timeout",
    type=float,
    default=5,
    show_default=True,
    help="timeout for the stop operation. If this timeout expires a kill is done",
)

dserver = click.option(
    "--exclude-dserver/--include-dserver",
    default=True,
    show_default=True,
    is_flag=True,
    help="exclude/include DServer devices",
)

server_type = click.option(
    "-t", "--server-type", default=None, required=True, help="server type"
)

server_type_filter = click.option(
    "-t",
    "--server-type",
    default=None,
    multiple=True,
    help="filter server type (supports pattern matching *,?,[])",
)

server_instance_filter = click.option(
    "--server-instance",
    default=None,
    multiple=True,
    help="filter server instances (supports pattern matching *,?,[])",
)

attr_filter = click.option(
    "-a",
    "--attribute",
    default=None,
    prompt=True,
    multiple=True,
    help="attribute name (supports pattern matching *,?,[])",
)

attrs_filter = click.option(
    "-a",
    "--attribute",
    default=None,
    multiple=True,
    help="attribute name(s) (supports pattern matching *,?,[])",
)

attr = click.option(
    "-a", "--attribute", required=True, prompt=True, help="attribute name"
)

attrs = click.option(
    "-a", "--attribute", required=True, multiple=True, help="attribute name(s)"
)

attrs_arg = click.argument("attributes", required=True, nargs=-1)

cmd = click.option("-c", "--command", required=True, prompt=True, help="command name")

prop = click.option(
    "-p", "--property", required=True, prompt=True, help="property name"
)

props_filter = click.option(
    "-p", "--property", required=True, multiple=True, help="property name"
)

value = click.option("-v", "--value", required=True, prompt=True, help="value")

#: server option
server = click.option(
    "-s", "--server", required=True, prompt=True, help="server name (<type>/<instance>)"
)

# list of server options
servers = click.option(
    "-s",
    "--servers",
    required=True,
    multiple=True,
    help="server names (<type>/<instance>)",
)

#: device option
device = click.option("-d", "--device", required=True, prompt=True, help="device name")

# list of server options
devices = click.option(
    "-d", "--devices", required=True, multiple=True, help="device names"
)

dry_run = click.option(
    "--dry-run",
    default=False,
    show_default=True,
    is_flag=True,
    help="dry run (=simulation)",
)


class ClickOutputHandler(logging.Handler):

    Style = collections.defaultdict(dict)
    Style.update(
        {
            logging.DEBUG: dict(dim=True),
            logging.INFO: dict(),
            logging.WARNING: dict(fg="yellow"),
            logging.ERROR: dict(fg="red"),
            logging.CRITICAL: dict(fg="magenta"),
        }
    )

    def emit(self, record):
        try:
            record.name = record.name.replace("tangoctl.", "")
            record.msg = click.style(record.msg, **self.Style[record.levelno])
            click.echo(self.format(record))
        except Exception:
            self.handleError(record)


def _prepare_logging():
    fmt = "%(asctime)s %(name)14s: %(message)s"
    handler = ClickOutputHandler()
    handler.addFilter(lambda record: record.name.startswith("tangoctl"))
    handler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=[handler])


def _ls_columns(seq, nb_cols=4):
    it = iter(seq)
    nb_rows = len(seq) // nb_cols
    if len(seq) % nb_cols:
        nb_rows += 1
    pars = nb_rows * (it,)
    return zip(*itertools.zip_longest(*pars, fillvalue=""))


def _table(*args, **kwargs):
    import tabulate

    kwargs.setdefault("disable_numparse", True)
    kwargs.setdefault("tablefmt", "plain")
    return tabulate.tabulate(*args, **kwargs)


def _server_str(server, color=False):
    server = server if isinstance(server, str) else server.name
    return click.style(server, fg="cyan" if color else None)


def _server_host_str(server, color=False):
    host = server if isinstance(server, str) else server.host
    host = "---" if host == "nada" else host
    return click.style(host, fg="white" if color else None,
                       dim=True if color else None)


def _device_class_str(dev, color=False):
    klass = dev if isinstance(dev, str) else dev.klass
    return click.style(klass, fg="magenta" if color else None)


def _device_str(dev, color=False):
    dev = dev if isinstance(dev, str) else dev.name
    return click.style(dev, fg="white" if color else None)


def _alias_str(dev, color=False):
    dev = dev if isinstance(dev, str) else dev.alias
    dev = "---" if dev is None else dev
    return click.style(dev, fg="blue" if color else None)


def _device_exported_str(dev, color=False):
    text = "Exported" if dev.exported else "Not. Exp."
    if color:
        fg = "green" if dev.exported else "red"
    else:
        fg = None
    return click.style(text, fg=fg)


def _time_color(us):
    if isinstance(us, Exception):
        return "red"
    elif us < 1e4:  # less than 10ms => OK
        return "green"
    elif us < 1e5:  # less than 100ms => so, so
        return "yellow"
    return "red"


def _attribute_info_table(device, attribute):
    info = tangoctl.device_attribute_info(device, attribute)
    return [
        ["Name", info.name],
        ["Type", tangoctl.type_str(info.data_type, info.data_format)],
        ["Access", tangoctl.access_str(info.writable)],
        ["Display level", tangoctl.value_str(info.disp_level)],
        ["Label", info.label],
        ["Memorized", tangoctl.value_str(info.memorized)],
        ["Max. dim", (info.max_dim_x, info.max_dim_y)],
        [
            "Range",
            "({}, {})".format(
                tangoctl.value_str(info.min_value), tangoctl.value_str(info.max_value)
            ),
        ],
        [
            "Alarms",
            "({}, {})".format(
                tangoctl.value_str(info.alarms.min_alarm),
                tangoctl.value_str(info.alarms.max_alarm),
            ),
        ],
        [
            "Warnings",
            "({}, {})".format(
                tangoctl.value_str(info.alarms.min_warning),
                tangoctl.value_str(info.alarms.max_warning),
            ),
        ],
        ["Label", info.label],
        ["Description", tangoctl.value_str(info.description)],
        ["Format", info.format],
        ["Unit", tangoctl.value_str(info.unit)],
        ["Display unit", tangoctl.value_str(info.display_unit)],
        ["Std. unit", tangoctl.value_str(info.standard_unit)],
        [
            "Arch. abs. change",
            tangoctl.value_str(info.events.arch_event.archive_abs_change),
        ],
        [
            "Arch. rel. change",
            tangoctl.value_str(info.events.arch_event.archive_rel_change),
        ],
        ["Arch. period", tangoctl.value_str(info.events.arch_event.archive_period)],
        ["Abs. change", tangoctl.value_str(info.events.ch_event.abs_change)],
        ["Rel. change", tangoctl.value_str(info.events.ch_event.rel_change)],
        ["Period", tangoctl.value_str(info.events.per_event.period)],
        ["Enums", ", ".join(info.enum_labels) if info.enum_labels else "---"],
    ]


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Query or send control commands to the tango system.

    Examples:

    \b
    Display tree of servers:
    $ tangoctl server tree
    \b
    Display list of devices:
    $ tangoctl device list
    \b
    Read 'state' attribute from a device
    $ tangoctl device attribute read -d sys/tg_test/1 state
    \b
    Execute command Init() on a device
    $ tangoctl device command exec -d sys/tg_test/1 init
    \b
    Display 'double_spectrum' attribute information
    $ tangoctl device attribute info -d sys/tg_test/1 double_spectrum
    \b
    Display list of device attributes:
    $ tangoctl device attribute list sys/tg_test/1

    """
    _prepare_logging()
    if ctx.invoked_subcommand is None:
        from . import repl

        repl.run(ctx)


@cli.group("device")
def device_group():
    """
    Device related operations (list, tree, add, delete, ...)
    """
    pass


@device_group.command("list")
@device_filter
@class_filter
@server_filter
@host_filter
@nb_cols
@dserver
def device_list(device, class_, server, host, nb_cols, exclude_dserver):
    """
    Show list of devices.

    Many filters with expression matching supported (device, server, host, device class)

    Example:

    \b
    $ tangoctl device list -d sys/*
    sys/access_control/1            sys/profile/droldan
    sys/database/2                  sys/taurus_test/1
    sys/database/3                  sys/tg_test/01
    sys/database/test               sys/tg_test/02
    sys/DDebug/PyAlarm_FE_AUTO      sys/tg_test/03
    sys/processprofiler/ct32suse11  sys/tg_test/1
    sys/profile/AdlinkIODS          sys/tg_test/useless
    sys/profile/controls01
    """

    with error():
        devices = tangoctl.iter_devices(
            device=device,
            klass=class_,
            server=server,
            host=host,
            exclude_dserver=exclude_dserver,
        )
        dev_names = [dev.name for dev in devices]
        device_rows = _ls_columns(dev_names, nb_cols=nb_cols)
        click.echo(_table(device_rows))


@device_group.command("table")
@device_filter
@class_filter
@server_filter
@host_filter
@color
@dserver
def device_table(device, class_, server, host, color, exclude_dserver):
    """
    Show table of devices.

    Many filters with expression matching supported (device, server, host, device class)

    Example:

    \b
    $ tangoctl device list -d sys/[dt]*
    Name                  Alias    Class       Server           Host            Exported
    sys/database/2        ---      DataBase    DataBaseds/2     pb01.cells.es   Exported
    sys/database/3        ---      DataBase    DataBaseds/3     pb02.cells.es   Not. Exp.
    sys/database/test     ---      DataBaseds  DataBaseds/test  pb01.cells.es   Exported
    sys/taurus_test/1     ---      PyDsTaurus  PyDsTaurus/test  pc157.cells.es  Not. Exp.
    sys/tg_test/01        ---      TangoTest   TangoTest/01     pb01.cells.es   Exported
    sys/tg_test/02        ---      TangoTest   TangoTest/02     pb01.cells.es   Not. Exp.
    sys/tg_test/03        ---      TangoTest   TangoTest/03     pb01.cells.es   Not. Exp.
    sys/tg_test/1         ---      TangoTest   TangoTest/test   pb01.cells.es   Exported
    sys/tg_test/useles    ---      Useless     Useless/Useless  pb01.cells.es   Not. Exp.
    """
    with error():
        db = None  # TODO: determine DB
        db_info = tangoctl.get_db_info(db=db)
        devices = tangoctl.iter_devices(
            db=db,
            device=device,
            klass=class_,
            server=server,
            host=host,
            exclude_dserver=exclude_dserver,
        )
        table = []
        for dev in devices:
            srv = db_info.servers[dev.server]
            row = [
                _device_str(dev, color),
                _alias_str(dev, color),
                _device_class_str(dev, color),
                _server_str(srv, color),
                _server_host_str(srv, color),
                _device_exported_str(dev, color),
            ]
            table.append(row)
        headers = ["Name", "Alias", "Class", "Server", "Host", "Exported"]
        click.echo(_table(table, headers=headers))


@device_group.command("tree", help="show tree of devices")
@device_filter
@class_filter
@server_filter
@host_filter
@color
@verbose
@dserver
def device_tree(device, class_, server, host, color, verbose, exclude_dserver):
    """
    Show a tree of devices.

    Examples:

    \b
    $ tangoctl device tree -s "TangoTest/*"
    pb01.cells.es:10000
    ├── tcoutinho
    │   └── bl13pilatus
    │       └── test
    ├── sys
    │   └── tg_test
    │       ├── 01
    │       └── 01
    ├── tango
    │   └── test
    │       └── pc113test
    ├── tangotest
    │   ├── jandreu
    │   │   └── 01
    │   └── unittest
    │       ├── temp-1
    │       ├── temp-2
    │       └── temp-3
    ├── test
    │   └── device
    │       ├── 3
    │       ├── fulvio
    │       └── mrosanes
    └── zreszela
        └── tg_test
            └── 1
    """
    with error():
        db = None
        db_info = tangoctl.get_db_info(db=db)

        import treelib

        tree = treelib.Tree()
        db_node = tree.create_node(db_info.name)
        all_servers = db_info.servers
        devices = tangoctl.iter_devices(
            device=device,
            klass=class_,
            server=server,
            host=host,
            exclude_dserver=exclude_dserver,
            db=db,
        )
        domains = collections.defaultdict(
            functools.partial(collections.defaultdict, dict)
        )
        for dev in devices:
            d, f, m = dev.name.split("/")
            domains[d.lower()][f.lower()][m.lower()] = dev
        if color:
            VERBOSE_TEMPLATE = "{:30} {:30} {:35} {:40} {:40} {}"
        else:
            VERBOSE_TEMPLATE = "{:30} {:15} {:20} {:25} {:25} {}"
        for domain in sorted(domains):
            d_node = tree.create_node(_device_str(domain, color), parent=db_node)
            families = domains[domain]
            for family in sorted(families):
                f_node = tree.create_node(_device_str(family, color), parent=d_node)
                members = families[family]
                for member in sorted(members):
                    if verbose:
                        dev = members[member]
                        srv = all_servers[dev.server]
                        text = VERBOSE_TEMPLATE.format(
                            _device_str(member, color),
                            _alias_str(dev, color),
                            _device_class_str(dev, color),
                            _server_str(srv, color),
                            _server_host_str(srv, color),
                            _device_exported_str(dev, color),
                        )
                    else:
                        text = member
                    tree.create_node(text, parent=f_node)
        click.echo(str(tree))


@device_group.command("ping", help="ping device(s) (supports pattern matching *,?,[])")
@devices
@color
@dserver
def device_ping(devices, color, exclude_dserver):
    """
    Ping device(s).

    Example:

    \b
    $ tangoctl device ping -d sys/*
    sys/access_control/1           not exported
    sys/profile/AdlinkIODS         not exported
    sys/database/2                 1175 us
    sys/database/3                 not exported
    sys/tg_test/1                  912 us
    sys/tg_test/useless            not exported
    sys/taurus_test/1              not exported
    sys/tg_test/02                 not exported
    sys/tg_test/03                 not exported
    sys/database/test              failed to connect
    sys/profile/droldan            not exported
    sys/tg_test/01                 failed to connect
    sys/profile/controls01         2212 us
    """
    with error():
        devices = tuple(
            tangoctl.expr_to_idevices(devices, exclude_dserver=exclude_dserver)
        )
        if not devices:
            click.echo("no device matches the given pattern")
            return
        device_names = [device.name for device in devices]
        size = max(map(len, device_names))
        template = "{{:{}}} ".format(size)
        for dev_name, value in tangoctl.device_ping(device_names):
            if isinstance(value, Exception):
                msg = tangoctl.tango_error_str(value)
                if "not exported" in msg:
                    msg = "not exported"
                elif "Failed to connect" in msg:
                    msg = "failed to connect"
            else:
                msg = "{} us".format(value)
            click.echo(template.format(dev_name), nl=False)
            click.secho(msg, color=color, fg=_time_color(value))


@device_group.command("add")
@server
@pair_class_device
def device_add(server, device):
    """
    Registers new device(s).

    Each device must be in the format "<class> <name>" where name must
    follow the usual <domain>/<family>/<member>.

    Example:

    \b
    $ tangoctl device add -s TangoTest/demo -d TangoTest the/demo/device1 -d TangoTest the/demo/device2
    Registered the/demo/device1 in TangoTest/demo
    Registered the/demo/device2 in TangoTest/demo
    """
    with error():
        for serv, dev in tangoctl.device_add(server, device):
            click.echo("Registered {} in {}".format(dev, serv))


@device_group.command("delete", help="unregisters device(s)")
@devices
def device_delete(devices):
    """
    Unregisters devices(s)

    \b
    $ tangoctl device delete -d the/demo/device1 -d the/demo/device2
    """
    with error():
        tangoctl.device_delete(devices)


@device_group.group("alias")
def device_alias():
    """device alias operations(add/remove/show)"""


@device_alias.command("show")
@device
def device_alias_show(device):
    """show the alias for the given device"""
    click.echo(tangoctl.alias_from_device(device))

@device_alias.command("add")
@device
@click.argument('alias', type=str)
def device_alias_add(device, alias):
    """set the alias for the given device"""
    tangoctl.set_device_alias(device, alias)


@device_alias.command("remove")
@click.argument('alias', type=str)
def device_alias_remove(device, alias):
    """unregister the alias from the database"""
    tangoctl.remove_device_alias(alias)


@device_group.group("command")
def device_command():
    """
    Command related operations (exec, info, ...).
    """
    pass


@device_command.command("exec")
@device
@cmd
@click.option("-p", "--parameter", help="command parameter")
def device_command_exec(device, command, parameter):
    """Execute a specific command"""
    with error():
        click.echo(str(tangoctl.device_command(device, command, parameter)))


@device_command.command("list")
@device
@nb_cols
def device_command_list(device, nb_cols):
    """Show list of commands."""
    with error():
        cmds = tangoctl.device_commands(device)
        cmd_names = [cmd.cmd_name for cmd in cmds]
        cmd_rows = _ls_columns(cmd_names, nb_cols=nb_cols)
        click.echo(_table(cmd_rows))


@device_command.command("table")
@device
def device_command_table(device):
    """Show table of device commands."""
    rows = []
    with error():
        for cmd in tangoctl.device_commands(device):
            arg = tangoctl.type_str(cmd.in_type)
            res = tangoctl.type_str(cmd.out_type)
            rows.append((cmd.cmd_name, arg, res))
        click.echo(_table(rows, headers=["Name", "Argument", "Return"]))


@device_command.command("info")
@device
@cmd
def device_command_info(device, command):
    """Information about a command."""
    with error():
        click.echo(str(tangoctl.device_command_info(device, command)))


@device_group.group("attribute")
def device_attribute():
    """Attribute related operations (read, write, info, ...)."""
    pass


@device_attribute.command("read")
@device
@attrs_filter
@color
def device_attribute_read(device, attribute, color):
    """Read a attribute(s) from device."""
    with error():
        rows = []
        for dev_name, values in tangoctl.attributes_read({device: attribute}):
            if isinstance(values, Exception):
                msg = tangoctl.tango_error_str(values)
                click.secho(msg, fg="red", color=color)
            else:
                for value in values:
                    value_str, fg = tangoctl.attr_value_str_color(value)
                    if color:
                        value_str = click.style(value_str, fg=fg)
                    rows.append((value["name"], value_str))
        click.echo(_table(rows))


@device_attribute.command("write")
@device
@attr
@value
def device_attribute_write(device, attribute, value):
    """Write an attribute."""
    with error():
        click.echo(tangoctl.device_attribute_write(device, attribute, value))


@device_attribute.command("info")
@device
@attr
def device_attribute_info(device, attribute):
    """Show information about an attribute."""
    with error():
        info = _attribute_info_table(device, attribute)
        click.echo(_table(info))


@device_attribute.command("list")
@device
@nb_cols
def device_attribute_list(device, nb_cols):
    """Show list of device attributes."""
    with error():
        attrs = tangoctl.device_attributes(device)
        attr_names = [attr.name for attr in attrs]
        attr_rows = _ls_columns(attr_names, nb_cols=nb_cols)
        click.echo(_table(attr_rows))


@device_attribute.command("table")
@device
def device_attribute_table(device):
    """Show table of device attributes."""
    with error():
        rows = []
        for attr in tangoctl.device_attributes(device):
            atype = tangoctl.type_str(attr.data_type, attr.data_format)
            rows.append((attr.name, atype, tangoctl.access_str(attr.writable)))
        click.echo(_table(rows))


@device_group.group("property")
def device_property():
    """Device property related operations."""
    pass


@device_property.command("read")
@device
@props_filter
def device_property_read(device, property):
    """Read device property(ies)."""
    rows = []
    with error():
        props = tangoctl.device_properties_read(device, property)
        for name in sorted(props):
            value = props[name]
            if len(value) == 1:
                value = value[0]
            rows.append((name, value))
        click.echo(_table(rows))


@device_property.command("write")
@device
@prop
@click.option("-v", "--value", required=True, prompt=True, help="value to write")
def device_property_write(device, property, value):
    """Write device property."""
    with error():
        click.echo(tangoctl.device_property_write(device, property, value))


@device_property.command("list")
@device
@nb_cols
def device_property_list(device, nb_cols):
    """Show list of device properties and the corresponding value."""
    with error():
        prop_names = tangoctl.device_property_list(device)
        rows = _ls_columns(prop_names, nb_cols=nb_cols)
        click.echo(_table(rows))


@device_group.command("info")
@device
def device_info(device):
    """
    Show information about a device.

    Example:

    \b
    $ tangoctl device info -d sys/tg_test/1
           class = TangoTest
        exported = 1
            host = pb01.cells.es
              ip = 84.89.246.82
    last started = 21st February 2019 at 12:06:48
    last stopped = 27th June 2017 at 15:05:05
            name = sys/tg_test/1
             pid = 8839
            port = 43393
          server = TangoTest/test
         version = 4
    """
    with error():
        dinfo = tangoctl.device_info(device)
        templ = "{{:>{}}} = {{}}".format(max(map(len, dinfo)))
        lines = [templ.format(name, dinfo[name]) for name in sorted(dinfo)]
        click.echo("\n".join(lines))


@cli.group("server")
def server_group():
    """
    Server related operations (list, tree, add, delete, ...)
    """
    pass


@server_group.command("list")
@server_filter
@nb_cols
def server_list(server, nb_cols):
    """
    Show list of servers.

    Example:

    \b
    $ tangoctl server list -s Lima*
    LimaCCDs/Pilatus         LimaCCDs/adscTest
    LimaCCDs/Prosilica       LimaCCDs/basler
    LimaCCDs/Simulator       LimaCCDs/imxpad2
    LimaCCDs/Simulator_test  LimaCCDs/tcoutinho
    """
    with error():
        servers = list(tangoctl.iter_servers(server=server))
        server_names = [s.name for s in servers]
        server_rows = _ls_columns(server_names, nb_cols=nb_cols)
        click.echo(_table(server_rows))


@server_group.command("ilist")
@server_type
@server_instance_filter
@nb_cols
def server_instance_list(server_type, server_instance, nb_cols):
    """
    Show list of server instances of a given TYPE

    Example:

    \b
    $ tangoctl server ilist -t TangoTest
    Pilatus         adscTest
    Prosilica       basler
    Simulator       imxpad2
    Simulator_test  tcoutinho
    """
    with error():
        servers = list(
            tangoctl.iter_servers(
                server_type=server_type, server_instance=server_instance
            )
        )
        server_instances = [s.instance for s in servers]
        server_rows = _ls_columns(server_instances, nb_cols=nb_cols)
        click.echo(_table(server_rows))


@server_group.command("stop")
@servers
def server_stop(servers):
    with error():
        server_names = tuple(tangoctl.expr_to_iservers(servers))
        if not server_names:
            click.echo("no server matches the given pattern")
            return
        raise NotImplementedError


@server_group.command("ping")
@servers
@color
def server_ping(servers, color):
    """
    Ping server(s).

    Example:

    \b
    $ tangoctl server ping -s TangoTest/1 -s LimaCCDs/*
    TangoTest/1             1127 us
    LimaCCDs/Simulator      724 us
    LimaCCDs/basler1        not exported
    LimaCCDs/imxpad2        failed to connect
    """
    with error():
        server_names = tuple(tangoctl.expr_to_iservers(servers))
        if not server_names:
            click.echo("no server matches the given pattern")
            return
        size = max(map(len, server_names))
        template = "{{:{}}} ".format(size)
        for server_name, value in tangoctl.server_ping(server_names):
            if isinstance(value, Exception):
                msg = tangoctl.tango_error_str(value)
                if "not exported" in msg:
                    msg = "not exported"
                elif "Failed to connect" in msg:
                    msg = "failed to connect"
            else:
                msg = "{} us".format(value)
            click.echo(template.format(server_name), nl=False)
            click.secho(msg, color=color, fg=_time_color(value))


@server_group.command("add")
@server
@pair_class_device
def server_add(server, device):
    """
    Registers a new server in with the given list of DEVICES.

    Each device must be in the format "<class> <name>" where name
    must follow the usual <domain>/<family>/<member>

    Example:

    \b
    $ tangoctl server add -s TangoTest/demo -d TangoTest the/demo/device1 -d TangoTest the/demo/device2
    Registered the/demo/device1 in TangoTest/demo
    Registered the/demo/device2 in TangoTest/demo
    """
    with error():
        for serv, dev in tangoctl.server_add(server, device):
            click.echo("Registered {} in {}".format(dev, serv))


@server_group.command("delete")
@servers
@color
def server_delete(servers, color):
    """
    Unregister existing server(s).

    Examples:

    Delete a server:

    $ tangoctl server delete -s TangoTest/1

    Delete multiple servers:

    $ tangoctl server delete -s TangoTest/1 -s LimaCCDs/basler1
    """
    with error():
        for server in servers:
            click.echo("Deleting {}... ".format(server), nl=False)
            try:
                tangoctl.server_delete(server)
                click.secho("[DONE]", fg="green", color=color)
            except Exception as err:
                msg = " ({})".format(tangoctl.tango_error_str(err, stack_message=0))
                click.secho("[ERROR]", fg="red", color=color, nl=False)
                click.echo(msg)


@server_group.command("info")
@server
def server_info(server):
    """
    Show information about a server.

    Example:

    \b
    $ tangoctl server info -s TangoTest/1
        exported = 1
            host = pb01.cells.es
              ip = 84.89.246.82
    last started = 21st February 2019 at 12:06:34
    last stopped = 24th February 2017 at 11:25:37
            name = TangoTest/1
             pid = 8365
            port = 57256
         version = 4
    """
    with error():
        sinfo = tangoctl.server_info(server)
        templ = "{{:>{}}} = {{}}".format(max(map(len, sinfo)))
        lines = [templ.format(name, sinfo[name]) for name in sorted(sinfo)]
        click.echo("\n".join(lines))


@server_group.command("tree")
@click.option(
    "-c",
    "--compact",
    default=False,
    show_default=True,
    is_flag=True,
    help="compact tree (server type and server instance in same node)",
)
@click.option(
    "--server-only",
    default=False,
    show_default=True,
    is_flag=True,
    help="don't show devices",
)
@server_filter
@server_type_filter
@server_instance_filter
@dserver
def server_tree(
    compact, server_only, server, server_type, server_instance, exclude_dserver
):
    """
    Show a tree of servers.

    Examples:

    \b
    $ tangoctl server tree -s "TangoTest/*"
    pb01.cells.es:10000
    └── TangoTest
        ├── 01
        │   └── sys/tg_test/01
        ├── 02
        │   ├── sys/tg_test/demo1
        │   └── sys/tg_test/demo2
        └── tcoutinho
            ├── sys/tg_test/tc1
            ├── sys/tg_test/tc2
            └── sys/tg_test/tc3
    """
    db = None
    db_info = tangoctl.get_db_info(db=db)
    db_name = db_info.name

    import treelib

    tree = treelib.Tree()
    db_node = tree.create_node(db_name)
    servers = tangoctl.iter_servers(
        server=server, server_type=server_type, server_instance=server_instance, db=db
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
    click.echo(str(tree))


@cli.group("attribute")
def attribute_group():
    """
    Device attribute related operations (read, write, info, ...)
    """
    pass


@attribute_group.command("read")
@device
@attrs_filter
@color
def attribute_read(device, attribute, color):
    """Read an attribute."""
    with error():
        rows = []
        for dev_name, values in tangoctl.attributes_read({device: attribute}):
            if isinstance(values, Exception):
                msg = tangoctl.tango_error_str(values)
                click.secho(msg, fg="red", color=color)
            else:
                for value in values:
                    value_str, fg = tangoctl.attr_value_str_color(value)
                    if color:
                        value_str = click.style(value_str, fg=fg)
                    rows.append((value["name"], value_str))
        click.echo(_table(rows))


@attribute_group.command("write")
@device
@attr
@value
def attribute_write(device, attribute, value):
    """Write an attribute."""
    with error():
        click.echo(tangoctl.device_attribute_write(device, attribute, value))


@attribute_group.command("info")
@device
@attr
def attribute_info(device, attribute):
    """Show information about an attribute."""
    with error():
        info = _attribute_info_table(device, attribute)
        click.echo(_table(info))


@cli.group("command")
def command_group():
    """
    Device command related operations (list, exec, info, ...)
    """
    pass


@command_group.command("exec", help="execute specified command")
@device
@cmd
@click.option("-p", "--parameter")
def command_exec(device, command, parameter):
    """Execute a specific command."""
    with error():
        click.echo(str(tangoctl.device_command(device, command, parameter)))


@cli.group("starter")
def starter_group():
    """
    Starter server related operations (list, stop, start, ...)
    """
    pass


@starter_group.command("tree")
@starter_filter
@server_filter
@server_type_filter
@server_instance_filter
@click.option(
    "--all",
    default=False,
    show_default=True,
    is_flag=True,
    help="include not controlled servers",
)
def starter_tree(starter, server, server_type, server_instance, all):
    """
    Show a tree of starters.

    Examples:

    \b
    $ tangoctl starter tree --starter "ibl04*"
    pb01.cells.es:10000
    └── ibl0401
        ├── level 1
        │   └── TangoTest/test
        ├── level 2
        │   ├── CryoCooler/cryo1
        │   └── Vacuum/OH
        └── level 3
            ├── Vacuum/EH
            ├── Sardana/BL04
            └── Lima/basler-01
    """
    db = None
    db_info = tangoctl.get_db_info(db=db)
    db_name = db_info.name

    import treelib

    tree = treelib.Tree()
    db_node = tree.create_node(db_name)
    starters = list(tangoctl.iter_starters(starter_name=starter, db=db))
    starters_servers = tangoctl.starters_servers(*starters)
    for starter in starters:
        level_servers = collections.defaultdict(list)
        servers = starters_servers[starter]
        fg = "red" if servers is None else "green"
        name = click.style(starter.name, fg=fg)
        starter_node = tree.create_node(name, parent=db_node)
        servers = servers.values() if servers else []
        servers = tangoctl.iter_starter_servers(
            servers, server, server_type, server_instance
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
                if state == "ON":
                    color = "green"
                elif state == "FAULT":
                    color = "red"
                elif state == "MOVING":
                    color = "blue"
                else:
                    color = "magenta"
                label = click.style(starter_server["name"], fg=color)
                tree.create_node(label, parent=level_node)

    click.echo(str(tree))


def _starter_stop(
    starter, server, server_type, server_instance, timeout, stop_timeout, dry_run
):
    if dry_run:
        click.secho("Making a dry run!", bold=True, fg="red")
    try:
        tangoctl.starter_stop_servers(
            starter_name=starter,
            server_name=server,
            server_type=server_type,
            server_instance=server_instance,
            timeout=timeout,
            stop_timeout=stop_timeout,
            dry_run=dry_run,
        )
    except gevent.Timeout:
        click.secho("Operation timeout ({} s)".format(timeout), fg="yellow")


def _starter_start(starter, server, server_type, server_instance, timeout, dry_run):
    if dry_run:
        click.secho("Making a dry run!", bold=True, fg="red")
    try:
        tangoctl.starter_start_servers(
            starter_name=starter,
            server_name=server,
            server_type=server_type,
            server_instance=server_instance,
            timeout=timeout,
            dry_run=dry_run,
        )
    except gevent.Timeout:
        click.secho("Operation timeout ({} s)".format(timeout), fg="yellow")


def _starter_restart(starter, server, server_type, server_instance, timeout, dry_run):
    # TODO: if no filter provided ask if really want to do it
    if dry_run:
        click.secho("Making a dry run!", bold=True, fg="red")
    try:
        tangoctl.starter_restart_servers(
            starter_name=starter,
            server_name=server,
            server_type=server_type,
            server_instance=server_instance,
            timeout=timeout,
            dry_run=dry_run,
        )
    except gevent.Timeout:
        click.secho("Operation timeout ({} s)".format(timeout), fg="yellow")


@starter_group.command("stop")
@starter_filter
@server_filter
@server_type_filter
@server_instance_filter
@timeout
@stop_timeout
@dry_run
def starter_stop(
    starter, server, server_type, server_instance, timeout, stop_timeout, dry_run
):
    """Stop selected servers.

    Servers which are reported to be stopped are skipped.

    Servers registered in higher levels are stopped first.

    Servers at the same level are stopped in parallel.

    (level-1) servers are stopped only when all higher level servers
    have been stopped.
    """
    return _starter_stop(
        starter, server, server_type, server_instance, timeout, stop_timeout, dry_run
    )


@starter_group.command("start")
@starter_filter
@server_filter
@server_type_filter
@server_instance_filter
@timeout
@dry_run
def starter_start(starter, server, server_type, server_instance, timeout, dry_run):
    """Start selected servers.

    Servers which are reported to be started are skipped.

    Servers registered in lower levels are started first.

    Servers at the same level are started in parallel.

    (level+1) servers are started only when all lower level servers
    have been started.
    """
    return _starter_start(starter, server, server_type, server_instance, timeout, dry_run)


@starter_group.command("restart")
@starter_filter
@server_filter
@server_type_filter
@server_instance_filter
@timeout
@dry_run
def starter_restart(starter, server, server_type, server_instance, timeout, dry_run):
    """Restart selected servers.

    The process of starting selected servers only starts after all
    have been stopped.

    When stopping:

        Servers which are reported to be stopped are skipped.

        Servers registered in higher levels are stopped first.

        Servers at the same level are stopped in parallel.

        (level-1) servers are stopped only when all higher level servers
        have been stopped.

    When starting:

        Servers which are reported to be started are skipped.

        Servers registered in lower levels are started first.

        Servers at the same level are started in parallel.

        (level+1) servers are started only when all lower level servers
        have been started.
    """
    return _starter_restart(starter, server, server_type, server_instance, timeout, dry_run)


if __name__ == "__main__":
    cli()
