import pkg_resources

import amdgpu_pptable.vega10_pptable


def test_load():
    with open(pkg_resources.resource_filename(__name__, 'vega64_nitro_oc_pp_table'), 'rb') as f:
        orig_buffer = f.read()

    buffer = bytearray(orig_buffer)
    pptable = amdgpu_pptable.vega10_pptable.parse(buffer)

    assert orig_buffer == buffer

    assert pptable.FanTable.ucRevId == 11
    assert pptable.FanTable.usFanAcousticLimitRpm == 1500

    assert len(pptable.SocclkDependencyTable.entries) == pptable.SocclkDependencyTable.ucNumEntries
    assert pptable.SocclkDependencyTable.entries[0].ulClk == 60000
    assert pptable.SocclkDependencyTable.entries[7].ulClk == 110700
    assert pptable.GfxclkDependencyTable.entries[7].ulClk == 163000
    assert pptable.GfxclkDependencyTable.entries[7].ucVddInd == 7

    assert pptable.PowerTuneTable.usSoftwareShutdownTemp == 91
    assert pptable.FanTable.ucFanMinRPM == 3
    assert pptable.FanTable.ucFanMaxRPM == 33

    assert list(e.ulMemClk / 100 for e in pptable.MclkDependencyTable.entries) == [167, 500, 800, 945]
    assert list(e.ulClk / 100 for e in pptable.GfxclkDependencyTable.entries) == \
        [852, 991, 1084, 1138, 1200, 1401, 1536, 1630]

    pptable.FanTable.usMinimumPWMLimit = 14
    pptable.FanTable.ucEnableZeroRPM = 0

    assert orig_buffer != buffer
