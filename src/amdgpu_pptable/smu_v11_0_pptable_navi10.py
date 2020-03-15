import collections
import enum
import logging

from .generated import smu_v11_0_pptable_navi10 as gen
from .generated.smu_v11_0_pptable_navi10 import *  # noqa: F401


LOG = logging.getLogger(__name__)


def _make_enum(name):
    return enum.IntEnum(
        name,
        {v: k for k, v in getattr(gen, f'{name}__enumvalues').items()},
        module=__name__
    )


SMU_11_0_ODFEATURE_CAP = _make_enum('SMU_11_0_ODFEATURE_CAP')
SMU_11_0_ODSETTING_ID = _make_enum('SMU_11_0_ODSETTING_ID')
SMU_11_0_PPCLOCK_ID = _make_enum('SMU_11_0_PPCLOCK_ID')


class ArrayDictAdapter(collections.abc.MutableMapping):
    index_type = int

    def __init__(self, array):
        self.data = array

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for key in range(len(self)):
            try:
                yield self.index_type(key)
            except ValueError:
                yield key

    @classmethod
    def make(cls, array, index_t=index_type):
        class DerivedArrayDictAdapter(cls):
            index_type = index_t
            wrapped_type = type(array)

        return DerivedArrayDictAdapter(array)


class struct_smu_11_0_overdrive_table(gen.struct_smu_11_0_overdrive_table):
    @property
    def min(self):
        return ArrayDictAdapter.make(super().min, SMU_11_0_ODSETTING_ID)

    @property
    def max(self):
        return ArrayDictAdapter.make(super().max, SMU_11_0_ODSETTING_ID)

    @property
    def cap(self):
        return ArrayDictAdapter.make(super().cap, SMU_11_0_ODFEATURE_CAP)


class struct_smu_11_0_power_saving_clock_table(gen.struct_smu_11_0_power_saving_clock_table):
    @property
    def min(self):
        return ArrayDictAdapter.make(super().min, SMU_11_0_PPCLOCK_ID)

    @property
    def max(self):
        return ArrayDictAdapter.make(super().max, SMU_11_0_PPCLOCK_ID)


class struct_smu_11_0_powerplay_table(gen.struct_smu_11_0_powerplay_table):
    @property
    def overdrive_table(self):
        return struct_smu_11_0_overdrive_table.from_buffer(super().overdrive_table)

    @property
    def power_saving_clock(self):
        return struct_smu_11_0_power_saving_clock_table.from_buffer(super().power_saving_clock)


def parse(buffer):
    main_table = struct_smu_11_0_powerplay_table.from_buffer(buffer)
    parse_result = {'Main': main_table}
    return collections.namedtuple('ParseResult', parse_result.keys())(**parse_result)


__all__ = gen.__all__ + [
    'parse'
]
