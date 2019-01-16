from . import pptable_v1_0, vega10_pptable


class UnknownTableRevision(KeyError):
    pass


def parse(buffer):
    header = pptable_v1_0.struct__ATOM_COMMON_TABLE_HEADER.from_buffer(buffer)

    if header.ucTableFormatRevision == pptable_v1_0.ATOM_Tonga_TABLE_REVISION_TONGA:
        return pptable_v1_0.parse(buffer)

    if header.ucTableFormatRevision == vega10_pptable.ATOM_Vega10_TABLE_REVISION_VEGA10:
        return vega10_pptable.parse(buffer)

    raise UnknownTableRevision(header.ucTableFormatRevision)
