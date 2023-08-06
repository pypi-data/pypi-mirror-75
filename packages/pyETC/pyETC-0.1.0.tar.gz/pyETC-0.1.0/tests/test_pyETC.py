#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyETC` package."""

import pytest
import numpy as np
import numpy.testing as npt

from click.testing import CliRunner

from pyETC import cli
from pyETC.pyETC import etc


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "pyETC.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_simple_run():
    """Test that one can make a run"""
    # load ETC with a config file and the COLIBRI caracteristics
    _etc = etc(configFile="example.hjson", name_telescope="colibri")
    _etc.information["object_type"] = "magnitude"

    # Execute
    _etc.sim()
    #  1 decimal only.
    npt.assert_almost_equal(np.round(_etc.information["SNR"], 1),
                            70.66,
                            decimal=1)


@pytest.mark.parametrize("etc_type", ["time", "mag"])
def test_spectrum(etc_type):
    """Test ETC using spectrum"""
    _etc = etc(configFile="example.hjson", name_telescope="colibri")
    _etc.information["etc_type"] = etc_type
    # Specify that the object is a spectrum
    _etc.information["object_type"] = "spectrum"

    # Define the folder. Starting from pyETC/pyETC directory
    _etc.information["object_folder"] = "/data/calspec/"

    # Define the file in this folder
    _etc.information["object_file"] = "bd02d3375_stis_001.txt"
    _etc.information["Nexp"] = 3
    _etc.information["SNR"] = 1000

    # Specify the channel
    _etc.information["channel"] = "CAGIRE"

    #  Select the z filter band
    _etc.information["filter_band"] = "J"
    _etc.information["photometry_system"] = "vega"
    _etc.information["moon_age"] = -2

    # Execute
    _etc.sim()

    if etc_type == "mag":
        npt.assert_almost_equal(_etc.information["mag"], 10.0, decimal=1)
    elif etc_type == "time":
        Texp = _etc.information["DIT"] * _etc.information["Nexp"]
        npt.assert_almost_equal(Texp, 4.7, decimal=1)


def test_grb_sim_gs02():
    """Test result with synchrotron model of Granot and Sari 2002"""

    _etc = etc(configFile="example.hjson", name_telescope="colibri")
    _etc.information["object_type"] = "grb_sim"
    _etc.information["grb_model"] = "gs02"
    _etc.information["grb_redshift"] = 3
    _etc.information["t_sinceBurst"] = 0.2
    _etc.information["E_iso"] = 1e53
    _etc.information["eta"] = 0.3
    _etc.information["eps_b"] = 1e-4
    _etc.information["eps_e"] = 0.1
    _etc.information["p"] = 2.2
    _etc.information["n0"] = 1
    _etc.information["Y"] = 0
    _etc.information["ism_type"] = 0
    _etc.information["host_extinction_law"] = "smc"
    _etc.information["Av_Host"] = 0.2
    _etc.information["galactic_extinction_law"] = "smc"
    _etc.information["IGM_extinction_model"] = "meiksin"
    _etc.information["Av_galactic"] = 0.1

    _etc.sim()

    npt.assert_almost_equal(_etc.information["SNR"], 0.5, decimal=1)
