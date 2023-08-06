# coding: utf-8
###############################################################################
# (C) Copyright 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                             #
# This file may be distributed under the terms of the License                 #
# Agreement provided with this software.                                      #
#                                                                             #
# THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
# INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
# FITNESS FOR A PARTICULAR PURPOSE.                                           #
###############################################################################
from typing import List, Optional, Iterable
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from pumpkin_supmcu.supmcu import request_module_definition, \
        SupMCUModuleDefinition, \
        TelemetryType, \
        SupMCUMaster, \
        SupMCUTelemetryDefinition, \
        SupMCUHDR, \
        TelemetryDataItem, \
        SupMCUTelemetry, \
        DataType
from .types import SupMCUModuleTelemetrySet, Telemetry, ModuleDefinition
from pumpkin_supmcu.i2c import I2CMaster

VERSION_TEL_IDX = 0
I2C_BLACKLIST = [0x68]


def export_dataclass(data: Iterable[dataclass], file: Path = None) -> Optional[str]:
    """
    Exports a list of dataclasses objects to a JSON file or stdout

    :param telemetry: an the telemetry data to export
    :param file: the filename to save the data as. If not included, it returns a JSON string
    """
    if file is None:
        return json.dumps([asdict(item) for item in data])
    else:
        with file.open("w") as f:
            json.dump([asdict(item) for item in data], f)


def import_bus_telemetry(file: Path) -> List[SupMCUModuleTelemetrySet]:
    """
    Imports a JSON file of telemetry data into a list of :any:`SupMCUModuleTelemetrySet`

    :param file: the JSON file to read the telemetry data from
    :return: a list of of imported :any:`SupMCUModuleTelemetrySet`
    """
    with file.open("r") as f:
        raw_telemetry = json.load(f)
    return parse_bus_telemetry(raw_telemetry)


def parse_bus_telemetry(raw_telemetry: dict) -> List[SupMCUModuleTelemetrySet]:
    """
    Parses a dictionary of telemetry data into a list of :any:`SupMCUModuleTelemetrySet`

    :param raw_telemetry: the telemetry data to parse
    :return: a list of parsed :any:`SupMCUModuleTelemetrySet`
    """
    for i, module in enumerate(raw_telemetry):
        for x, telem in enumerate(module['supmcu_telemetry']):
            telem['sup_telemetry']['header'] = SupMCUHDR(**telem['sup_telemetry']['header'])
            for y, item in enumerate(telem['sup_telemetry']['items']):
                item['data_type'] = DataType(item['data_type'])
                telem['sup_telemetry']['items'][y] = item
            telem['sup_telemetry']['items'] = [TelemetryDataItem(**item) for item in telem['sup_telemetry']['items']]
            telem['sup_telemetry'] = SupMCUTelemetry(**telem['sup_telemetry'])
            telem['type'] = TelemetryType(telem['type'])
            telem['simulatable'] = bool(telem['simulatable'])
            module['supmcu_telemetry'][x] = Telemetry(**telem)
        for x, telem in enumerate(module['module_telemetry']):
            telem['sup_telemetry']['header'] = SupMCUHDR(**telem['sup_telemetry']['header'])
            for y, item in enumerate(telem['sup_telemetry']['items']):
                item['data_type'] = DataType(item['data_type'])
                telem['sup_telemetry']['items'][y] = item
            telem['sup_telemetry']['items'] = [TelemetryDataItem(**item) for item in telem['sup_telemetry']['items']]
            telem['sup_telemetry'] = SupMCUTelemetry(**telem['sup_telemetry'])
            telem['type'] = TelemetryType(telem['type'])
            telem['simulatable'] = bool(telem['simulatable'])
            module['module_telemetry'][x] = Telemetry(**telem)
        raw_telemetry[i] = SupMCUModuleTelemetrySet(**module)
    return raw_telemetry


def import_bus_telemetry_definition(file: Path) -> List[ModuleDefinition]:
    """
    Imports a JSON file of telemetry definitions into a list of :any:`ModuleDefinition` objects

    :param file: the JSON file to read the telemetry definition from
    :return: the list of imported :any:`ModuleDefinition` telemetry
    """
    with file.open("r") as f:
        raw_telemetry = json.load(f)
    definitions = parse_bus_telemetry_definition(raw_telemetry)
    return definitions


def parse_bus_telemetry_definition(raw_telemetry: dict) -> List[ModuleDefinition]:
    """
    Parses a dictionary of definitions into a list of :any:`ModuleDefinition` objects

    :param raw_telemetry: the telemetry dictionary to parse
    :return: the list of :any:`ModuleDefinition` telemetry data
    """
    for telem in raw_telemetry:
        # Iterates over each telemetry definition dict and creates a SupMCUTelemetryDefinition out of it
        telem['definition']['supmcu_telemetry'] = {index: SupMCUTelemetryDefinition(**item) for index, item in telem['definition']['supmcu_telemetry'].items()}
        telem['definition']['module_telemetry'] = {index: SupMCUTelemetryDefinition(**item) for index, item in telem['definition']['module_telemetry'].items()}
        # Creates a SupMCUModuleDefinition from the "definition" dict
        telem['definition'] = SupMCUModuleDefinition(**telem['definition'])
    return [ModuleDefinition(**telem) for telem in raw_telemetry]


def discover_bus_telemetry(master: I2CMaster, addresses: Optional[Iterable[int]] = None, blacklist: Iterable[int] = []) \
        -> List[ModuleDefinition]:
    """
    Discovers all of the telemetry on the SupMCU bus.

    :param master: The I2C master device to use.
    :param addresses: The list of addresses to use for the bus. If `None`, master must support the `scan_bus` function.
    :param blacklist: A list of addresses to not scan
    :return: List of SupMCU Module definitions.
    """
    if addresses is None:
        addresses = master.get_bus_devices()
    blacklist += I2C_BLACKLIST
    addresses = [addr for addr in addresses if addr not in blacklist]
    return [discover_module_telemetry(master, addr) for addr in addresses]


def discover_module_telemetry(master: I2CMaster, address: int) -> ModuleDefinition:
    """
    Discovers all of the telemetry of a module at `address`.

    :param master: The I2C master device to use.
    :param address: The I2C address to use for the bus.
    :return: The SupMCU Module definition.
    """
    mod_def = request_module_definition(master, address)
    master = SupMCUMaster(master, [mod_def])
    version = master.request_telemetry(address, TelemetryType.SupMCU, VERSION_TEL_IDX).items[0].value
    return ModuleDefinition(version, mod_def)
