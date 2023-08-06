# PyCO2SYS: marine carbonate system calculations in Python.
# Copyright (C) 2020  Matthew Paul Humphreys et al.  (GNU GPLv3)
"""Calculate one new carbonate system variable from various input pairs."""

from autograd import numpy as np
from .. import convert
from . import delta, initialise

pHTol = 1e-8  # tolerance for ending iterations in all pH solvers


def CarbfromTCH(TC, H, totals, k_constants):
    """Calculate carbonate ion from dissolved inorganic carbon and [H+].

    Based on CalculateCarbfromTCpH, version 01.0, 06-12-2019, by Denis Pierrot.
    """
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    return TC * K1 * K2 / (H ** 2 + K1 * H + K1 * K2)


def CarbfromTCpH(TC, pH, totals, k_constants):
    """Calculate carbonate ion from dissolved inorganic carbon and pH."""
    H = 10.0 ** -pH
    return CarbfromTCH(TC, H, totals, k_constants)


@np.errstate(invalid="ignore")
def HCO3fromTCH(TC, H, totals, k_constants):
    """Calculate bicarbonate ion from dissolved inorganic carbon and [H+]."""
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    return TC * K1 * H / (H ** 2 + K1 * H + K1 * K2)


def HCO3fromTCpH(TC, pH, totals, k_constants):
    """Calculate bicarbonate ion from dissolved inorganic carbon and pH."""
    H = 10.0 ** -pH
    return HCO3fromTCH(TC, H, totals, k_constants)


@np.errstate(invalid="ignore")
def AlkParts(TC, pH, FREEtoTOT, totals, k_constants):
    """Calculate the different components of total alkalinity from dissolved inorganic
    carbon and pH.

    Although coded for H on the Total pH scale, for the pH values occuring in seawater
    (pH > 6) this will be equally valid on any pH scale (i.e. H terms are negligible) as
    long as the K Constants are on that scale.

    Based on CalculateAlkParts, version 01.03, 10-10-97, by Ernie Lewis.
    """
    H = 10.0 ** -pH
    HCO3 = HCO3fromTCH(TC, H, totals, k_constants)
    CO3 = CarbfromTCH(TC, H, totals, k_constants)
    BAlk = totals["TB"] * k_constants["KB"] / (k_constants["KB"] + H)
    OH = k_constants["KW"] / H
    PAlk = (
        totals["TPO4"]
        * (
            k_constants["KP1"] * k_constants["KP2"] * H
            + 2 * k_constants["KP1"] * k_constants["KP2"] * k_constants["KP3"]
            - H ** 3
        )
        / (
            H ** 3
            + k_constants["KP1"] * H ** 2
            + k_constants["KP1"] * k_constants["KP2"] * H
            + k_constants["KP1"] * k_constants["KP2"] * k_constants["KP3"]
        )
    )
    SiAlk = totals["TSi"] * k_constants["KSi"] / (k_constants["KSi"] + H)
    NH3Alk = totals["TNH3"] * k_constants["KNH3"] / (k_constants["KNH3"] + H)
    H2SAlk = totals["TH2S"] * k_constants["KH2S"] / (k_constants["KH2S"] + H)
    Hfree = H / FREEtoTOT  # for H on the Total scale
    HSO4 = totals["TSO4"] / (
        1 + k_constants["KSO4"] / Hfree
    )  # since KSO4 is on the Free scale
    HF = totals["TF"] / (1 + k_constants["KF"] / Hfree)  # since KF is on the Free scale
    return {
        "HCO3": HCO3,
        "CO3": CO3,
        "BAlk": BAlk,
        "OH": OH,
        "PAlk": PAlk,
        "SiAlk": SiAlk,
        "NH3Alk": NH3Alk,
        "H2SAlk": H2SAlk,
        "Hfree": Hfree,
        "HSO4": HSO4,
        "HF": HF,
    }


