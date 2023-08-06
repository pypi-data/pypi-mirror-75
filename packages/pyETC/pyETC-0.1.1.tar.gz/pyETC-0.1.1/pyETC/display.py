#!/usr/bin/env python
# -*- coding: utf-8 -*-

def display(info_dict, results_dict):

    f = open("%s/results/result.txt" % info_dict["path"], "w")
    f.write(" Focal length (m): %f \n" % info_dict["foc_len"])
    f.write(" Pixel length on axis1 (m/pix): %f \n" % info_dict["pixsize1"])
    f.write(" Pixel length on axis2 (m/pix): %f \n" % info_dict["pixsize2"])
    f.write(
        " Pixel spatial sampling on axis1 (arcsec/pix): %f \n" % info_dict["scale1"]
    )
    f.write(
        " Pixel spatial sampling on axis2 (arcsec/pix): %f \n" % info_dict["scale2"]
    )
    f.write(" Pixel solid angle (arrsec2/pix): %f \n" % info_dict["solid_angle"])
    f.write(" Field of view of the CCD image on axis1 (deg): %f \n" % info_dict["FoV1"])
    f.write(" Field of view of the CCD image on axis1 (deg): %f \n" % info_dict["FoV1"])
    f.write(
        " Fwhm of the seeing at elevation (arcsec): %f \n" % info_dict["seeing_arcsec"]
    )
    f.write(
        " Fwhm of the seeing in the image plane (m): %f \n"
        % info_dict["Fwhm_psf_seeing"]
    )
    f.write(
        " Fhwm of the total PSF in the image plane (m): %f \n" % info_dict["Fwhm_psf"]
    )
    f.write(
        " Fhwm of the total PSF in the image plane (arcsec): %f \n"
        % info_dict["Fwhm_psf_arcsec"]
    )
    f.write(
        " Radius for integrated signal (arcsec): %f \n" % info_dict["radius_int_signal"]
    )
    f.write(" Number of pixels for integrated signal (pix): %f \n" % info_dict["npix"])
    f.write(
        " Factor for %f co_averaged images: %f \n"
        % (info_dict["images_averaged"], info_dict["factor_averaged"])
    )
    f.write("\n\nRESULTS\n")
    f.write(
        " Fraction of total flux for integrating the signal (area/total): %f \n"
        % results_dict["PSF_frac"]
    )
    f.write(
        " Flux fraction in the brightest pixel in the favorable case (max flux at the center of the pixel): %f \n"
        % results_dict["fpix_best"]
    )
    f.write(
        " Flux fraction in the brightest pixel in the worst case (max flux at the corner of the pixel): %f \n"
        % results_dict["fpix_worst"]
    )
    f.write(
        " Flux fraction in the brightest pixel in the intermediate case: %f \n"
        % results_dict["fpix_mid"]
    )
    f.write(
        " Total Flux of the object absorbed by the atmosphere and optics (photons/object): %f \n"
        % results_dict["Ftot_ph"]
    )
    f.write(
        " Total flux of the object absorbed by the atmosphere and optics (electrons/object): %f \n"
        % results_dict["Ftot_el"]
    )
    f.write(
        " Brightest pixel flux of the object after passing through the optics (electrons_pixel): %f \n"
        % results_dict["Fpix_el"]
    )
    f.write(
        " Total flux of the sky absorbed by optics (photons/pixel): %f \n"
        % results_dict["Skypix_ph"]
    )
    f.write(
        " Total flux of the sky absorbed by optics (electrons/pixel): %f \n"
        % results_dict["Skypix_el"]
    )
    f.write(" EMCCD excess noise factor: %f \n" % results_dict["fex"])
    f.write(" Thermal signal: (electrons/pixels): %f \n" % results_dict["S_th"])
    f.write(" Sky signal (electrons/pixel): %f \n" % results_dict["S_sky"])
    f.write(
        " Brightest pixel object signal (electrons/pixel): %f \n" % results_dict["S_ph"]
    )
    f.write(" Thermal noise (elcectrons/pixel): %f \n" % results_dict["N_th"])
    f.write(" Sky noise (elctrons/pixel): %f \n" % results_dict["N_sky"])
    f.write(
        " Brightest pixel object noise (electrons/pixel): %f \n" % results_dict["N_ph"]
    )
    f.write(
        " Converter analog to digital noise of 1/2 ADU (electrons/pixel): %f \n"
        % results_dict["N_cn"]
    )
    f.write(" Total noise (elcetrons/pixels): %f \n" % results_dict["N_tot"])
    f.write(
        " Peak SNR (Object signal / noise at the brightest pixel): %f \n"
        % results_dict["peak_SNR_obj"]
    )
    f.write(
        " Integrated thermal signal (electrons/area): %f \n"
        % results_dict["integ_S_th"]
    )
    f.write(
        " Integrated sky signal (electrons/area): %f \n" % results_dict["integ_S_sky"]
    )
    f.write(
        " Integrated Object signal (electrons/area): %f \n" % results_dict["integ_S_ph"]
    )
    f.write(
        " Integrated thermal noise (electrons/area): %f \n" % results_dict["integ_N_th"]
    )
    f.write(
        " Integrated sky noise (electrons/pixel): %f \n" % results_dict["integ_N_sky"]
    )
    f.write(
        " Integrated object noise (electrons/area): %f \n" % results_dict["integ_N_ph"]
    )
    f.write(
        " Integrated converter analog to digital noise of 1/2 ADU (electrons/area): %f \n"
        % results_dict["integ_N_cn"]
    )
    f.write(
        " Integrated readout noise (electrons/pixel): %f \n"
        % results_dict["integ_N_ro"]
    )
    f.write(
        " Total integrated noise over npix (electrons/area): %f \n"
        % results_dict["integ_N_tot"]
    )
    f.write(
        " Integrated SNR (Object signal / noise over %f pixels): %f \n"
        % (results_dict["npix"], results_dict["integ_SNR_obj"])
    )
