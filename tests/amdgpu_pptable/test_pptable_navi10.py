import pkg_resources
import pytest

import amdgpu_pptable.smu_v11_0_pptable_navi10


@pytest.mark.parametrize('table', ['5700xt_aorus', '5700xt_gaming_x', '5700xt_nitro_se'])
def test_parse_navi10(table):
    with open(pkg_resources.resource_filename(__name__, table + '/pp_table'), 'rb') as f:
        orig_buffer = f.read()

    buffer = bytearray(orig_buffer)
    amdgpu_pptable.smu_v11_0_pptable_navi10.parse(buffer)