def phosphate_components(pH, totals, k_constants):
    """Calculate the components of total phosphate."""
    tPO4 = totals["TPO4"]
    KP1 = k_constants["KP1"]
    KP2 = k_constants["KP2"]
    KP3 = k_constants["KP3"]
    h_scale = 10.0 ** -pH
    denom = h_scale ** 3 + KP1 * h_scale ** 2 + KP1 * KP2 * h_scale + KP1 * KP2 * KP3
    return {
        "PO4": tPO4 * KP1 * KP2 * KP3 / denom,
        "HPO4": tPO4 * KP1 * KP2 * h_scale / denom,
        "H2PO4": tPO4 * KP1 * h_scale ** 2 / denom,
        "H3PO4": tPO4 * h_scale ** 3 / denom,
    }


def alkalinity_phosphate(h_scale, totals, k_constants):
    """Calculate the contribution of phosphate components to total alkalinity."""
    # phosphate = phosphate_components(-np.log10(h_scale), totals, k_constants)
    # return 2 * phosphate["PO4"] + phosphate["HPO4"] - phosphate["H3PO4"]
    KP1 = k_constants["KP1"]
    KP2 = k_constants["KP2"]
    KP3 = k_constants["KP3"]
    return (
        totals["TPO4"]
        * (KP1 * KP2 * h_scale + 2 * KP1 * KP2 * KP3 - h_scale ** 3)
        / (h_scale ** 3 + KP1 * h_scale ** 2 + KP1 * KP2 * h_scale + KP1 * KP2 * KP3)
    )


@np.errstate(invalid="ignore")
def alkalinity_components(TC, pH, totals, k_constants):
    """Calculate the different components of total alkalinity from dissolved inorganic
    carbon and pH.

    This is currently not used in the default CO2SYS but it will eventually replace the
    existing AlkParts function.

    Based on CalculateAlkParts by Ernie Lewis.
    """
    h_scale = 10.0 ** -pH  # on the pH scale declared by the user
    HCO3 = HCO3fromTCH(TC, h_scale, totals, k_constants)
    CO3 = CarbfromTCH(TC, h_scale, totals, k_constants)
    BAlk = totals["TB"] * k_constants["KB"] / (k_constants["KB"] + h_scale)
    OH = k_constants["KW"] / h_scale
    PAlk = alkalinity_phosphate(h_scale, totals, k_constants)
    SiAlk = totals["TSi"] * k_constants["KSi"] / (k_constants["KSi"] + h_scale)
    NH3Alk = totals["TNH3"] * k_constants["KNH3"] / (k_constants["KNH3"] + h_scale)
    H2SAlk = totals["TH2S"] * k_constants["KH2S"] / (k_constants["KH2S"] + h_scale)
    # KSO4 and KF are always on the Free scale, so:
    h_free = h_scale * k_constants["pHfactor_to_Free"]
    HSO4 = totals["TSO4"] / (1 + k_constants["KSO4"] / h_free)
    HF = totals["TF"] / (1 + k_constants["KF"] / h_free)
    return {
        "HCO3": HCO3,
        "CO3": CO3,
        "BAlk": BAlk,
        "OH": OH,
        "PAlk": PAlk,
        "SiAlk": SiAlk,
        "NH3Alk": NH3Alk,
        "H2SAlk": H2SAlk,
        "Hfree": h_free,
        "HSO4": HSO4,
        "HF": HF,
    }


def TAfromTCpH_original(TC, pH, totals, k_constants):
    """Calculate total alkalinity from dissolved inorganic carbon and pH.

    This calculates TA from TC and pH.
    Though it is coded for H on the total pH scale, for the pH values occuring
    in seawater (pH > 6) it will be equally valid on any pH scale (H terms
    negligible) as long as the K Constants are on that scale.

    Based on CalculateTAfromTCpH, version 02.02, 10-10-97, by Ernie Lewis.
    """
    FREEtoTOT = convert.free2tot(totals, k_constants)
    alks = AlkParts(TC, pH, FREEtoTOT, totals, k_constants)
    TA = (
        alks["HCO3"]
        + 2 * alks["CO3"]
        + alks["BAlk"]
        + alks["OH"]
        + alks["PAlk"]
        + alks["SiAlk"]
        + alks["NH3Alk"]
        + alks["H2SAlk"]
        - alks["Hfree"]
        - alks["HSO4"]
        - alks["HF"]
    )
    return TA


