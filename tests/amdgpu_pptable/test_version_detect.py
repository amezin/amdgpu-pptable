import pkg_resources

import pytest

import amdgpu_pptable.version_detect
import amdgpu_pptable.vega10_pptable
import amdgpu_pptable.pptable_v1_0
import amdgpu_pptable.smu_v11_0_pptable_navi10


@pytest.mark.parametrize('pptable_file,expected_type', [
    ('rx580_pulse_pp_table', amdgpu_pptable.pptable_v1_0.ATOM_Tonga_POWERPLAYTABLE),
    ('vega64_nitro_oc_pp_table', amdgpu_pptable.vega10_pptable.ATOM_Vega10_POWERPLAYTABLE),
    ('5700xt_gaming_x/pp_table', amdgpu_pptable.smu_v11_0_pptable_navi10.struct_smu_11_0_powerplay_table),
    ('5700xt_nitro_se/pp_table', amdgpu_pptable.smu_v11_0_pptable_navi10.struct_smu_11_0_powerplay_table)
])
def test_type(pptable_file, expected_type):
    with open(pkg_resources.resource_filename(__name__, pptable_file), 'rb') as f:
        orig_buffer = f.read()

    buffer = bytearray(orig_buffer)
    pptable = amdgpu_pptable.version_detect.parse(buffer)

    assert type(pptable.Main) is expected_type
