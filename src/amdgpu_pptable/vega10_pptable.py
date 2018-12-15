import collections
import ctypes
import logging

from .generated.vega10_pptable import *


LOG = logging.getLogger(__name__)


class UnknownRevId(KeyError):
    pass


def parse_subtable(buffer, offset, type_select):
    header = Vega10_PPTable_Generic_SubTable_Header.from_buffer(buffer, offset)
    return type_select(header.ucRevId).from_buffer(buffer, offset)


def parse_array_subtable(buffer, offset, subtable_type, type_select=None):
    entries_name, entries_type = subtable_type._fields_[-1]
    assert entries_type._length_ == 1

    header = subtable_type.from_buffer(buffer, offset)

    if type_select is None:
        entry_type = entries_type._type_
    else:
        entry_type = type_select(header.ucRevId)

    class DynamicArraySubtable(ctypes.LittleEndianStructure):
        _pack_ = subtable_type._pack_
        _fields_ = subtable_type._fields_[:-1] + [(entries_name, entry_type * header.ucNumEntries)]

    DynamicArraySubtable.__name__ = f'{subtable_type.__name__}[{header.ucNumEntries}]'
    DynamicArraySubtable.__qualname__ = f'{subtable_type.__qualname__}[{header.ucNumEntries}]'

    return DynamicArraySubtable.from_buffer(buffer, offset)


def fan_table_type(rev_id):
    if rev_id == 10:
        return ATOM_Vega10_Fan_Table
    elif rev_id > 10:
        return ATOM_Vega10_Fan_Table_V2
    else:
        raise UnknownRevId(rev_id)


def powertune_table_type(rev_id):
    if rev_id == 5:
        return ATOM_Vega10_PowerTune_Table
    elif rev_id == 6:
        return ATOM_Vega10_PowerTune_Table_V2
    else:
        return ATOM_Vega10_PowerTune_Table_V3


def gfxclk_record_type(rev_id):
    if rev_id == 0:
        return ATOM_Vega10_GFXCLK_Dependency_Record
    elif rev_id == 1:
        return ATOM_Vega10_GFXCLK_Dependency_Record_V2
    else:
        raise UnknownRevId(rev_id)


def parse(buffer):
    main_table = ATOM_Vega10_POWERPLAYTABLE.from_buffer(buffer)
    parse_result = {'Table': main_table}

    def subtable(name, parse_func, *args, **kwargs):
        offset = getattr(main_table, f'us{name}Offset')
        if offset > 0:
            try:
                parse_result[name] = parse_func(buffer, offset, *args, **kwargs)
            except UnknownRevId as ex:
                LOG.warning("%s: unknown ucRevId: %s", name, ex.args[0])

    subtable('StateArray', parse_array_subtable, ATOM_Vega10_State_Array)
    subtable('SocclkDependencyTable', parse_array_subtable, ATOM_Vega10_SOCCLK_Dependency_Table)
    subtable('MclkDependencyTable', parse_array_subtable, ATOM_Vega10_MCLK_Dependency_Table)
    subtable('GfxclkDependencyTable', parse_array_subtable, ATOM_Vega10_GFXCLK_Dependency_Table, gfxclk_record_type)
    subtable('DcefclkDependencyTable', parse_array_subtable, ATOM_Vega10_DCEFCLK_Dependency_Table)
    subtable('PixclkDependencyTable', parse_array_subtable, ATOM_Vega10_PIXCLK_Dependency_Table)
    subtable('DispClkDependencyTable', parse_array_subtable, ATOM_Vega10_DISPCLK_Dependency_Table)
    subtable('PhyClkDependencyTable', parse_array_subtable, ATOM_Vega10_PHYCLK_Dependency_Table)
    subtable('VddcLookupTable', parse_array_subtable, ATOM_Vega10_Voltage_Lookup_Table)
    subtable('VddmemLookupTable', parse_array_subtable, ATOM_Vega10_Voltage_Lookup_Table)
    subtable('VddciLookupTable', parse_array_subtable, ATOM_Vega10_Voltage_Lookup_Table)
    subtable('MMDependencyTable', parse_array_subtable, ATOM_Vega10_MM_Dependency_Table)
    subtable('VCEStateTable', parse_array_subtable, ATOM_Vega10_VCE_State_Table)
    subtable('HardLimitTable', parse_array_subtable, ATOM_Vega10_Hard_Limit_Table)
    subtable('PCIETable', parse_array_subtable, ATOM_Vega10_PCIE_Table)

    subtable('FanTable', parse_subtable, fan_table_type)
    subtable('PowerTuneTable', parse_subtable, powertune_table_type)
    subtable('ThermalController', parse_subtable, lambda _: ATOM_Vega10_Thermal_Controller)

    return collections.namedtuple('ParseResult', parse_result.keys())(*parse_result.values())
