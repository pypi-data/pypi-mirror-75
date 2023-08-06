#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.interpolate import interp1d
from . import utils
from . import preliminary_computations as precomp


def set_filter(info_dict, norm=False, norm_val=0.95):
    """
    Compute the transmittance of the filter with respect to  wavelength

    Parameters
    ----------
    info_dict: dictionary

    wavelength : array
        wavelengths in angstrom

    norm: boolean
        enables to normalise the values to 'norm_val' (default: False)

    norm_val: float
        value used for normalising the data

    Returns
    ---------
    trans :  array
        transmittance of the filter at a given wavelength  (0-1)
    """
    if info_dict["detailed_trans"] == 1:
        filter_path = (
            ("%s/transmissions/filters/" % info_dict["path"])
            + info_dict["filter_folder"]
            + "/"
            + info_dict["filter_band"]
            + ".txt"
        )
    else:
        filter_path = (
            ("%s/transmissions/throughput_curves/" % info_dict["path"])
            + info_dict["filter_folder"]
            + "/"
            + info_dict["filter_band"]
            + ".txt"
        )

    File = open(filter_path, "r")
    lines = File.readlines()

    wvl = []
    trans = []
    for line in lines:
        if line[0] != "#" and len(line) > 3:
            bits = line.split()
            trans.append(float(bits[1]))
            wvl.append(float(bits[0]))
    if info_dict["detailed_trans"] == 1:
        wvl = np.array(wvl) * 10.0  # nm --> angstroms
        trans = np.array(trans, dtype=np.float64) * 1e-2
    else:
        wvl = np.array(wvl)  # should be given in Angstroms
        trans = np.array(trans, dtype=np.float64)  # should be betwwen 0 and 1
    # Normalisation
    if norm:
        trans = trans / max(trans) * norm_val

    # Resample the transmission to the
    trans = utils.resample(wvl, trans, info_dict["wavelength_ang"], 0.0, 1.0)

    return trans


def effectiveWavelength(info_dict):
    """
    Calculates effective wavelength for the passband.
    This is the same as equation (3) of Carter et al. 2009.

    Parameters
    ----------
    info_dict: dictionary

    wavelength: array
        wavelength in nm at which the flux has to be calculated

    Returns:
    ------
    effWavelength: float
        effective wavelength of the passband, in Angstroms

    """
    info_dict = precomp.system_response(info_dict)
    Total_trans = info_dict["system_response"]
    # a=np.trapz(filter_trans*filter_trans, wavelength)
    # b=np.trapz(filter_trans/wavelength, wavelength)
    # effWavelength=np.sqrt(a/b)
    a = np.trapz(info_dict["wavelength_ang"] *
                 Total_trans, info_dict["wavelength_ang"])
    b = np.trapz(Total_trans, info_dict["wavelength_ang"])
    effWavelength = a / b
    info_dict["effWavelength"] = effWavelength
    return info_dict


def effPassband_width(info_dict):
    """ Calculates the wavelength width of the filter passband

    Parameters
    ----------
    info_dict: dictionary

    wavelength: array
        wavelength in nm at which the flux has to be calculated

    Returns:
    ------
    width: float
        wavelength width of the passband, in Angstroms

    """
    Total_trans = info_dict["system_response"]
    width = np.trapz(Total_trans, info_dict["wavelength_ang"])
    info_dict["Passband_width"] = width
    return info_dict


def Passband_cuton(info_dict):
    """
    Calculates the cuton wavelength of the filter passband.
    Defined as an the value where thetransmission reaches
    50% the first time.

    Parameters
    ----------
    info_dict: dictionary

    wavelength: array
        wavelength (angstrom)

    Returns:
    --------
    cuton_wvl: float
        cuton wavelength of the passband, in Angstroms

    """
    Total_trans = info_dict["system_response"]
    limit = 0.5
    # eff_wvl = effectiveWavelength(info_dict)
    w = np.where(info_dict["wavelength_ang"] <
                 info_dict["effWavelength"])
    f = interp1d(info_dict["wavelength_ang"][w], Total_trans[w])
    wvl = np.linspace(
        info_dict["wavelength_ang"][w][0],
        info_dict["wavelength_ang"][w][-1],
        10000
    )
    index = np.argmin((f(wvl) - limit * max(Total_trans)) ** 2.0)
    cuton_wvl = wvl[index]
    info_dict["Passband_cuton"] = cuton_wvl
    return info_dict


