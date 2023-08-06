#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from . import preliminary_computations as precomp
from .local_conditions import sky_countrate
from . import optics as opt
from . import photometry as phot
from . import utils


def etc_computation(info_dict):
    """
    Compute either the SNR, the total exposure time or
    the magnitude in function of the 2 others

    Parameters
    ----------
    info_dict: dictionary
        contains all relevant information

    wavelength : array
        wavelengths in angstrom

    Returns
    ---------
    SNR: float
        Signal to noise ratio

    mag: float
        magnitude reached

    tot_exp_time: float
        total exposure time in seconds

    """
    # display result
    verbose = info_dict["verbose"]

    etc_type = info_dict["etc_type"]
    SNR = info_dict["SNR"]
    tot_exp_time = info_dict["Nexp"] * info_dict["exptime"]
    info_dict["total_exposure_time"] = tot_exp_time
    Nexp = info_dict["Nexp"]
    # Detector Integration Time in seconds
    if etc_type == "snr" or etc_type == "mag":
        DIT = info_dict["exptime"] - info_dict["T_dithering"]

    # Display
    if verbose:
        print("\nInformation about Passband:")
        print("----------------------------")
        print("Cut_on: %.f angstroms" % info_dict["Passband_cuton"])
        print("Effective wavelength: %.f angstroms" %
              info_dict["effWavelength"])
        print("Cut_off: %.f angstroms" % info_dict["Passband_cutoff"])

        print("\nAirmass: %.2f" % info_dict["airmass"])
        print("\nSeeing: %.2f" % info_dict["seeing_los_arcsec"])

    if info_dict["detailed_trans"] == 1:
        # Computes mean transmission of each components for the given passband
        mean_trans_tel = utils.mean_efficiency_passband(
            info_dict, opt.telescope_efficiency(info_dict)
        )
        mean_trans_inst = utils.mean_efficiency_passband(
            info_dict,
            opt.instrument_channel_efficiency(info_dict)
            * info_dict["Trans_filter"]
            * info_dict["camera_efficiency"],
        )
        mean_trans_filter = utils.mean_efficiency_passband(
            info_dict, info_dict["Trans_filter"]
        )
        mean_eta_cam = utils.mean_efficiency_passband(
            info_dict, info_dict["camera_efficiency"]
        )
        mean_trans_optics = mean_trans_tel * mean_trans_inst
        mean_trans_atm = utils.mean_efficiency_passband(
            info_dict, info_dict["Trans_atmosphere"]
        )
        mean_trans_system = mean_trans_optics
        info_dict["trans_mean_tel"] = mean_trans_tel
        info_dict["trans_mean_inst"] = mean_trans_inst
        info_dict["trans_mean_optics"] = mean_trans_optics
        info_dict["trans_mean_filter"] = mean_trans_filter
        info_dict["trans_mean_atm"] = mean_trans_atm
        info_dict["trans_mean_cam"] = mean_eta_cam
        info_dict["trans_mean_system"] = mean_trans_system

        if verbose:
            print("\nMEAN EFFICENCIES:")
            print("------------------")
            print("Obscuration: %.3f" % (1.0 - info_dict["obstruction"]))
            print(
                "Telescope: %.3f (+obs: %.3f)"
                % (mean_trans_tel,
                   mean_trans_tel * (1.0 - info_dict["obstruction"]))
            )
            print("Instrument: %.3f" % mean_trans_inst)
            print(
                "Optics (tel+inst): %.3f  (+obs: %.3f)"
                % (
                    mean_trans_optics,
                    mean_trans_optics * (1.0 - info_dict["obstruction"]),
                )
            )
            print("Filter: %.3f" % mean_trans_filter)
            print("Atmosphere: %.3f" % mean_trans_atm)
            print("Camera: %.3f" % mean_eta_cam)
            print(
                "System: %.3f (+obs: %.3f)\n"
                % (
                    mean_trans_system,
                    mean_trans_system * (1 - info_dict["obstruction"]),
                )
            )

    elif info_dict["detailed_trans"] == 0:
        mean_eta_cam = utils.mean_efficiency_passband(
            info_dict, info_dict["camera_efficiency"]
        )
        mean_eta_optics = utils.mean_efficiency_passband(
            info_dict, phot.set_filter(info_dict)
        )
        mean_trans_system = mean_eta_cam * mean_eta_optics
        info_dict["trans_mean_system"] = mean_trans_system
        if verbose:
            print("\nMEAN EFFICENCIES:")
            print("------------------")
            print("Obscuration: %.3f" % (1.0 - info_dict["obstruction"]))
            print(
                "System: %.2f (+obs: %.3f)\n"
                % (
                    mean_trans_system,
                    mean_trans_system * (1 - info_dict["obstruction"]),
                )
            )

    # Number of pixels covering 1.35*FWHM of the PSF
    npix = info_dict["npix"]
    # Factor when estimating the Noise from other images
    factor_ima = precomp.factor_images_averaged(info_dict)
    # Fraction of light in the brightest pixel
    f_pix = precomp.Normalisation_factor(info_dict, True)
    # Fraction of light in the PSF
    f_PSF = precomp.Normalisation_factor(info_dict, False)

    info_dict["factor_ima"] = factor_ima
    info_dict["f_pix"] = f_pix
    info_dict["f_PSF"] = f_PSF

    # Background Noise countrate in e-/s/px
    # ---------------------------------------
    info_dict = sky_countrate(info_dict)  # e-/s/px
    BN = info_dict["Sky_CountRate"]
    # print ('Sky countrate: %.2f (e-/px/s)' % BN)
    # Thermic signal (electrons/s/pixel)  <--> Dark current
    # ------------------------------------------------------
    DC = info_dict["cameras"][info_dict["channel"]]["DC"]
    # Digitization noise   (e-/pixel)
    # ----------------------------------
    # Converter analog to digital noise of 1/2 ADU (electrons/pixel)
    DigN = info_dict["dig_noise"]

    # Readout noise (e-/pixel)
    # --------------------------
    RN = info_dict["cameras"][info_dict["channel"]]["RN"]

    # Instrument background (e-/s/pix)
    inst_bg = info_dict["Instrument_bg"]

    # Object
    # ---------
    # Count rate of the object in e-/s
    if etc_type == "snr" or etc_type == "time":
        CR, fph = info_dict["Object_fes"], info_dict["Object_fph"]  # e-/s

    # Zeropoint
    # -----------
    ZP = info_dict["zeropoint"]

    # Add some info in info_cit
    if verbose:
        print("Zeropoint: %.2f (%s mag)" % (ZP,
                                            info_dict["photometry_system"]))

    # Compute the SNR
    # ------------------
    if etc_type == "snr":
        # In the case of a given magnitude to reach, the fraction of flux
        # we kept should be included so that the given mag corresponds to the
        # measured count rate.
        if info_dict["object_type"] == "magnitude":
            CR = CR  # / f_PSF
            CR_pix = CR  # / f_pix
        else:
            CR_pix = CR

        # Peak SNR (Object signal/noise at the brightest pixel)
        SNR_pix = (
            np.sqrt(Nexp)
            * CR_pix
            * f_pix
            * DIT
            / np.sqrt(
                CR_pix * f_pix * DIT
                + factor_ima * ((RN ** 2.0 + DigN ** 2.0)
                                + DIT * (DC + BN + inst_bg))
            )
        )

        # Total integrated noise over npix (electrons/area)
        SNR = (
            np.sqrt(Nexp)
            * CR
            * f_PSF
            * DIT
            / np.sqrt(
                CR * f_PSF * DIT
                + factor_ima
                * npix
                * ((RN ** 2.0 + DigN ** 2.0) + DIT * (DC + BN + inst_bg))
            )
        )

        if info_dict["object_type"] == "magnitude":
            # mag = ZP - 2.5*np.log10(CR*f_PSF)
            mag = info_dict["object_magnitude"]
            mag_pix = ZP - 2.5 * np.log10(CR_pix * f_pix)
            mag_pix = info_dict["object_magnitude"]
        else:
            mag = ZP - 2.5 * np.log10(CR)
            mag_pix = ZP - 2.5 * np.log10(CR_pix)

        Ftot_el = CR * f_PSF * DIT  # *np.sqrt(Nexp)
        Ftot_el_pix = CR_pix * f_pix * DIT  # *np.sqrt(Nexp)
        DIT_pix = DIT

        info_dict["SNR"] = SNR
        info_dict["SNR_pix"] = SNR_pix
        info_dict["mag_pix"] = mag_pix
        info_dict["Ftot_el_pix"] = Ftot_el_pix
        info_dict["Ftot_el"] = Ftot_el
        info_dict["DIT_pix"] = DIT_pix

        if verbose:
            print(
                "\n\nA magnitude (%s system) of %.2f in %s band within a total exposure time of %.2f seconds splited in %d exposure(s), implies a total SNR of :\n"
                % (
                    info_dict["photometry_system"],
                    mag,
                    info_dict["filter_band"],
                    DIT * Nexp,
                    Nexp,
                )
            )
            # print ('\t - Peak SNR at the brightest pixel: %.2f \n' % SNR_pix)
            print("\t - Integrated SNR over %d pixels: %.2f" % (npix, SNR))
            print(
                "\n\nA magnitude (%s system) of %.2f in %s band within a total exposure time of %.2f seconds splited in %d exposure(s), implies a SNR for the central pixel of of :\n\n"
                % (
                    info_dict["photometry_system"],
                    mag_pix,
                    info_dict["filter_band"],
                    DIT_pix * Nexp,
                    Nexp,
                )
            )
            print("\t - SNR of the central pixel: %.2f \n\n" % SNR_pix)

    # Compute the total exposure time
    # --------------------------------
    elif etc_type == "time":

        # In the case of a given magnitude to reach, the fraction of flux
        # we kept should be included so that the given mag corresponds to the
        # measured count rate.
        if info_dict["object_type"] == "magnitude":
            CR = CR  # / f_PSF

        # Integrated over Npixels     (solve 2nd degree equation)
        if Nexp > 1:
            SNR_1 = SNR / np.sqrt(Nexp)
        else:
            SNR_1 = SNR
        A_sys = -((CR * f_PSF) ** 2.0)
        B_sys = SNR_1 ** 2.0 * (CR * f_PSF + factor_ima * npix
                                * (DC + BN + inst_bg))
        C_sys = SNR_1 ** 2.0 * factor_ima * npix * (RN ** 2.0 + DigN ** 2.0)

        delta = B_sys * B_sys - 4.0 * A_sys * C_sys

        DIT = (-B_sys - np.sqrt(delta)) / (2.0 * A_sys)
        # mag = -2.5*np.log10(obj_janskys/3631)

        if info_dict["object_type"] == "magnitude":
            mag = ZP - 2.5 * np.log10(CR)  # *f_PSF)
        else:
            mag = ZP - 2.5 * np.log10(CR)

        Ftot_el = CR * f_PSF * DIT  # *np.sqrt(Nexp)

        # Brightest pixel
        if info_dict["object_type"] == "magnitude":
            CR_pix = CR  # / f_pix
        else:
            CR_pix = CR

        A_sys = -((CR_pix * f_pix) ** 2.0)
        B_sys = SNR_1 ** 2.0 * (CR_pix * f_pix + factor_ima
                                * (DC + BN + inst_bg))
        C_sys = SNR_1 ** 2.0 * factor_ima * (RN ** 2.0 + DigN ** 2.0)

        delta = B_sys * B_sys - 4.0 * A_sys * C_sys

        DIT_pix = (-B_sys - np.sqrt(delta)) / (2.0 * A_sys)

        if info_dict["object_type"] == "magnitude":
            mag_pix = ZP - 2.5 * np.log10(CR_pix)  # *f_pix)
        else:
            mag_pix = ZP - 2.5 * np.log10(CR)

        Ftot_el_pix = CR_pix * f_pix * DIT_pix  # *np.sqrt(Nexp)

        info_dict["DIT"] = DIT
        info_dict["DIT_pix"] = DIT_pix
        info_dict["Ftot_el_pix"] = Ftot_el_pix
        info_dict["Ftot_el"] = Ftot_el
        info_dict["mag_pix"] = mag_pix

        if verbose:
            print(
                "\n\nReaching a magnitude (%s system) of %.2f in %s band with a SNR of %.2f requires:\n"
                % (info_dict["photometry_system"], mag, info_dict["filter_band"], SNR)
            )
            print("\t - a Total exposure time of: %.2f s\n" % (DIT * Nexp))
            print(
                "\n\nReaching a magnitude (%s system) of %.2f in %s band with a SNR of %.2f for the central pixel requires:\n\n"
                % (
                    info_dict["photometry_system"],
                    mag_pix,
                    info_dict["filter_band"],
                    SNR,
                )
            )
            print("\t - a Total exposure time of: %.2f s\n\n" % (DIT_pix * Nexp))

    # Compute the magnitude
    # ------------------------
    elif etc_type == "mag":
        # f_PSF=1
        # f_pix=1
        # Integrated over Npixels    (solve 2nd degree equation)
        A_sys = -((f_PSF * DIT * np.sqrt(Nexp)) ** 2.0)
        B_sys = SNR ** 2.0 * f_PSF * DIT
        C_sys = SNR ** 2.0 * (
            factor_ima * npix * (RN ** 2.0 + DigN ** 2.0 + DIT
                                 * (DC + BN + inst_bg))
        )

        delta = B_sys * B_sys - 4.0 * A_sys * C_sys

        CR = (-B_sys - np.sqrt(delta)) / (2.0 * A_sys)
        Ftot_el = CR * f_PSF * DIT  # *np.sqrt(Nexp)

        mag = ZP - 2.5 * np.log10(CR)

        # Central pixel
        A_sys = -((f_pix * DIT * np.sqrt(Nexp)) ** 2.0)
        B_sys = SNR ** 2.0 * f_pix * DIT
        C_sys = SNR ** 2.0 * (
            factor_ima * (RN ** 2.0 + DigN ** 2.0 + DIT * (DC + BN + inst_bg))
        )

        delta = B_sys * B_sys - 4.0 * A_sys * C_sys

        CR_pix = (-B_sys - np.sqrt(delta)) / (2.0 * A_sys)
        Ftot_el_pix = CR_pix * f_pix * DIT  # *np.sqrt(Nexp)
        mag_pix = ZP - 2.5 * np.log10(CR_pix)
        DIT_pix = DIT

        object_mag = mag * np.ones(len(info_dict["wavelength_ang"]))
        fJy = phot.mag2Jy(info_dict, object_mag)  # Jy
        # erg/s/cm2/A
        flam = utils.fJy_to_flambda(info_dict["wavelength_ang"], fJy)
        # ph/s/cm2/A
        fph = utils.flambda_to_fph(info_dict["wavelength_ang"], flam)

        info_dict["Object_mag"] = object_mag
        info_dict["object_magnitude"] = mag
        info_dict["mag_pix"] = mag_pix
        info_dict["DIT_pix"] = DIT
        info_dict["Ftot_el_pix"] = Ftot_el_pix
        info_dict["Ftot_el"] = Ftot_el

        if verbose:
            print(
                "\n\nFor a total SNR=%.2f in a total exposure time of %.2f (sec) in %d exposure(s) we reach:\n"
                % (SNR, DIT * Nexp, Nexp)
            )
            print(
                "\t - a magnitude (%s system) of: %.2f in %s band\n"
                % (info_dict["photometry_system"],
                   mag,
                   info_dict["filter_band"])
            )
            print(
                "\n\nFor the central pixel a SNR=%.2f in a total exposure time of %.2f (sec) in %d exposure(s) we reach:\n\n"
                % (SNR, DIT_pix * Nexp, Nexp)
            )
            print(
                "\t - a magnitude (%s system) of: %.2f in %s band\n\n"
                % (info_dict["photometry_system"], mag_pix, info_dict["filter_band"])
            )

    info_dict["DIT"] = DIT

    # sigma_shot_noise = np.sqrt(Ftot_el * DIT)
    # sigma_dark_current = np.sqrt(DC * npix * DIT)
    # sigma_sky = np.sqrt(BN * npix * DIT)
    # sigma_digitization = np.sqrt(npix * DigN ** 2.0)
    # sigma_readout_noise = np.sqrt(npix * RN ** 2.0)

    # Total number of electrons in the brightest pixel for 1 exposure
    N_el_tot_pix1 = Ftot_el_pix + (BN + DC + inst_bg) * DIT_pix + RN + DigN
    N_el_tot_pix2 = (Ftot_el * f_pix / f_PSF
                     + (BN + DC + inst_bg) * DIT + RN + DigN)

    info_dict["N_el_tot_pix1"] = N_el_tot_pix1
    info_dict["N_el_tot_pix2"] = N_el_tot_pix2

    if N_el_tot_pix1 > info_dict["cameras"][info_dict["channel"]]["FWC"]:
        info_dict["saturation"] = "Yes"
    else:
        info_dict["saturation"] = "No"

    if verbose:

        print(
            "\nFull well capacity of 1 pixel: %.2f (electrons)"
            % (info_dict["cameras"][info_dict["channel"]]["FWC"])
        )
        print("\n\n--------- One pixel only------------------")
        print(
            "\nPhoto-electrons created: central pix for %d exposure(s) of %.2f sec "
            % (Nexp, DIT_pix)
        )
        print("\tby:")
        print("\t- Object:         %10.2f   (electrons)" % Ftot_el_pix)
        print("\t- Sky:            %10.2f   (electrons)" % (BN * DIT_pix))
        print("\t- Readout:        %10.2f   (electrons)" % RN)
        print("\t- Dark current:   %10.2f   (electrons)" % (DC * DIT_pix))
        print("\t- Digitization:   %10.2f   (electrons)" % DigN)
        print("\t- Instrument bg:  %10.2f   (electrons)" % (inst_bg * DIT_pix))

        print(
            "\nSNR: -central pixel: %.2f"
            % (
                np.sqrt(Nexp)
                * Ftot_el_pix
                / np.sqrt(
                    Ftot_el_pix
                    + factor_ima
                    * ((RN ** 2.0 + DigN ** 2.0) + DIT_pix
                       * (DC + BN + inst_bg))
                )
            )
        )

        print(
            "\nTotal of electrons collected in the central pixel during an exposure time of %d seconds: %.2f "
            % (DIT_pix, N_el_tot_pix1)
        )
        if N_el_tot_pix1 > info_dict["cameras"][info_dict["channel"]]["FWC"]:
            print(
                "--> Central pixel saturated: number of electrons > Full well Capacity"
            )
        elif N_el_tot_pix1 > info_dict["cameras"][info_dict["channel"]]["gain"] * (
            2.0 ** (info_dict["cameras"][info_dict["channel"]]["bits"]) - 1
        ):
            print(
                "--> Central pixel saturated: number of electrons > number of digitizations"
            )
        elif (
            N_el_tot_pix1 > 1.0 / 2 * info_dict["cameras"][info_dict["channel"]]["FWC"]
        ):
            print(
                "--> Number of electrons in central pixel > 1/2 of Full well Capacity. Risk of non-linear response."
            )

        else:
            print("--> No saturation")

        print("\n\n\n--------- Integrated over %d pixels------------------" % npix)
        print(
            "\nPhoto-electrons created: brightest pix |  total of %d pixels, %d exposure(s) of %.2f sec "
            % (npix, Nexp, DIT)
        )
        print("\tby:")
        print(
            "\t- Object:         %10.2f   |   %10.2f   (electrons)"
            % (Ftot_el * f_pix / f_PSF, Ftot_el)
        )
        print(
            "\t- Sky:            %10.2f   |   %10.2f   (electrons)"
            % (BN * DIT, (BN * npix * DIT * Nexp))
        )
        print(
            "\t- Readout:        %10.2f   |   %10.2f   (electrons)"
            % (RN, (RN * npix * Nexp))
        )
        print(
            "\t- Dark current:   %10.2f   |   %10.2f   (electrons)"
            % (DC * DIT, (DC * DIT * npix * Nexp))
        )
        print(
            "\t- Digitization:   %10.2f   |   %10.2f   (electrons)"
            % (DigN, (DigN * npix * Nexp))
        )
        print(
            "\t- Instrument bg:  %10.2f   |   %10.2f   (electrons)"
            % (inst_bg * DIT, (inst_bg * DIT * npix * Nexp))
        )

        print(
            "\nSNR: -Brightest pixel: %.2f"
            % (
                np.sqrt(Nexp)
                * Ftot_el
                * f_pix
                / f_PSF
                / np.sqrt(
                    Ftot_el * f_pix / f_PSF
                    + factor_ima
                    * ((RN ** 2.0 + DigN ** 2.0) + DIT * (DC + BN + inst_bg))
                )
            )
        )
        print(
            "     -integrated over %d pixels: %.2f"
            % (
                npix,
                np.sqrt(Nexp)
                * Ftot_el
                / np.sqrt(
                    Ftot_el
                    + factor_ima
                    * npix
                    * ((RN ** 2.0 + DigN ** 2.0) + DIT * (DC + BN + inst_bg))
                ),
            )
        )
        print(
            "\nTotal of electrons collected in the brightest pixel during an exposure time of %d seconds: %.2f "
            % (DIT_pix, N_el_tot_pix2)
        )
        if N_el_tot_pix2 > info_dict["cameras"][info_dict["channel"]]["FWC"]:
            print(
                "--> Brightest pixel saturated: number of electrons > Full well Capacity"
            )
        elif N_el_tot_pix2 > info_dict["cameras"][info_dict["channel"]]["gain"] * (
            2.0 ** (info_dict["cameras"][info_dict["channel"]]["bits"]) - 1
        ):
            print(
                "--> Brightest pixel saturated: number of electrons > number of digitizations"
            )
        elif (
            N_el_tot_pix2 > 1.0 / 2 * info_dict["cameras"][info_dict["channel"]]["FWC"]
        ):
            print(
                "--> Number of electrons in brightest pixel > 1/2 of Full well Capacity. Risk of non-linear response."
            )

        else:
            print("--> No saturation")

        print(
            "\nDead time: %.2f sec \n(%.2f sec for dithering, the %.2f sec for the readout are not taken into account)"
            % (
                info_dict["deadtime_tot"],
                info_dict["T_dithering"],
                info_dict["cameras"][info_dict["channel"]]["ReadoutTime"],
            )
        )
    info_dict["SNR"] = SNR
    info_dict["mag"] = mag
    info_dict["total_exposure_time"] = DIT * Nexp
    info_dict["fph"] = fph

    return info_dict
