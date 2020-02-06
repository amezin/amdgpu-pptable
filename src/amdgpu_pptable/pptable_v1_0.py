import collections
import ctypes
import logging

from .generated.pptable_v1_0 import *


LOG = logging.getLogger(__name__)


def parse_table(buffer, offset, type_select):
    header = PPTable_Generic_SubTable_Header.from_buffer(buffer, offset)
    return type_select(header.ucRevId).from_buffer(buffer, offset)


def parse_array_table(buffer, offset, type_select=None):
    table = parse_table(buffer, offset, type_select)

    entries_name, entries_type = table.__class__._fields_[-1]
    assert entries_type._length_ == 1

    class DynamicArrayTable(ctypes.LittleEndianStructure):
        _pack_ = table.__class__._pack_
        _fields_ = table.__class__._fields_[:-1] + [(entries_name, entries_type._type_ * table.ucNumEntries)]
        wrapped_type = table.__class__

    return DynamicArrayTable.from_buffer(buffer, offset)


def fan_table_type(rev_id):
    if rev_id < 8:
        return ATOM_Tonga_Fan_Table
    else:
        return ATOM_Fiji_Fan_Table


def sclk_table_type(rev_id):
    if rev_id < 1:
        return ATOM_Tonga_SCLK_Dependency_Table
    else:
        return ATOM_Polaris_SCLK_Dependency_Table


def powertune_table_type(rev_id):
    if rev_id < 3:
        return ATOM_Tonga_PowerTune_Table
    else:
        return ATOM_Fiji_PowerTune_Table


def pcie_table_type(rev_id):
    if rev_id < 1:
        return ATOM_Tonga_PCIE_Table
    else:
        return ATOM_Polaris10_PCIE_Table


def parse(buffer):
    main_table = ATOM_Tonga_POWERPLAYTABLE.from_buffer(buffer)
    parse_result = {'Main': main_table}

    def table(name, parse_func, *args, **kwargs):
        offset = getattr(main_table, f'us{name}Offset')
        if offset > 0:
            parse_result[name] = parse_func(buffer, offset, *args, **kwargs)

    table('StateArray', parse_array_table, lambda _: ATOM_Tonga_State_Array)
    table('SclkDependencyTable', parse_array_table, sclk_table_type)
    table('MclkDependencyTable', parse_array_table, lambda _: ATOM_Tonga_MCLK_Dependency_Table)
    table('MMDependencyTable', parse_array_table, lambda _: ATOM_Tonga_MM_Dependency_Table)
    table('VddcLookupTable', parse_array_table, lambda _: ATOM_Tonga_Voltage_Lookup_Table)
    table('VddgfxLookupTable', parse_array_table, lambda _: ATOM_Tonga_Voltage_Lookup_Table)
    table('VCEStateTable', parse_array_table, lambda _: ATOM_Tonga_VCE_State_Table)
    table('HardLimitTable', parse_array_table, lambda _: ATOM_Tonga_Hard_Limit_Table)
    table('PCIETable', parse_array_table, pcie_table_type)

    table('FanTable', parse_table, fan_table_type)
    table('PowerTuneTable', parse_table, powertune_table_type)
    table('ThermalController', parse_table, lambda _: ATOM_Tonga_Thermal_Controller)
    table('PPMTable', parse_table, lambda _: ATOM_Tonga_PPM_Table)
    table('GPIOTable', parse_table, lambda _: ATOM_Tonga_GPIO_Table)

    return collections.namedtuple('ParseResult', parse_result.keys())(*parse_result.values())
