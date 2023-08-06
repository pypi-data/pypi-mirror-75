#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import errno


def write_results(info_dict):
    """ Write the results in a file """

    #  create folder results if not existing
    directory = "%s/results/" % info_dict["path"]
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f = open("%s/results/results_summary.txt" % info_dict["path"], "w")
    f.write("Information about the simulation:\n")
    f.write("---------------------------------\n")
    if info_dict["etc_type"] == "time":
        f.write(
            "Compute the time required to observe the object with a SNR=%.2f \n"
            % info_dict["SNR"]
        )
        if info_dict["object_type"] == "magnitude":
            f.write("Object: magnitude of %.2f\n" % info_dict["object_magnitude"])
        else:
            f.write(
                "Object: %s/%s\n"
                % (info_dict["object_folder"], info_dict["object_file"])
            )
    elif info_dict["etc_type"] == "snr":
        f.write(
            "Compute the SNR reached when observing the object during %d exposure(s) of %.2f seconds\n"
            % (info_dict["Nexp"], info_dict["total_exposure_time"] / info_dict["Nexp"])
        )
        if info_dict["object_type"] == "magnitude":
            f.write("Object: magnitude of %.2f\n" % info_dict["object_magnitude"])
        else:
            f.write(
                "Object: %s/%s\n"
                % (info_dict["object_folder"], info_dict["object_file"])
            )
    elif info_dict["etc_type"] == "mag":
        f.write(
            "Compute the magnitude reached when observing during %d exposure(s) of %.2f seconds with a SNR=%.2f\n"
            % (
                info_dict["Nexp"],
                info_dict["total_exposure_time"] / info_dict["Nexp"],
                info_dict["SNR"],
            )
        )

    f.write("\nInformation about Passband:\n")
    f.write("----------------------------\n")
    f.write("Filter: %s %s\n" % (info_dict["filter_folder"], info_dict["filter_band"]))
    f.write("Cut_on: %.f angstroms\n" % info_dict["Passband_cuton"])
    f.write("Effective wavelength: %.f angstroms\n" % info_dict["effWavelength"])
    f.write("Cut_off: %.f angstroms\n" % info_dict["Passband_cutoff"])

    f.write("\nInformation about Local conditions:\n")
    f.write("----------------------------\n")
    f.write("Site: %s\n" % info_dict["sky_site"])
    f.write("Seeing at zenith: %.2f\n" % info_dict["seeing_zenith"])
    f.write("Elevation: %.2f degrees\n" % info_dict["elevation"])
    f.write("Airmass: %.2f\n" % info_dict["airmass"])
    f.write("Moon age: %.2f\n" % info_dict["moon_age"])

    if info_dict["detailed_trans"] == 1:

        f.write("\nMEAN EFFICENCIES:\n")
        f.write("------------------\n")
        f.write("Obscuration: %.2f \n" % (1.0 - info_dict["obstruction"]))
        f.write(
            "Telescope: %.2f (+obs: %.2f) \n"
            % (
                info_dict["trans_mean_tel"],
                info_dict["trans_mean_tel"] * (1.0 - info_dict["obstruction"]),
            )
        )
        f.write("Instrument: %.2f \n" % info_dict["trans_mean_inst"])
        f.write(
            "Optics (tel+inst): %.2f  (+obs: %.2f) \n"
            % (
                info_dict["trans_mean_optics"],
                info_dict["trans_mean_optics"] * (1.0 - info_dict["obstruction"]),
            )
        )
        f.write("Filter: %.2f \n" % info_dict["trans_mean_filter"])
        f.write("Atmosphere: %.2f \n" % info_dict["trans_mean_atm"])
        f.write("Camera: %.2f \n" % info_dict["trans_mean_cam"])
        f.write(
            "System: %.2f (+obs: %.2f)\n"
            % (
                info_dict["trans_mean_system"],
                info_dict["trans_mean_system"] * (1 - info_dict["obstruction"]),
            )
        )

    elif info_dict["detailed_trans"] == 0:

        f.write("\nMEAN EFFICENCIES:\n")
        f.write("------------------\n")
        f.write("Obscuration: %.2f \n" % (1.0 - info_dict["obstruction"]))
        f.write(
            "System: %.2f (+obs: %.2f)\n"
            % (
                info_dict["trans_mean_system"],
                info_dict["trans_mean_system"] * (1 - info_dict["obstruction"]),
            )
        )

    f.write(
        "\nZeropoint: %.2f (%s mag) \n"
        % (info_dict["zeropoint"], info_dict["photometry_system"])
    )

    if info_dict["etc_type"] == "snr":

        f.write(
            "\n\nA magnitude (%s system) of %.2f in %s band within a total exposure time of %.2f seconds splited in %d exposure(s), implies a total SNR of :\n\n"
            % (
                info_dict["photometry_system"],
                info_dict["mag"],
                info_dict["filter_band"],
                info_dict["exptime"],
                info_dict["Nexp"],
            )
        )
        f.write(
            "\t - Integrated SNR over %d pixels: %.2f \n\n"
            % (info_dict["npix"], info_dict["SNR"])
        )
        f.write(
            "\nA magnitude (%s system) of %.2f in %s band within a total exposure time of %.2f seconds splited in %d exposure(s), implies a SNR for the central pixel of of :\n\n"
            % (
                info_dict["photometry_system"],
                info_dict["mag_pix"],
                info_dict["filter_band"],
                info_dict["DIT_pix"] * info_dict["Nexp"],
                info_dict["Nexp"],
            )
        )
        f.write("\t - SNR of the central pixel: %.2f \n\n" % info_dict["SNR_pix"])

    elif info_dict["etc_type"] == "time":
        f.write(
            "\n\nA magnitude (%s system) of %.2f in %s band with a total SNR of %.2f requires:\n\n"
            % (
                info_dict["photometry_system"],
                info_dict["mag"],
                info_dict["filter_band"],
                info_dict["SNR"],
            )
        )
        f.write(
            "\t - a Total exposure time of : %.2f \n\n"
            % (info_dict["DIT"] * info_dict["Nexp"])
        )
        f.write(
            "\n\nA magnitude (%s system) of %.2f in %s band with a SNR of %.2f for the central pixel requires:\n\n"
            % (
                info_dict["photometry_system"],
                info_dict["mag_pix"],
                info_dict["filter_band"],
                info_dict["SNR"],
            )
        )
        f.write(
            "\t - a Total exposure time of : %.2f \n\n"
            % (info_dict["DIT_pix"] * info_dict["Nexp"])
        )

    elif info_dict["etc_type"] == "mag":

        f.write(
            "\n\nFor a total SNR=%.2f in a total exposure time of %.2f (sec) in %d exposure(s) we reach:\n\n"
            % (info_dict["SNR"], info_dict["exptime"], info_dict["Nexp"])
        )
        f.write(
            "\t - a magnitude (%s system) of: %.2f in %s band\n\n"
            % (
                info_dict["photometry_system"],
                info_dict["mag"],
                info_dict["filter_band"],
            )
        )
        f.write(
            "\n\nFor the central pixel a SNR=%.2f in a total exposure time of %.2f (sec) in %d exposure(s) we reach:\n\n"
            % (
                info_dict["SNR"],
                info_dict["DIT_pix"] * info_dict["Nexp"],
                info_dict["Nexp"],
            )
        )
        f.write(
            "\t - a magnitude (%s system) of: %.2f in %s band\n\n"
            % (
                info_dict["photometry_system"],
                info_dict["mag_pix"],
                info_dict["filter_band"],
            )
        )

    # f.write ('\nFull well capacity of 1 pixel: %.2f (electrons)\nInverse gain of %.2f e/ADU and %d bits implies a maximum number of electrons to be digitized of  %.2f (electrons) \n' % (info_dict['cameras'][info_dict['channel']]['FWC'],info_dict['cameras'][info_dict['channel']]['gain'],info_dict['cameras'][info_dict['channel']]['bits'],info_dict['cameras'][info_dict['channel']]['gain']*(2.**(info_dict['cameras'][info_dict['channel']]['bits'])-1)))
    f.write(
        "\nFull well capacity of 1 pixel: %.2f (electrons)"
        % (info_dict["cameras"][info_dict["channel"]]["FWC"])
    )
    f.write("\n\n--------- One pixel only------------------\n")
    f.write(
        "\nPhoto-electrons created: central pix for %d exposure(s) of %.2f sec \n"
        % (info_dict["Nexp"], info_dict["DIT_pix"])
    )
    f.write("\tby:\n")
    f.write("\t- Object:         %10.2f   (electrons)\n" % info_dict["Ftot_el_pix"])
    f.write(
        "\t- Sky:            %10.2f   (electrons)\n"
        % (info_dict["Sky_CountRate"] * info_dict["DIT_pix"])
    )
    f.write(
        "\t- Readout:        %10.2f   (electrons)\n"
        % info_dict["cameras"][info_dict["channel"]]["RN"]
    )
    f.write(
        "\t- Dark current:   %10.2f   (electrons)\n"
        % (info_dict["cameras"][info_dict["channel"]]["DC"] * info_dict["DIT_pix"])
    )
    f.write("\t- Digitization:   %10.2f   (electrons)\n" % info_dict["dig_noise"])

    f.write(
        "\nSNR: -central pixel: %.2f\n"
        % (
            np.sqrt(info_dict["Nexp"])
            * info_dict["Ftot_el_pix"]
            / np.sqrt(
                info_dict["Ftot_el_pix"]
                + info_dict["factor_ima"]
                * (
                    (
                        info_dict["cameras"][info_dict["channel"]]["RN"] ** 2.0
                        + info_dict["dig_noise"] ** 2.0
                    )
                    + info_dict["DIT_pix"]
                    * (
                        info_dict["cameras"][info_dict["channel"]]["DC"]
                        + info_dict["Sky_CountRate"]
                    )
                )
            )
        )
    )

    f.write(
        "\nTotal of electrons collected in the central pixel during an exposure time of %d seconds: %.2f \n"
        % (info_dict["DIT_pix"], info_dict["N_el_tot_pix1"])
    )
    if info_dict["N_el_tot_pix1"] > info_dict["cameras"][info_dict["channel"]]["FWC"]:
        f.write(
            "--> Central pixel saturated: number of electrons > Full well Capacity\n"
        )
    elif info_dict["N_el_tot_pix1"] > info_dict["cameras"][info_dict["channel"]][
        "gain"
    ] * (2.0 ** (info_dict["cameras"][info_dict["channel"]]["bits"]) - 1):
        f.write(
            "--> Central pixel saturated: number of electrons > number of digitizations\n"
        )
    elif (
        info_dict["N_el_tot_pix1"]
        > 1.0 / 2 * info_dict["cameras"][info_dict["channel"]]["FWC"]
    ):
        f.write(
            "--> Number of electrons in central pixel > 1/2 of Full well Capacity. Risk of non-linear response.\n"
        )
    else:
        f.write("--> No saturation\n")

    f.write(
        "\n\n\n--------- Integrated over %d pixels------------------\n"
        % info_dict["npix"]
    )

    f.write(
        "\nPhoto-electrons created: brightest pix |  total of %d pixels, %d exposure(s) of %.2f sec \n"
        % (info_dict["npix"], info_dict["Nexp"], info_dict["DIT"])
    )
    f.write("\tby:\n")
    f.write(
        "\t- Object:         %10.2f   |   %10.2f   (electrons)\n"
        % (
            info_dict["Ftot_el"] * info_dict["f_pix"] / info_dict["f_PSF"],
            info_dict["Ftot_el"],
        )
    )
    f.write(
        "\t- Sky:            %10.2f   |   %10.2f   (electrons)\n"
        % (
            info_dict["Sky_CountRate"] * info_dict["DIT"],
            (
                info_dict["Sky_CountRate"]
                * info_dict["npix"]
                * info_dict["DIT"]
                * info_dict["Nexp"]
            ),
        )
    )
    f.write(
        "\t- Readout:        %10.2f   |   %10.2f   (electrons)\n"
        % (
            info_dict["cameras"][info_dict["channel"]]["RN"],
            (
                info_dict["cameras"][info_dict["channel"]]["RN"]
                * info_dict["npix"]
                * info_dict["Nexp"]
            ),
        )
    )
    f.write(
        "\t- Dark current:   %10.2f   |   %10.2f   (electrons)\n"
        % (
            info_dict["cameras"][info_dict["channel"]]["DC"] * info_dict["DIT"],
            (
                info_dict["cameras"][info_dict["channel"]]["DC"]
                * info_dict["DIT"]
                * info_dict["npix"]
                * info_dict["Nexp"]
            ),
        )
    )
    f.write(
        "\t- Digitization:   %10.2f   |   %10.2f   (electrons)\n"
        % (
            info_dict["dig_noise"],
            (info_dict["dig_noise"] * info_dict["npix"] * info_dict["Nexp"]),
        )
    )
    # f.write ('\nTotal noise: %.2f \n' % (np.sqrt(Ftot_el * f_PSF * DIT *Nexp + Nexp*factor_ima * npix*((RN**2. + DigN**2.) + DIT * ( DC + BN )))))

    f.write(
        "\nSNR: -central pixel: %.2f\n"
        % (
            np.sqrt(info_dict["Nexp"])
            * info_dict["Ftot_el"]
            * info_dict["f_pix"]
            / info_dict["f_PSF"]
            / np.sqrt(
                info_dict["Ftot_el"] * info_dict["f_pix"] / info_dict["f_PSF"]
                + info_dict["factor_ima"]
                * (
                    (
                        info_dict["cameras"][info_dict["channel"]]["RN"] ** 2.0
                        + info_dict["dig_noise"] ** 2.0
                    )
                    + info_dict["DIT"]
                    * (
                        info_dict["cameras"][info_dict["channel"]]["DC"]
                        + info_dict["Sky_CountRate"]
                    )
                )
            )
        )
    )
    f.write(
        "     -integrated over %d pixels: %.2f\n"
        % (
            info_dict["npix"],
            (np.sqrt(info_dict["Nexp"]) * info_dict["Ftot_el"])
            / np.sqrt(
                info_dict["Ftot_el"]
                + info_dict["factor_ima"]
                * info_dict["npix"]
                * (
                    (
                        info_dict["cameras"][info_dict["channel"]]["RN"] ** 2.0
                        + info_dict["dig_noise"] ** 2.0
                    )
                    + info_dict["DIT"]
                    * (
                        info_dict["cameras"][info_dict["channel"]]["DC"]
                        + info_dict["Sky_CountRate"]
                    )
                )
            ),
        )
    )

    f.write(
        "\nTotal of electrons collected in the brightest pixel during an exposure time of %d seconds: %.2f \n"
        % (info_dict["DIT"], info_dict["N_el_tot_pix2"])
    )
    if info_dict["N_el_tot_pix2"] > info_dict["cameras"][info_dict["channel"]]["FWC"]:
        f.write(
            "--> Brightest pixel saturated: number of electrons > Full well Capacity \n"
        )
    elif info_dict["N_el_tot_pix2"] > info_dict["cameras"][info_dict["channel"]][
        "gain"
    ] * (2.0 ** (info_dict["cameras"][info_dict["channel"]]["bits"]) - 1):
        f.write(
            "--> Brightest pixel saturated: number of electrons > number of digitizations\n"
        )
    elif (
        info_dict["N_el_tot_pix2"]
        > 1.0 / 2 * info_dict["cameras"][info_dict["channel"]]["FWC"]
    ):
        f.write(
            "--> Number of electrons in brightest pixel > 1/2 of Full well Capacity. Risk of non-linear response.\n"
        )
    else:
        f.write("--> No saturation\n")

        f.write(
            "\nDead time: %.2f sec \n(%.2f sec for dithering, the %.2f sec for the readout are not taken into account)\n"
            % (
                info_dict["deadtime_tot"],
                info_dict["T_dithering"],
                info_dict["cameras"][info_dict["channel"]]["ReadoutTime"],
            )
        )
        f.close()
