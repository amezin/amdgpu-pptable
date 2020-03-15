import pkg_resources

import amdgpu_pptable.pptable_v1_0


def test_load():
    with open(pkg_resources.resource_filename(__name__, 'rx580_pulse_pp_table'), 'rb') as f:
        orig_buffer = f.read()

    buffer = bytearray(orig_buffer)
    pptable = amdgpu_pptable.pptable_v1_0.parse(buffer)

    assert orig_buffer == buffer

    assert type(pptable.FanTable) is amdgpu_pptable.pptable_v1_0.ATOM_Fiji_Fan_Table
    assert type(pptable.SclkDependencyTable.entries[0]) is \
        amdgpu_pptable.pptable_v1_0.ATOM_Polaris_SCLK_Dependency_Record
    assert type(pptable.PCIETable.entries[0]) is amdgpu_pptable.pptable_v1_0.ATOM_Polaris10_PCIE_Record

    assert pptable.PowerTuneTable.usSoftwareShutdownTemp == 94
    assert pptable.PowerTuneTable.usMaximumPowerDeliveryLimit == 155
    assert pptable.ThermalController.ucFanMaxRPM == 32

    assert list(e.ulMclk / 100 for e in pptable.MclkDependencyTable.entries) == [300, 1000, 2000]
    assert list(e.ulSclk / 100 for e in pptable.SclkDependencyTable.entries) == \
        [300, 600, 900, 1145, 1215, 1257, 1300, 1366]

    pptable.FanTable.ucMinimumPWMLimit = 14

    assert orig_buffer != buffer
