#include "vega10powerplaytable.h"

#include <cstdint>

#include "linux_headers/atom-types.h"
#include "linux_headers/atomfirmware.h"
#include "linux_headers/vega10_pptable.h"

#define ADD_FIELD(x, ptr) add_field(#x, (ptr)->x)
#define ADD_CHILD_TABLE(t, tp, off, ptr) parse_child<tp>((t), #tp "(" #off ")", (ptr), ((ptr)->off))

static std::unique_ptr<Table> parse(ATOM_Vega10_Fan_Table *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucRevId, ptr);
    t->ADD_FIELD(usFanOutputSensitivity, ptr);
    t->ADD_FIELD(usFanRPMMax, ptr);
    t->ADD_FIELD(usThrottlingRPM, ptr);
    t->ADD_FIELD(usFanAcousticLimit, ptr);
    t->ADD_FIELD(usTargetTemperature, ptr);
    t->ADD_FIELD(usMinimumPWMLimit, ptr);
    t->ADD_FIELD(usTargetGfxClk, ptr);
    t->ADD_FIELD(usFanGainEdge, ptr);
    t->ADD_FIELD(usFanGainHotspot, ptr);
    t->ADD_FIELD(usFanGainLiquid, ptr);
    t->ADD_FIELD(usFanGainVrVddc, ptr);
    t->ADD_FIELD(usFanGainVrMvdd, ptr);
    t->ADD_FIELD(usFanGainPlx, ptr);
    t->ADD_FIELD(usFanGainHbm, ptr);
    t->ADD_FIELD(ucEnableZeroRPM, ptr);
    t->ADD_FIELD(usFanStopTemperature, ptr);
    t->ADD_FIELD(usFanStartTemperature, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_Fan_Table_V2 *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucRevId, ptr);
    t->ADD_FIELD(usFanOutputSensitivity, ptr);
    t->ADD_FIELD(usFanAcousticLimitRpm, ptr);
    t->ADD_FIELD(usThrottlingRPM, ptr);
    t->ADD_FIELD(usTargetTemperature, ptr);
    t->ADD_FIELD(usMinimumPWMLimit, ptr);
    t->ADD_FIELD(usTargetGfxClk, ptr);
    t->ADD_FIELD(usFanGainEdge, ptr);
    t->ADD_FIELD(usFanGainHotspot, ptr);
    t->ADD_FIELD(usFanGainLiquid, ptr);
    t->ADD_FIELD(usFanGainVrVddc, ptr);
    t->ADD_FIELD(usFanGainVrMvdd, ptr);
    t->ADD_FIELD(usFanGainPlx, ptr);
    t->ADD_FIELD(usFanGainHbm, ptr);
    t->ADD_FIELD(ucEnableZeroRPM, ptr);
    t->ADD_FIELD(usFanStopTemperature, ptr);
    t->ADD_FIELD(usFanStartTemperature, ptr);
    t->ADD_FIELD(ucFanParameters, ptr);
    t->ADD_FIELD(ucFanMinRPM, ptr);
    t->ADD_FIELD(ucFanMaxRPM, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_Thermal_Controller *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucRevId, ptr);
    t->ADD_FIELD(ucType, ptr);
    t->ADD_FIELD(ucI2cLine, ptr);
    t->ADD_FIELD(ucI2cAddress, ptr);
    t->ADD_FIELD(ucFanParameters, ptr);
    t->ADD_FIELD(ucFanMinRPM, ptr);
    t->ADD_FIELD(ucFanMaxRPM, ptr);
    t->ADD_FIELD(ucFlags, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_State *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucSocClockIndexHigh, ptr);
    t->ADD_FIELD(ucSocClockIndexLow, ptr);
    t->ADD_FIELD(ucGfxClockIndexHigh, ptr);
    t->ADD_FIELD(ucGfxClockIndexLow, ptr);
    t->ADD_FIELD(ucMemClockIndexHigh, ptr);
    t->ADD_FIELD(ucMemClockIndexLow, ptr);
    t->ADD_FIELD(usClassification, ptr);
    t->ADD_FIELD(ulCapsAndSettings, ptr);
    t->ADD_FIELD(usClassification2, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_CLK_Dependency_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ulClk, ptr);
    t->ADD_FIELD(ucVddInd, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_MCLK_Dependency_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ulMemClk, ptr);
    t->ADD_FIELD(ucVddInd, ptr);
    t->ADD_FIELD(ucVddMemInd, ptr);
    t->ADD_FIELD(ucVddciInd, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_GFXCLK_Dependency_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ulClk, ptr);
    t->ADD_FIELD(ucVddInd, ptr);
    t->ADD_FIELD(usCKSVOffsetandDisable, ptr);
    t->ADD_FIELD(usAVFSOffset, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_GFXCLK_Dependency_Record_V2 *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ulClk, ptr);
    t->ADD_FIELD(ucVddInd, ptr);
    t->ADD_FIELD(usCKSVOffsetandDisable, ptr);
    t->ADD_FIELD(usAVFSOffset, ptr);
    t->ADD_FIELD(ucACGEnable, ptr);
    t->ADD_FIELD(ucReserved[0], ptr);
    t->ADD_FIELD(ucReserved[1], ptr);
    t->ADD_FIELD(ucReserved[2], ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_Voltage_Lookup_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(usVdd, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_MM_Dependency_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucVddcInd, ptr);
    t->ADD_FIELD(ulDClk, ptr);
    t->ADD_FIELD(ulVClk, ptr);
    t->ADD_FIELD(ulEClk, ptr);
    t->ADD_FIELD(ulPSPClk, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_VCE_State_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucVCEClockIndex, ptr);
    t->ADD_FIELD(ucFlag, ptr);
    t->ADD_FIELD(ucSCLKIndex, ptr);
    t->ADD_FIELD(ucMCLKIndex, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_Hard_Limit_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ulSOCCLKLimit, ptr);
    t->ADD_FIELD(ulGFXCLKLimit, ptr);
    t->ADD_FIELD(ulMCLKLimit, ptr);
    t->ADD_FIELD(usVddcLimit, ptr);
    t->ADD_FIELD(usVddciLimit, ptr);
    t->ADD_FIELD(usVddMemLimit, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_PCIE_Record *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ulLCLK, ptr);
    t->ADD_FIELD(ucPCIEGenSpeed, ptr);
    t->ADD_FIELD(ucPCIELaneWidth, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_PowerTune_Table *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucRevId, ptr);
    t->ADD_FIELD(usSocketPowerLimit, ptr);
    t->ADD_FIELD(usBatteryPowerLimit, ptr);
    t->ADD_FIELD(usSmallPowerLimit, ptr);
    t->ADD_FIELD(usTdcLimit, ptr);
    t->ADD_FIELD(usEdcLimit, ptr);
    t->ADD_FIELD(usSoftwareShutdownTemp, ptr);
    t->ADD_FIELD(usTemperatureLimitHotSpot, ptr);
    t->ADD_FIELD(usTemperatureLimitLiquid1, ptr);
    t->ADD_FIELD(usTemperatureLimitLiquid2, ptr);
    t->ADD_FIELD(usTemperatureLimitHBM, ptr);
    t->ADD_FIELD(usTemperatureLimitVrSoc, ptr);
    t->ADD_FIELD(usTemperatureLimitVrMem, ptr);
    t->ADD_FIELD(usTemperatureLimitPlx, ptr);
    t->ADD_FIELD(usLoadLineResistance, ptr);
    t->ADD_FIELD(ucLiquid1_I2C_address, ptr);
    t->ADD_FIELD(ucLiquid2_I2C_address, ptr);
    t->ADD_FIELD(ucVr_I2C_address, ptr);
    t->ADD_FIELD(ucPlx_I2C_address, ptr);
    t->ADD_FIELD(ucLiquid_I2C_LineSCL, ptr);
    t->ADD_FIELD(ucLiquid_I2C_LineSDA, ptr);
    t->ADD_FIELD(ucVr_I2C_LineSCL, ptr);
    t->ADD_FIELD(ucVr_I2C_LineSDA, ptr);
    t->ADD_FIELD(ucPlx_I2C_LineSCL, ptr);
    t->ADD_FIELD(ucPlx_I2C_LineSDA, ptr);
    t->ADD_FIELD(usTemperatureLimitTedge, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_PowerTune_Table_V2 *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucRevId, ptr);
    t->ADD_FIELD(usSocketPowerLimit, ptr);
    t->ADD_FIELD(usBatteryPowerLimit, ptr);
    t->ADD_FIELD(usSmallPowerLimit, ptr);
    t->ADD_FIELD(usTdcLimit, ptr);
    t->ADD_FIELD(usEdcLimit, ptr);
    t->ADD_FIELD(usSoftwareShutdownTemp, ptr);
    t->ADD_FIELD(usTemperatureLimitHotSpot, ptr);
    t->ADD_FIELD(usTemperatureLimitLiquid1, ptr);
    t->ADD_FIELD(usTemperatureLimitLiquid2, ptr);
    t->ADD_FIELD(usTemperatureLimitHBM, ptr);
    t->ADD_FIELD(usTemperatureLimitVrSoc, ptr);
    t->ADD_FIELD(usTemperatureLimitVrMem, ptr);
    t->ADD_FIELD(usTemperatureLimitPlx, ptr);
    t->ADD_FIELD(usLoadLineResistance, ptr);
    t->ADD_FIELD(ucLiquid1_I2C_address, ptr);
    t->ADD_FIELD(ucLiquid2_I2C_address, ptr);
    t->ADD_FIELD(ucLiquid_I2C_Line, ptr);
    t->ADD_FIELD(ucVr_I2C_address, ptr);
    t->ADD_FIELD(ucPlx_I2C_address, ptr);
    t->ADD_FIELD(ucVr_I2C_Line, ptr);
    t->ADD_FIELD(ucPlx_I2C_Line, ptr);
    t->ADD_FIELD(usTemperatureLimitTedge, ptr);
    return t;
}