def TAfromTCpH_fixed(TC, pH, totals, k_constants):
    """Calculate total alkalinity from dissolved inorganic carbon and pH.

    This calculates TA from TC and pH.
    It has been corrected to work properly on any pH scale.

    Based on CalculateTAfromTCpH, version 02.02, 10-10-97, by Ernie Lewis.
    """
    alks = alkalinity_components(TC, pH, totals, k_constants)
    TA = (
        alks["HCO3"]
        + 2 * alks["CO3"]
        + alks["BAlk"]
        + alks["OH"]
        + alks["PAlk"]
        + alks["SiAlk"]
        + alks["NH3Alk"]
        + alks["H2SAlk"]
        - alks["Hfree"]
        - alks["HSO4"]
        - alks["HF"]
    )
    return TA


# Set which alkalinity function to use
TAfromTCpH = TAfromTCpH_original


def TAfrompHfCO2(pH, fCO2, totals, k_constants):
    """Calculate total alkalinity from dissolved inorganic carbon and CO2 fugacity."""
    TC = TCfrompHfCO2(pH, fCO2, totals, k_constants)
    return TAfromTCpH(TC, pH, totals, k_constants)


def TCfrompHHCO3(pH, HCO3, totals, k_constants):
    """Calculate dissolved inorganic carbon from pH and bicarbonate ion.

    Follows ZW01 Appendix B (6).
    """
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    H = 10.0 ** -pH
    return HCO3 * (1 + H / K1 + K2 / H)


def TCfrompHCarb(pH, CARB, totals, k_constants):
    """Calculate dissolved inorganic carbon from pH and carbonate ion.

    Follows ZW01 Appendix B (7).
    """
    H = 10.0 ** -pH
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    return CARB * (1 + H / K2 + H ** 2 / (K1 * K2))


def TAfrompHCarb(pH, CARB, totals, k_constants):
    """Calculate total alkalinity from dissolved inorganic carbon and carbonate ion."""
    TC = TCfrompHCarb(pH, CARB, totals, k_constants)
    return TAfromTCpH(TC, pH, totals, k_constants)


def TAfrompHHCO3(pH, HCO3, totals, k_constants):
    """Calculate total alkalinity from dissolved inorganic carbon and bicarbonate ion.
    """
    TC = TCfrompHHCO3(pH, HCO3, totals, k_constants)
    return TAfromTCpH(TC, pH, totals, k_constants)


@np.errstate(invalid="ignore")
def _pHfromTAVX(TA, VX, totals, k_constants, initialfunc, deltafunc):
    """Calculate pH from total alkalinity and DIC or one of its components using a
    Newton-Raphson iterative method.

    Although it is coded for H on the total pH scale, for the pH values occuring in
    seawater (pH > 6) it will be equally valid on any pH scale (H terms negligible) as
    long as the K Constants are on that scale.

    Based on the CalculatepHfromTA* functions, version 04.01, Oct 96, by Ernie Lewis.
    """
    # First guess inspired by M13/OE15, added v1.3.0:
    pH = initialfunc(
        TA, VX, totals["TB"], k_constants["K1"], k_constants["K2"], k_constants["KB"]
    )
    deltapH = 1.0 + pHTol
    while np.any(np.abs(deltapH) >= pHTol):
        pHdone = np.abs(deltapH) < pHTol  # check which rows don't need updating
        deltapH = deltafunc(pH, TA, VX, totals, k_constants)  # the pH jump
        # To keep the jump from being too big:
        abs_deltapH = np.abs(deltapH)
        np.sign_deltapH = np.sign(deltapH)
        # Jump by 1 instead if `deltapH` > 5
        deltapH = np.where(abs_deltapH > 5.0, np.sign_deltapH, deltapH)
        # Jump by 0.5 instead if 1 < `deltapH` < 5
        deltapH = np.where(
            (abs_deltapH > 0.5) & (abs_deltapH <= 5.0), 0.5 * np.sign_deltapH, deltapH,
        )  # assumes that once we're within 1 of the correct pH, we will converge
        pH = np.where(pHdone, pH, pH + deltapH)  # only update rows that need it
    return pH


def pHfromTATC(TA, TC, totals, k_constants):
    """Calculate pH from total alkalinity and dissolved inorganic carbon."""
    return _pHfromTAVX(TA, TC, totals, k_constants, initialise.fromTC, delta.pHfromTATC)