def Passband_cutoff(info_dict):
    """
    Calculates the cutoff wavelength of the filter passband.
    Defined as an the value where thetransmission reaches 50%
    for the last time.

    Parameters
    ----------
    info_dict: dictionary

    wavelength: array
        wavelength (angstrom)

    Returns:
    --------
    cutoff_wvl: float
        cutoff wavelength of the passband, in Angstroms

    """
    Total_trans = info_dict["system_response"]
    limit = 0.5
    # eff_wvl = effectiveWavelength(info_dict)
    w = np.where(info_dict["wavelength_ang"] >
                 info_dict["effWavelength"])
    f = interp1d(info_dict["wavelength_ang"][w], Total_trans[w])
    wvl = np.linspace(
        info_dict["wavelength_ang"][w][0],
        info_dict["wavelength_ang"][w][-1],
        10000
    )
    index = np.argmin((f(wvl) - limit * max(Total_trans)) ** 2.0)
    cutoff_wvl = wvl[index]
    info_dict["Passband_cutoff"] = cutoff_wvl
    return info_dict


def sed_vega(info_dict):
    """This function stores the SED of Vega, used for calculation
    of magnitudes on the Vega system. The Vega SED used is taken
    from Bohlin 2007 (http://adsabs.harvard.edu/abs/2007ASPC..364..315B),
    and is available from the STScI CALSPEC library
    (http://www.stsci.edu/hst/observatory/cdbs/calspec.html).

    Parameters
    ----------
    wvl: array
        wavelength in nm at which the flux has to be computed

    Returns
    -------
    wavelength: array
        wavelength in Angstrom

    Flux: array
        Flux of Vega in erg/cm2/s/A

    """
    VEGA_PATH = "%s/data/bohlin2006_Vega.dat" % info_dict["path"]

    inFile = open(VEGA_PATH, "r")
    lines = inFile.readlines()

    wavelength = []
    flux = []
    for line in lines:
        if line[0] != "#" and len(line) > 3:
            bits = line.split()
            flux.append(float(bits[1]))
            wavelength.append(float(bits[0]))

    wavelength = np.array(wavelength)
    flux = np.array(flux, dtype=np.float64)

    return [wavelength, flux]


def zeromag_to_flux(info_dict, unit="Flam", phot_sys="dummy"):
    """
    This function return the zero magnitude in either the AB system,
    ie 3631 Jy for all wavelengths, or the Vega one.

    Parameters
    ----------
    info_dict: dictionary

    wavelength: array
        wavelength in nm at which the flux has to be calculated

    unit: string
        'Jy': return the flux in Jansky / 'Fv': return the flux in erg/s/cm2/Hz
        'Flam': return the flux in erg/s/cm2/A (default) / 'ph': ph/s/cm2/A

    Returns
    ---------
    zero_flux: array
        Flux corresponding to a zero magnitude in either AB or
        Vega system in units of Jansky, erg/s/cm2/Hz or erg/s/cm2/A
    """
    if phot_sys != "dummy":
        photometry_system = phot_sys
    else:
        photometry_system = info_dict["photometry_system"]

    if photometry_system == "AB":
        """
        if unit == 'Jy':
             zero_flux = 3631.*np.ones(len(info_dict['wavelength_ang']))
        elif unit == 'Fv':
             zero_flux = utils.fJy_to_fnu(3631.*
                            np.ones(len(info_dict['wavelength_ang'])))
        elif unit == 'Flam':
             zero_flux = utils.fJy_to_flambda(wvl,3631.*
                            np.ones(len(info_dict['wavelength_ang'])))
        elif unit == 'ph':
             zero_flux_flambda = utils.fJy_to_flambda(wavelength,3631.*
                            np.ones(len(info_dict['wavelength_ang'])))
             zero_flux = utils.flambda_to_fph(info_dict['wavelength_ang'],
                                              zero_flux_flambda)
        """
        # Calculate the Flux in Jy corresponding to m=0
        Flux_zero_Jy = 3631

    elif photometry_system.lower() == "vega":
        # in (A, erg/s/cm2/A)
        wavelength_vega, flux_vega = sed_vega(info_dict)
        f = interp1d(wavelength_vega, flux_vega, kind="linear")
        flux_resampled = f(info_dict["wavelength_ang"])
        """
         if unit =='Jy':
              zero_flux = utils.flambda_to_fJy(info_dict['wavelength_ang'],
                                               flux_resampled)
         elif unit =='Fv':
              zero_flux = utils.flambda_to_fnu(info_dict['wavelength_ang'],
                                               flux_resampled)
         elif unit == 'Flam':
              zero_flux = flux_resampled
         elif unit =='ph':
              zero_flux = utils.flambda_to_fph(info_dict['wavelength_ang'],
                                               flux_resampled)
         """
        # Calculate the Flux in Jy corresponding to m=0
        # Here we consider a constant Flux (in Jy) through the passband
        # Flux_zero_Jy=np.trapz(utils.flambda_to_fJy(
        #     info_dict['wavelength_ang'],flux_resampled)
        #     * precomp.system_response(info_dict,wavelength)
        #     / wavelength,wavelength)
        #     / np.trapz(precomp.system_response(info_dict,wavelength)
        #             / wavelength,wavelength)

        Flux_zero_Jy = np.trapz(
            utils.flambda_to_fJy(info_dict["wavelength_ang"], flux_resampled)
            * info_dict["system_response"]
            / info_dict["wavelength_ang"],
            info_dict["wavelength_ang"],
        ) / np.trapz(
            info_dict["system_response"] / info_dict["wavelength_ang"],
            info_dict["wavelength_ang"],
        )

    info_dict["Flux_zero_Jy"] = Flux_zero_Jy
    return info_dict


