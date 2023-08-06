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

from dataclasses import dataclass
from pumpkin_supmcu.supmcu import SupMCUTelemetry, TelemetryType, typeof_supmcu_fmt_char, \
        SupMCUHDR, TelemetryDataItem, DataType, SupMCUTelemetryDefinition, \
        SupMCUModuleDefinition
from typing import List


_data_type_default_value = {
    DataType.Str: '',
    DataType.Char: '',  # char
    DataType.UINT8: 0,  # uint8_t
    DataType.INT8: 0,  # int8_t
    DataType.UINT16: 0,  # uint16_t
    DataType.INT16: 0,  # int16_t
    DataType.UINT32: 0,  # uint32_t
    DataType.INT32: 0,  # int32_t
    DataType.UINT64: 0,  # uint64_t
    DataType.INT64: 0,  # int64_t
    DataType.Float: 0.0,  # float
    DataType.Double: 0.0,  # double
    DataType.Hex8: 0x0,  # uint8_t (hex)
    DataType.Hex16: 0x0,  # uint16_t (hex)
}


@dataclass
class ModuleDefinition(object):
    version: str
    definition: SupMCUModuleDefinition


@dataclass
class Telemetry(object):
    """Contains a :any:`SupMCUTelemetry` object along with some metadata"""
    idx: int
    name: str
    size: int
    type: TelemetryType
    simulatable: bool
    sup_telemetry: SupMCUTelemetry

    @classmethod
    def from_definition(cls, definition: SupMCUTelemetryDefinition, tel_type: TelemetryType) -> dataclass:
        fmt = definition.format.replace(".", ",").split(",")
        fmt = [typeof_supmcu_fmt_char(f) for f in fmt]
        tel = SupMCUTelemetry(
            SupMCUHDR(True, -1),
            []
        )
        for idx, data_type in enumerate(fmt):
            item = TelemetryDataItem(data_type, 0, "0")
            if definition.simulatable:
                item.set_value(definition.defaults[idx])
            else:
                item.set_value(_data_type_default_value[data_type])
            tel.items.append(item)

        return cls(
            definition.idx,
            definition.name,
            definition.telemetry_length,
            tel_type,
            definition.simulatable,
            tel
        )


@dataclass
class SupMCUModuleTelemetrySet(object):
    """Like a :any:`SupMCUModuleDefinition` but with actual :any:`Telemetry` data instead of :any:`SupMCUTelemetryDefinition`"""
    name: str
    cmd_name: str
    address: int
    version: str
    supmcu_telemetry: List[Telemetry]
    module_telemetry: List[Telemetry]

    @classmethod
    def from_definition(cls, module_def: ModuleDefinition) -> dataclass:
        return cls(
            module_def.definition.name,
            module_def.definition.cmd_name,
            module_def.definition.address,
            module_def.version,
            [Telemetry.from_definition(new_def, TelemetryType.SupMCU) for new_def in module_def.definition.supmcu_telemetry.values()],
            [Telemetry.from_definition(new_def, TelemetryType.Module) for new_def in module_def.definition.module_telemetry.values()]
        )