static std::unique_ptr<Table> parse(ATOM_Vega10_PowerTune_Table_V3 *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucRevId, ptr);
    t->ADD_FIELD(usSocketPowerLimit, ptr);
    t->ADD_FIELD(usBatteryPowerLimit, ptr);
    t->ADD_FIELD(usSmallPowerLimit, ptr);
    t->ADD_FIELD(usTdcLimit, ptr);
    t->ADD_FIELD(usEdcLimit, ptr);
    t->ADD_FIELD(usSoftwareShutdownTemp, ptr);
    t->ADD_FIELD(usTemperatureLimitHotSpot, ptr);
    t->ADD_FIELD(usTemperatureLimitLiquid1, ptr);
    t->ADD_FIELD(usTemperatureLimitLiquid2, ptr);
    t->ADD_FIELD(usTemperatureLimitHBM, ptr);
    t->ADD_FIELD(usTemperatureLimitVrSoc, ptr);
    t->ADD_FIELD(usTemperatureLimitVrMem, ptr);
    t->ADD_FIELD(usTemperatureLimitPlx, ptr);
    t->ADD_FIELD(usLoadLineResistance, ptr);
    t->ADD_FIELD(ucLiquid1_I2C_address, ptr);
    t->ADD_FIELD(ucLiquid2_I2C_address, ptr);
    t->ADD_FIELD(ucLiquid_I2C_Line, ptr);
    t->ADD_FIELD(ucVr_I2C_address, ptr);
    t->ADD_FIELD(ucPlx_I2C_address, ptr);
    t->ADD_FIELD(ucVr_I2C_Line, ptr);
    t->ADD_FIELD(ucPlx_I2C_Line, ptr);
    t->ADD_FIELD(usTemperatureLimitTedge, ptr);
    t->ADD_FIELD(usBoostStartTemperature, ptr);
    t->ADD_FIELD(usBoostStopTemperature, ptr);
    t->ADD_FIELD(ulBoostClock, ptr);
    t->ADD_FIELD(Reserved[0], ptr);
    t->ADD_FIELD(Reserved[1], ptr);
    return t;
}