def pHfromTAfCO2(TA, fCO2, totals, k_constants):
    """Calculate pH from total alkalinity and CO2 fugacity."""
    # Slightly more convoluted than the others because initialise.fromCO2 takes CO2 as
    # an input, while delta.pHfromTAfCO2 takes fCO2.
    return _pHfromTAVX(
        TA,
        fCO2,
        totals,
        k_constants,
        lambda TA, fCO2, TB, K1, K2, KB: initialise.fromCO2(
            TA, k_constants["K0"] * fCO2, TB, K1, K2, KB
        ),  # this just transforms initalise.fromCO2 to take fCO2 in place of CO2
        delta.pHfromTAfCO2,
    )


def pHfromTACarb(TA, CARB, totals, k_constants):
    """Calculate pH from total alkalinity and carbonate ion molinity."""
    return _pHfromTAVX(
        TA, CARB, totals, k_constants, initialise.fromCO3, delta.pHfromTACarb
    )


def pHfromTAHCO3(TA, HCO3, totals, k_constants):
    """Calculate pH from total alkalinity and bicarbonate ion molinity."""
    return _pHfromTAVX(
        TA, HCO3, totals, k_constants, initialise.fromHCO3, delta.pHfromTAHCO3
    )


def fCO2fromTCpH(TC, pH, totals, k_constants):
    """Calculate CO2 fugacity from dissolved inorganic carbon and pH.

    Based on CalculatefCO2fromTCpH, version 02.02, 12-13-96, by Ernie Lewis.
    """
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    H = 10.0 ** -pH
    return TC * H ** 2 / (H ** 2 + K1 * H + K1 * K2) / K0


@np.errstate(invalid="ignore")
def TCfromTApH(TA, pH, totals, k_constants):
    """Calculate dissolved inorganic carbon from total alkalinity and pH.

    This calculates TC from TA and pH.
    Though it is coded for H on the total pH scale, for the pH values occuring
    in seawater (pH > 6) it will be equally valid on any pH scale (H terms
    negligible) as long as the K Constants are on that scale.

    Based on CalculateTCfromTApH, version 02.03, 10-10-97, by Ernie Lewis.
    """
    TA_TC0_pH = TAfromTCpH(0.0, pH, totals, k_constants)
    F = TA_TC0_pH > TA
    if np.any(F):
        print("Some input pH values are impossibly high given the input alkalinity;")
        print("returning np.nan rather than negative DIC values.")
    CAlk = np.where(F, np.nan, TA - TA_TC0_pH)
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    H = 10.0 ** -pH
    TC = CAlk * (H ** 2 + K1 * H + K1 * K2) / (K1 * (H + 2 * K2))
    return TC


@np.errstate(divide="ignore", invalid="ignore")
def pHfromTCfCO2(TC, fCO2, totals, k_constants):
    """Calculate pH from dissolved inorganic carbon and CO2 fugacity.

    This calculates pH from TC and fCO2 using K0, K1, and K2 by solving the quadratic in
    H: fCO2*K0 = TC*H*H/(K1*H + H*H + K1*K2).
    If there is not a real root, then pH is returned as np.nan.

    Based on CalculatepHfromTCfCO2, version 02.02, 11-12-96, by Ernie Lewis.
    """
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    RR = K0 * fCO2 / TC
    Discr = (K1 * RR) ** 2 + 4 * (1 - RR) * K1 * K2 * RR
    F = (RR >= 1) | (Discr <= 0)
    if np.any(F):
        print("Some input fCO2 values are impossibly high given the input DIC;")
        print("returning np.nan.")
    H = np.where(F, np.nan, 0.5 * (K1 * RR + np.sqrt(Discr)) / (1 - RR))
    pH = -np.log10(H)
    return pH


def TCfrompHfCO2(pH, fCO2, totals, k_constants):
    """Calculate dissolved inorganic carbon from pH and CO2 fugacity.

    Based on CalculateTCfrompHfCO2, version 01.02, 12-13-96, by Ernie Lewis.
    """
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    H = 10.0 ** -pH
    return K0 * fCO2 * (H ** 2 + K1 * H + K1 * K2) / H ** 2


