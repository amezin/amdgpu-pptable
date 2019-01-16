import pkg_resources

import pytest

import amdgpu_pptable.version_detect
import amdgpu_pptable.vega10_pptable
import amdgpu_pptable.pptable_v1_0


@pytest.mark.parametrize('pptable_file,expected_type', [
    ('rx580_pulse_pp_table', amdgpu_pptable.pptable_v1_0.ATOM_Tonga_POWERPLAYTABLE),
    ('vega64_nitro_oc_pp_table', amdgpu_pptable.vega10_pptable.ATOM_Vega10_POWERPLAYTABLE)
])
def test_type(pptable_file, expected_type):
    with open(pkg_resources.resource_filename(__name__, pptable_file), 'rb') as f:
        orig_buffer = f.read()

    buffer = bytearray(orig_buffer)
    pptable = amdgpu_pptable.version_detect.parse(buffer)

    assert type(pptable.Main) is expected_type