template<typename T, typename E>
static std::unique_ptr<Table> parse_array(T *ptr, const std::string &name, E *elem)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucRevId, ptr);
    t->ADD_FIELD(ucNumEntries, ptr);

    for (int i = 0; i < ptr->ucNumEntries; i++) {
        t->tables[name + "[" + FieldBase::to_string(i) + "]"] = parse(&elem[i]);
    }

    return t;
}

template<typename T>
static std::unique_ptr<Table> parse(T *ptr)
{
    return parse_array(ptr, "entries", ptr->entries);
}

static std::unique_ptr<Table> parse(ATOM_Vega10_State_Array *ptr)
{
    return parse_array(ptr, "states", ptr->states);
}

static std::unique_ptr<Table> parse(ATOM_Vega10_GFXCLK_Dependency_Table *ptr)
{
    if (ptr->ucRevId == 0) {
        return parse_array(ptr, "entries", ptr->entries);
    } else if (ptr->ucRevId == 1) {
        return parse_array(ptr, "states", reinterpret_cast<ATOM_Vega10_GFXCLK_Dependency_Record_V2 *>(ptr->entries));
    } else {
        return std::unique_ptr<Table>(new Table());
    }
}

static Vega10_PPTable_Generic_SubTable_Header *generic_subtable_header(void *base, ptrdiff_t offset)
{
    if (!offset) {
        return nullptr;
    }

    return reinterpret_cast<Vega10_PPTable_Generic_SubTable_Header *>(reinterpret_cast<char *>(base) + offset);
}

