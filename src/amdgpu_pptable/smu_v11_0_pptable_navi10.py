import collections
import ctypes
import logging

from .generated.smu_v11_0_pptable_navi10 import *


LOG = logging.getLogger(__name__)


def parse(buffer):
    main_table = struct_smu_11_0_powerplay_table.from_buffer(buffer)
    parse_result = {'Main': main_table}
    return collections.namedtuple('ParseResult', parse_result.keys())(**parse_result)
