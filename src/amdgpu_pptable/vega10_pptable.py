import collections
import ctypes
import logging

from .generated.vega10_pptable import *


LOG = logging.getLogger(__name__)


class UnknownRevId(KeyError):
    pass


def select_by_rev_id(header, rev_id_dict):
    try:
        return rev_id_dict[header.ucRevId]
    except KeyError as ex:
        raise UnknownRevId(header.ucRevId) from ex


def parse_subtable(buffer, offset, rev_id_dict):
    header = Vega10_PPTable_Generic_SubTable_Header.from_buffer(buffer, offset)
    subtable_type = select_by_rev_id(header, rev_id_dict)
    return subtable_type.from_buffer(buffer, offset)


def parse_array_subtable(buffer, offset, subtable_type, rev_id_dict=None):
    entries_name, entries_type = subtable_type._fields_[-1]
    assert entries_type._length_ == 1

    if rev_id_dict is None:
        rev_id_dict = {0: entries_type._type_}

    header = subtable_type.from_buffer(buffer, offset)
    entry_type = select_by_rev_id(header, rev_id_dict)

    class DynamicArraySubtable(ctypes.LittleEndianStructure):
        _pack_ = subtable_type._pack_
        _fields_ = subtable_type._fields_[:-1] + [(entries_name, entry_type * header.ucNumEntries)]
        __name__ = f'{subtable_type.__name__}[{header.ucNumEntries}]'
        __qualname__ = f'{subtable_type.__qualname__}[{header.ucNumEntries}]'

    return DynamicArraySubtable.from_buffer(buffer, offset)


def parse(buffer):
    main_table = ATOM_Vega10_POWERPLAYTABLE.from_buffer(buffer)
    parse_result = {'Table': main_table}

    def subtable(name, parse_func, *args, **kwargs):
        offset = getattr(main_table, f'us{name}Offset')
        if offset > 0:
            try:
                parse_result[name] = parse_func(buffer, offset, *args, **kwargs)
                return

            except UnknownRevId as ex:
                LOG.warning("%s: unknown ucRevId: %s", name, ex.args[0])

        parse_result[name] = None

    subtable('StateArray', parse_array_subtable, ATOM_Vega10_State_Array,
             {
                 2: ATOM_Vega10_State
             })
    subtable('FanTable', parse_subtable,
             {
                 10: ATOM_Vega10_Fan_Table,
                 11: ATOM_Vega10_Fan_Table_V2
             })
    subtable('ThermalController', parse_subtable,
             {
                 1: ATOM_Vega10_Thermal_Controller
             })
    subtable('SocclkDependencyTable', parse_array_subtable, ATOM_Vega10_SOCCLK_Dependency_Table)
    subtable('MclkDependencyTable', parse_array_subtable, ATOM_Vega10_MCLK_Dependency_Table,
             {
                 1: ATOM_Vega10_MCLK_Dependency_Record
             })
    subtable('GfxclkDependencyTable', parse_array_subtable, ATOM_Vega10_GFXCLK_Dependency_Table,
             {
                 0: ATOM_Vega10_GFXCLK_Dependency_Record,
                 1: ATOM_Vega10_GFXCLK_Dependency_Record_V2
             })
    subtable('DcefclkDependencyTable', parse_array_subtable, ATOM_Vega10_DCEFCLK_Dependency_Table)
    subtable('PixclkDependencyTable', parse_array_subtable, ATOM_Vega10_PIXCLK_Dependency_Table)
    subtable('DispClkDependencyTable', parse_array_subtable, ATOM_Vega10_DISPCLK_Dependency_Table)
    subtable('PhyClkDependencyTable', parse_array_subtable, ATOM_Vega10_PHYCLK_Dependency_Table)
    subtable('VddcLookupTable', parse_array_subtable, ATOM_Vega10_Voltage_Lookup_Table,
             {
                 1: ATOM_Vega10_Voltage_Lookup_Record
             })
    subtable('VddmemLookupTable', parse_array_subtable, ATOM_Vega10_Voltage_Lookup_Table,
             {
                 1: ATOM_Vega10_Voltage_Lookup_Record
             })
    subtable('VddciLookupTable', parse_array_subtable, ATOM_Vega10_Voltage_Lookup_Table,
             {
                 1: ATOM_Vega10_Voltage_Lookup_Record
             })
    subtable('MMDependencyTable', parse_array_subtable, ATOM_Vega10_MM_Dependency_Table,
             {
                 1: ATOM_Vega10_MM_Dependency_Record
             })
    subtable('VCEStateTable', parse_array_subtable, ATOM_Vega10_VCE_State_Table)
    subtable('HardLimitTable', parse_array_subtable, ATOM_Vega10_Hard_Limit_Table)
    subtable('PCIETable', parse_array_subtable, ATOM_Vega10_PCIE_Table,
             {
                 2: ATOM_Vega10_PCIE_Record
             })
    subtable('PowerTuneTable', parse_subtable,
             {
                 5: ATOM_Vega10_PowerTune_Table,
                 6: ATOM_Vega10_PowerTune_Table_V2,
                 7: ATOM_Vega10_PowerTune_Table_V3
             })

    return collections.namedtuple('ParseResult', parse_result.keys())(*parse_result.values())