template<typename T>
void parse_child(Table &t, std::string child_name, void *base, ptrdiff_t child_offset)
{
    auto ptr = reinterpret_cast<T *>(generic_subtable_header(base, child_offset));
    if (!ptr) {
        return;
    }

    t.tables[child_name] = parse(ptr);
}

static std::unique_ptr<Table> parse(ATOM_Vega10_POWERPLAYTABLE *ptr)
{
    std::unique_ptr<Table> t(new Table());
    t->ADD_FIELD(ucTableRevision, ptr);
    t->ADD_FIELD(usTableSize, ptr);
    t->ADD_FIELD(ulGoldenPPID, ptr);
    t->ADD_FIELD(ulGoldenRevision, ptr);
    t->ADD_FIELD(usFormatID, ptr);
    t->ADD_FIELD(ulPlatformCaps, ptr);
    t->ADD_FIELD(ulMaxODEngineClock, ptr);
    t->ADD_FIELD(ulMaxODMemoryClock, ptr);
    t->ADD_FIELD(usPowerControlLimit, ptr);
    t->ADD_FIELD(usUlvVoltageOffset, ptr);
    t->ADD_FIELD(usUlvSmnclkDid, ptr);
    t->ADD_FIELD(usUlvMp1clkDid, ptr);
    t->ADD_FIELD(usUlvGfxclkBypass, ptr);
    t->ADD_FIELD(usGfxclkSlewRate, ptr);
    t->ADD_FIELD(ucGfxVoltageMode, ptr);
    t->ADD_FIELD(ucSocVoltageMode, ptr);
    t->ADD_FIELD(ucUclkVoltageMode, ptr);
    t->ADD_FIELD(ucUvdVoltageMode, ptr);
    t->ADD_FIELD(ucVceVoltageMode, ptr);
    t->ADD_FIELD(ucMp0VoltageMode, ptr);
    t->ADD_FIELD(ucDcefVoltageMode, ptr);
    t->ADD_FIELD(usReserve, ptr);

    ADD_CHILD_TABLE(*t, ATOM_Vega10_State_Array, usStateArrayOffset, ptr);

    if (ptr->usFanTableOffset) {
        auto header = generic_subtable_header(ptr, ptr->usFanTableOffset);
        if (header->ucRevId == 10) {
            ADD_CHILD_TABLE(*t, ATOM_Vega10_Fan_Table, usFanTableOffset, ptr);
        } else if (header->ucRevId > 10) {
            ADD_CHILD_TABLE(*t, ATOM_Vega10_Fan_Table_V2, usFanTableOffset, ptr);
        }
    }

    ADD_CHILD_TABLE(*t, ATOM_Vega10_Thermal_Controller, usThermalControllerOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_SOCCLK_Dependency_Table, usSocclkDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_MCLK_Dependency_Table, usMclkDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_GFXCLK_Dependency_Table, usGfxclkDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_DCEFCLK_Dependency_Table, usDcefclkDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_PIXCLK_Dependency_Table, usPixclkDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_DISPCLK_Dependency_Table, usDispClkDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_PHYCLK_Dependency_Table, usPhyClkDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_Voltage_Lookup_Table, usVddcLookupTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_Voltage_Lookup_Table, usVddmemLookupTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_Voltage_Lookup_Table, usVddciLookupTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_MM_Dependency_Table, usMMDependencyTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_VCE_State_Table, usVCEStateTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_Hard_Limit_Table, usHardLimitTableOffset, ptr);
    ADD_CHILD_TABLE(*t, ATOM_Vega10_PCIE_Table, usPCIETableOffset, ptr);

    if (ptr->usPowerTuneTableOffset) {
        auto header = generic_subtable_header(ptr, ptr->usPowerTuneTableOffset);
        if (header->ucRevId == 5) {
            ADD_CHILD_TABLE(*t, ATOM_Vega10_PowerTune_Table, usPowerTuneTableOffset, ptr);
        } else if (header->ucRevId == 6) {
            ADD_CHILD_TABLE(*t, ATOM_Vega10_PowerTune_Table_V2, usPowerTuneTableOffset, ptr);
        } else {
            ADD_CHILD_TABLE(*t, ATOM_Vega10_PowerTune_Table_V3, usPowerTuneTableOffset, ptr);
        }
    }

    return t;
}

std::unique_ptr<Table> parse_vega10_pptable(void *p)
{
    return parse(reinterpret_cast<ATOM_Vega10_POWERPLAYTABLE *>(p));
}