@np.errstate(invalid="ignore")
def pHfromTCCarb(TC, CARB, totals, k_constants):
    """Calculate pH from dissolved inorganic carbon and carbonate ion.

    This calculates pH from Carbonate and TC using K1, and K2 by solving the
    quadratic in H: TC * K1 * K2= Carb * (H * H + K1 * H +  K1 * K2).

    Based on CalculatepHfromTCCarb, version 01.00, 06-12-2019, by Denis Pierrot.
    """
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    RR = 1 - TC / CARB
    Discr = K1 ** 2 - 4 * K1 * K2 * RR
    F = (CARB >= TC) | (Discr <= 0)
    if np.any(F):
        print("Some input CO3 values are impossibly high given the input DIC;")
        print("returning np.nan.")
    H = np.where(F, np.nan, (-K1 + np.sqrt(Discr)) / 2)
    return -np.log10(H)


def fCO2frompHCarb(pH, CARB, totals, k_constants):
    """Calculate CO2 fugacity from pH and carbonate ion.

    Based on CalculatefCO2frompHCarb, version 01.0, 06-12-2019, by Denis Pierrot.
    """
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    H = 10.0 ** -pH
    return CARB * H ** 2 / (K0 * K1 * K2)


def fCO2frompHHCO3(pH, HCO3, totals, k_constants):
    """Calculate CO2 fugacity from pH and bicarbonate ion."""
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    H = 10.0 ** -pH
    return HCO3 * H / (K0 * K1)


def pHfromfCO2Carb(fCO2, CARB, totals, k_constants):
    """Calculate pH from CO2 fugacity and carbonate ion.

    This calculates pH from Carbonate and fCO2 using K0, K1, and K2 by solving
    the equation in H: fCO2 * K0 * K1* K2 = Carb * H * H

    Based on CalculatepHfromfCO2Carb, version 01.00, 06-12-2019, by Denis
    Pierrot.
    """
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    H = np.sqrt(K0 * K1 * K2 * fCO2 / CARB)
    return -np.log10(H)


@np.errstate(invalid="ignore")
def pHfromTCHCO3(TC, HCO3, totals, k_constants):
    """Calculate pH from dissolved inorganic carbon and carbonate ion.

    Follows ZW01 Appendix B (12).
    """
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    a = HCO3 / K1
    b = HCO3 - TC
    c = HCO3 * K2
    bsq_4ac = b ** 2 - 4 * a * c
    F = (HCO3 >= TC) | (bsq_4ac <= 0)
    if np.any(F):
        print("Some input HCO3 values are impossibly high given the input DIC;")
        print("returning np.nan.")
    H = np.where(F, np.nan, (-b - np.sqrt(bsq_4ac)) / (2 * a))
    return -np.log10(H)


def CarbfromfCO2HCO3(fCO2, HCO3, totals, k_constants):
    """Calculate carbonate ion from CO2 fugacity and bicarbonate ion."""
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    return HCO3 ** 2 * K2 / (K0 * fCO2 * K1)


def fCO2fromCarbHCO3(CARB, HCO3, totals, k_constants):
    """Calculate CO2 fugacity from carbonate ion and bicarbonate ion."""
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    K2 = k_constants["K2"]
    return HCO3 ** 2 * K2 / (CARB * K1 * K0)


def fCO2fromTATC(TA, TC, totals, k_constants):
    """Calculate CO2 fugacity from total alkalinity and dissolved inorganic carbon."""
    pH = pHfromTATC(TA, TC, totals, k_constants)
    return fCO2fromTCpH(TC, pH, totals, k_constants)


def fCO2fromTApH(TA, pH, totals, k_constants):
    """Calculate CO2 fugacity from total alkalinity and pH."""
    TC = TCfromTApH(TA, pH, totals, k_constants)
    return fCO2fromTCpH(TC, pH, totals, k_constants)


def CarbfromTATC(TA, TC, totals, k_constants):
    """Calculate carbonate ion from total alkalinity and dissolved inorganic carbon."""
    pH = pHfromTATC(TA, TC, totals, k_constants)
    return CarbfromTCpH(TC, pH, totals, k_constants)