def zeropoint(info_dict):
    """
    Computes the zero point of a particular system configuration
    (filter, atmospheric conditions,optics,camera).
    The zeropoint is the magnitude which will lead to one count per second.
    By definition ZP = -2.5*log10( Flux_1e-_per_s / Flux_zeromag ),
    where Flux_1e-_per_s = 1 e-/s and Flux_zeromag =
    sum_over_passband ( zero_flux * system_response * A_tel ) in e-/s
    Hence:
    ZP = 2.5*log10( sum_over_passband ( zero_flux * system_response * A_tel ))

    Parameters
    ----------
    info_dict: dictionary

    wavelength: array
        wavelength in angstrom

    Returns
    ------_
    zeropoint: float
        zeropoint in magnitude
    """
    # Integrate over the wavelengths
    # Flux_zero = np.trapz(zeromag_to_flux(info_dict,wavelength,unit='ph')
    #                   * precomp.system_response(info_dict,wavelength),
    #                   wavelength)*precomp.A_tel(info_dict)
    # Flux_zero = np.trapz(zeromag_to_flux(info_dict,unit='ph')
    #                   * info_dict['system_response'],
    #                    info_dict['wavelength_ang'])
    #                   * info_dict['A_tel']
    Flux_zero = (
        np.trapz(
            utils.flambda_to_fph(
                info_dict["wavelength_ang"],
                utils.fJy_to_flambda(
                    info_dict["wavelength_ang"], info_dict["Flux_zero_Jy"]
                ),
            )
            * info_dict["system_response"]
            * info_dict["Trans_atmosphere"],
            info_dict["wavelength_ang"],
        )
        * info_dict["A_tel"]
    )
    ZP = 2.5 * np.log10(Flux_zero)
    info_dict["zeropoint"] = ZP
    return info_dict


def mag2Jy(info_dict, Mag):
    """Converts a magnitude into flux density in Jy

    Parameters
    -----------
    info_dict: dictionary

    Mag: array or float
        AB or vega magnitude

    Returns
    -------
    fluxJy: array or float
        flux density in Jy

    """

    fluxJy = info_dict["Flux_zero_Jy"] * 10 ** (-0.4 * Mag)

    return fluxJy


def Jy2Mag(info_dict, fluxJy):
    """Converts flux density in Jy into magnitude

    Parameters
    ----------
    info_dict: dictionary

    fluxJy: array or float
        flux density in Jy

    Returns
    -------
    mag : array or float
        magnitude
    """
    # print (fluxJy,info_dict['Flux_zero_Jy'])
    Mag = -2.5 * np.log10(fluxJy / info_dict["Flux_zero_Jy"])

    return Mag


def set_photometry(info_dict):

    info_dict = effectiveWavelength(info_dict)
    info_dict = effPassband_width(info_dict)
    info_dict = Passband_cuton(info_dict)
    info_dict = Passband_cutoff(info_dict)
    info_dict = zeromag_to_flux(info_dict)
    info_dict = zeropoint(info_dict)

    return info_dict