def CarbfromTApH(TA, pH, totals, k_constants):
    """Calculate carbonate ion from total alkalinity and pH."""
    TC = TCfromTApH(TA, pH, totals, k_constants)
    return CarbfromTCpH(TC, pH, totals, k_constants)


def HCO3fromTApH(TA, pH, totals, k_constants):
    """Calculate carbonate ion from total alkalinity and pH."""
    TC = TCfromTApH(TA, pH, totals, k_constants)
    return HCO3fromTCpH(TC, pH, totals, k_constants)


def CarbfrompHfCO2(pH, fCO2, totals, k_constants):
    """Calculate carbonate ion from pH and CO2 fugacity."""
    TC = TCfrompHfCO2(pH, fCO2, totals, k_constants)
    return CarbfromTCpH(TC, pH, totals, k_constants)


def HCO3frompHfCO2(pH, fCO2, totals, k_constants):
    """Calculate bicarbonate ion from pH and CO2 fugacity."""
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    H = 10.0 ** -pH
    return K0 * K1 * fCO2 / H


def HCO3frompHCarb(pH, CARB, totals, k_constants):
    """Calculate bicarbonate ion from pH and carbonate ion."""
    H = 10.0 ** -pH
    return CARB * H / k_constants["K2"]


def CarbfrompHHCO3(pH, HCO3, totals, k_constants):
    """Calculate bicarbonate ion from pH and carbonate ion."""
    H = 10.0 ** -pH
    return k_constants["K2"] * HCO3 / H


def TAfromfCO2Carb(fCO2, CARB, totals, k_constants):
    """Total alkalinity from CO2 fugacity and carbonate ion."""
    pH = pHfromfCO2Carb(fCO2, CARB, totals, k_constants)
    return TAfrompHfCO2(pH, fCO2, totals, k_constants)


def TCfromfCO2Carb(fCO2, CARB, totals, k_constants):
    """Dissolved inorganic carbon from CO2 fugacity and carbonate ion."""
    pH = pHfromfCO2Carb(fCO2, CARB, totals, k_constants)
    return TCfrompHCarb(pH, CARB, totals, k_constants)


def HCO3fromfCO2Carb(fCO2, CARB, totals, k_constants):
    """Bicarbonate ion from CO2 fugacity and carbonate ion."""
    pH = pHfromfCO2Carb(fCO2, CARB, totals, k_constants)
    return HCO3frompHCarb(pH, CARB, totals, k_constants)


def TAfromfCO2HCO3(fCO2, HCO3, totals, k_constants):
    """Total alkalinity from CO2 fugacity and bicarbonate ion."""
    CARB = CarbfromfCO2HCO3(fCO2, HCO3, totals, k_constants)
    return TAfromfCO2Carb(fCO2, CARB, totals, k_constants)


def TCfromfCO2HCO3(fCO2, HCO3, totals, k_constants):
    """Dissolved inorganic carbon from CO2 fugacity and bicarbonate ion."""
    CARB = CarbfromfCO2HCO3(fCO2, HCO3, totals, k_constants)
    return k_constants["K0"] * fCO2 + HCO3 + CARB


def pHfromfCO2HCO3(fCO2, HCO3, totals, k_constants):
    """pH from CO2 fugacity and bicarbonate ion."""
    K0 = k_constants["K0"]
    K1 = k_constants["K1"]
    H = K0 * K1 * fCO2 / HCO3
    return -np.log10(H)


def pHfromCarbHCO3(CARB, HCO3, totals, k_constants):
    """pH from carbonate ion and carbonate ion."""
    H = k_constants["K2"] * HCO3 / CARB
    return -np.log10(H)


def TAfromCarbHCO3(CARB, HCO3, totals, k_constants):
    """Total alkalinity from carbonate ion and carbonate ion."""
    pH = pHfromCarbHCO3(CARB, HCO3, totals, k_constants)
    return TAfrompHCarb(pH, CARB, totals, k_constants)


def TCfromCarbHCO3(CARB, HCO3, totals, k_constants):
    """Dissolved inorganic carbon from carbonate ion and carbonate ion."""
    pH = pHfromCarbHCO3(CARB, HCO3, totals, k_constants)
    return TCfrompHCarb(pH, CARB, totals, k_constants)
