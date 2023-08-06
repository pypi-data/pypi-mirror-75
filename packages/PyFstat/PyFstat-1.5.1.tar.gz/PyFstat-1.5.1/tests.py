import unittest
import numpy as np
import os
import shutil
import pyfstat
import lalpulsar
import logging
import time


class Test(unittest.TestCase):
    outdir = "TestData"

    @classmethod
    def setUpClass(self):
        if os.path.isdir(self.outdir):
            try:
                shutil.rmtree(self.outdir)
            except OSError:
                logging.warning("{} not removed prior to tests".format(self.outdir))
        self.h0 = 1
        self.cosi = 0
        self.sqrtSX = 1
        self.F0 = 30
        self.F1 = -1e-10
        self.F2 = 0
        self.minStartTime = 700000000
        self.duration = 2 * 86400
        self.maxStartTime = self.minStartTime + self.duration
        self.Alpha = 5e-3
        self.Delta = 1.2
        self.tref = self.minStartTime
        self.detectors = "H1"
        self.SFTWindowType = "tukey"
        self.SFTWindowBeta = 1.0
        Writer = pyfstat.Writer(
            F0=self.F0,
            F1=self.F1,
            F2=self.F2,
            label="test",
            h0=self.h0,
            cosi=self.cosi,
            sqrtSX=self.sqrtSX,
            outdir=self.outdir,
            tstart=self.minStartTime,
            Alpha=self.Alpha,
            Delta=self.Delta,
            tref=self.tref,
            duration=self.duration,
            Band=4,
            detectors=self.detectors,
            SFTWindowType=self.SFTWindowType,
            SFTWindowBeta=self.SFTWindowBeta,
            randSeed=None,
        )
        Writer.make_data()
        self.sftfilepath = Writer.sftfilepath

    @classmethod
    def tearDownClass(self):
        if os.path.isdir(self.outdir):
            try:
                shutil.rmtree(self.outdir)
            except OSError:
                logging.warning("{} not removed prior to tests".format(self.outdir))


class Writer(Test):
    label = "TestWriter"
    tested_class = pyfstat.Writer

    def test_make_cff(self):
        Writer = self.tested_class(label=self.label, outdir=self.outdir)
        Writer.make_cff()
        self.assertTrue(
            os.path.isfile(os.path.join(".", self.outdir, self.label + ".cff"))
        )

    def test_run_makefakedata(self):
        duration = 3600
        Writer = self.tested_class(
            label=self.label, outdir=self.outdir, duration=duration
        )
        Writer.make_cff()
        Writer.run_makefakedata()
        expected_outfile = os.path.join(
            ".",
            Writer.outdir,
            "H-2_H1_1800SFT_{}-{}-{}.sft".format(
                Writer.label, Writer.tstart, Writer.duration
            ),
        )
        self.assertTrue(os.path.isfile(expected_outfile))
        cl_validate = "lalapps_SFTvalidate " + expected_outfile
        pyfstat.helper_functions.run_commandline(
            cl_validate, raise_error=True, return_output=False
        )

    def test_makefakedata_usecached(self):
        Writer = self.tested_class(label=self.label, outdir=self.outdir, duration=3600)
        if os.path.isfile(Writer.sftfilepath):
            os.remove(Writer.sftfilepath)
        # first run: make everything from scratch
        Writer.make_cff()
        Writer.run_makefakedata()
        time_first = os.path.getmtime(Writer.sftfilepath)
        # second run: should re-use .cff and .sft
        Writer.make_cff()
        Writer.run_makefakedata()
        time_second = os.path.getmtime(Writer.sftfilepath)
        self.assertTrue(time_first == time_second)
        # third run: touch the .cff to force regeneration
        time.sleep(1)  # make sure timestamp is actually different!
        os.system("touch {}".format(Writer.config_file_name))
        Writer.run_makefakedata()
        time_third = os.path.getmtime(Writer.sftfilepath)
        self.assertFalse(time_first == time_third)

    def test_noise_sfts(self):
        duration_Tsft = 100
        Tsft = 1800
        h0 = 1000
        randSeed = 69420
        window = "tukey"
        window_beta = 0.01

        # create sfts with a strong signal in them
        noise_and_signal_writer = self.tested_class(
            label="test_noiseSFTs_noise_and_signal",
            outdir=self.outdir,
            h0=h0,
            duration=duration_Tsft * Tsft,
            Tsft=Tsft,
            randSeed=randSeed,
            SFTWindowType=window,
            SFTWindowBeta=window_beta,
        )
        sftfilepattern = os.path.join(
            noise_and_signal_writer.outdir,
            "*{}*{}-*sft".format(duration_Tsft, noise_and_signal_writer.label),
        )

        noise_and_signal_writer.make_data()

        # compute Fstat
        coherent_search = pyfstat.ComputeFstat(
            tref=noise_and_signal_writer.tref,
            sftfilepattern=sftfilepattern,
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
        )
        FS_1 = coherent_search.get_fullycoherent_twoF(
            noise_and_signal_writer.tstart,
            noise_and_signal_writer.tend,
            noise_and_signal_writer.F0,
            noise_and_signal_writer.F1,
            noise_and_signal_writer.F2,
            noise_and_signal_writer.Alpha,
            noise_and_signal_writer.Delta,
        )

        # create noise sfts and then inject a strong signal
        noise_writer = self.tested_class(
            label="test_noiseSFTs_only_noise",
            outdir=self.outdir,
            h0=0,
            duration=duration_Tsft * Tsft,
            Tsft=Tsft,
            randSeed=randSeed,
            SFTWindowType=window,
            SFTWindowBeta=window_beta,
        )
        noise_writer.make_data()

        add_signal_writer = self.tested_class(
            label="test_noiseSFTs_add_signal",
            outdir=self.outdir,
            h0=h0,
            duration=duration_Tsft * Tsft,
            Tsft=Tsft,
            sqrtSX=0,
            SFTWindowType=window,
            SFTWindowBeta=window_beta,
            noiseSFTs=os.path.join(
                noise_writer.outdir,
                "*{}*{}-*sft".format(duration_Tsft, noise_writer.label),
            ),
        )
        sftfilepattern = os.path.join(
            add_signal_writer.outdir,
            "*{}*{}-*sft".format(duration_Tsft, add_signal_writer.label),
        )
        add_signal_writer.make_data()

        # compute Fstat
        coherent_search = pyfstat.ComputeFstat(
            tref=add_signal_writer.tref,
            sftfilepattern=sftfilepattern,
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
        )
        FS_2 = coherent_search.get_fullycoherent_twoF(
            add_signal_writer.tstart,
            add_signal_writer.tend,
            add_signal_writer.F0,
            add_signal_writer.F1,
            add_signal_writer.F2,
            add_signal_writer.Alpha,
            add_signal_writer.Delta,
        )

        self.assertTrue(np.abs(FS_1 - FS_2) / FS_1 < 0.01)


class BinaryModulatedWriter(Writer):
    label = "TestBinaryModulatedWriter"
    tested_class = pyfstat.BinaryModulatedWriter


class Bunch(Test):
    def test_bunch(self):
        b = pyfstat.core.Bunch(dict(x=10))
        self.assertTrue(b.x == 10)


class par(Test):
    label = "TestPar"

    def test(self):
        parfile = os.path.join(self.outdir, self.label + ".par")
        os.system('echo "x=100\ny=10" > ' + parfile)

        par = pyfstat.core.read_par(parfile, return_type="Bunch")
        self.assertTrue(par.x == 100)
        self.assertTrue(par.y == 10)

        par = pyfstat.core.read_par(
            outdir=self.outdir, label=self.label, return_type="dict"
        )
        self.assertTrue(par["x"] == 100)
        self.assertTrue(par["y"] == 10)
        os.system("rm -r {}".format(self.outdir))


class BaseSearchClass(Test):
    def test_shift_matrix(self):
        BSC = pyfstat.BaseSearchClass()
        dT = 10
        a = BSC._shift_matrix(4, dT)
        b = np.array(
            [
                [
                    1,
                    2 * np.pi * dT,
                    2 * np.pi * dT ** 2 / 2.0,
                    2 * np.pi * dT ** 3 / 6.0,
                ],
                [0, 1, dT, dT ** 2 / 2.0],
                [0, 0, 1, dT],
                [0, 0, 0, 1],
            ]
        )
        self.assertTrue(np.array_equal(a, b))

    def test_shift_coefficients(self):
        BSC = pyfstat.BaseSearchClass()
        thetaA = np.array([10.0, 1e2, 10.0, 1e2])
        dT = 100

        # Calculate the 'long' way
        thetaB = np.zeros(len(thetaA))
        thetaB[3] = thetaA[3]
        thetaB[2] = thetaA[2] + thetaA[3] * dT
        thetaB[1] = thetaA[1] + thetaA[2] * dT + 0.5 * thetaA[3] * dT ** 2
        thetaB[0] = thetaA[0] + 2 * np.pi * (
            thetaA[1] * dT + 0.5 * thetaA[2] * dT ** 2 + thetaA[3] * dT ** 3 / 6.0
        )

        self.assertTrue(np.array_equal(thetaB, BSC._shift_coefficients(thetaA, dT)))

    def test_shift_coefficients_loop(self):
        BSC = pyfstat.BaseSearchClass()
        thetaA = np.array([10.0, 1e2, 10.0, 1e2])
        dT = 1e1
        thetaB = BSC._shift_coefficients(thetaA, dT)
        self.assertTrue(
            np.allclose(
                thetaA, BSC._shift_coefficients(thetaB, -dT), rtol=1e-9, atol=1e-9
            )
        )


class ComputeFstat(Test):
    def test_run_computefstatistic_single_point_injectSqrtSX(self):

        search = pyfstat.ComputeFstat(
            tref=self.minStartTime,
            minStartTime=self.minStartTime,
            maxStartTime=self.maxStartTime,
            detectors=self.detectors,
            injectSqrtSX=self.sqrtSX,
            minCoverFreq=self.F0 - 0.1,
            maxCoverFreq=self.F0 + 0.1,
        )
        FS = search.get_fullycoherent_twoF(
            tstart=self.minStartTime,
            tend=self.maxStartTime,
            F0=self.F0,
            F1=self.F1,
            F2=self.F2,
            Alpha=self.Alpha,
            Delta=self.Delta,
        )
        self.assertTrue(FS > 0.0)

    def test_run_computefstatistic_single_point_with_SFTs(self):
        Writer = pyfstat.Writer(
            label="TestComputeFstatSinglePoint",
            outdir=self.outdir,
            duration=86400,
            h0=1,
            sqrtSX=1,
            detectors="H1",
        )
        Writer.make_data()
        predicted_FS = Writer.predict_fstat()

        sftfilepattern = os.path.join(Writer.outdir, "*{}-*sft".format(Writer.label))

        search = pyfstat.ComputeFstat(
            tref=Writer.tref,
            sftfilepattern=sftfilepattern,
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
        )
        FS = search.get_fullycoherent_twoF(
            Writer.tstart,
            Writer.tend,
            Writer.F0,
            Writer.F1,
            Writer.F2,
            Writer.Alpha,
            Writer.Delta,
        )
        self.assertTrue(np.abs(predicted_FS - FS) / FS < 0.3)

        Writer.detectors = "H1"
        predicted_FS = Writer.predict_fstat()
        search = pyfstat.ComputeFstat(
            tref=Writer.tref,
            detectors="H1",
            sftfilepattern=sftfilepattern,
            SSBprec=lalpulsar.SSBPREC_RELATIVISTIC,
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
        )
        FS = search.get_fullycoherent_twoF(
            Writer.tstart,
            Writer.tend,
            Writer.F0,
            Writer.F1,
            Writer.F2,
            Writer.Alpha,
            Writer.Delta,
        )
        self.assertTrue(np.abs(predicted_FS - FS) / FS < 0.3)

    def test_run_computefstatistic_single_point_injectSources(self):
        # This seems to be writing with a signal...
        Writer = pyfstat.Writer(
            label="TestComputeFstatSinglePointInjectSources",
            outdir=self.outdir,
            add_noise=False,
            duration=86400,
            h0=1,
            sqrtSX=1,
        )
        Writer.make_cff()
        injectSources = Writer.config_file_name

        search = pyfstat.ComputeFstat(
            tref=Writer.tref,
            assumeSqrtSX=1,
            injectSources=injectSources,
            minCoverFreq=28,
            maxCoverFreq=32,
            minStartTime=Writer.tstart,
            maxStartTime=Writer.tstart + Writer.duration,
            detectors=Writer.detectors,
        )
        FS_from_file = search.get_fullycoherent_twoF(
            Writer.tstart,
            Writer.tend,
            Writer.F0,
            Writer.F1,
            Writer.F2,
            Writer.Alpha,
            Writer.Delta,
        )
        Writer.make_data()
        predicted_FS = Writer.predict_fstat()
        self.assertTrue(np.abs(predicted_FS - FS_from_file) / FS_from_file < 0.3)

        injectSourcesdict = pyfstat.core.read_par(Writer.config_file_name)
        injectSourcesdict["F0"] = injectSourcesdict["Freq"]
        injectSourcesdict["F1"] = injectSourcesdict["f1dot"]
        injectSourcesdict["F2"] = injectSourcesdict["f2dot"]
        search = pyfstat.ComputeFstat(
            tref=Writer.tref,
            assumeSqrtSX=1,
            injectSources=injectSourcesdict,
            minCoverFreq=28,
            maxCoverFreq=32,
            minStartTime=Writer.tstart,
            maxStartTime=Writer.tstart + Writer.duration,
            detectors=Writer.detectors,
        )
        FS_from_dict = search.get_fullycoherent_twoF(
            Writer.tstart,
            Writer.tend,
            Writer.F0,
            Writer.F1,
            Writer.F2,
            Writer.Alpha,
            Writer.Delta,
        )
        self.assertTrue(FS_from_dict == FS_from_file)

    def test_get_fully_coherent_BSGL(self):
        # first pure noise, expect lnBSGL<0
        search_H1L1 = pyfstat.ComputeFstat(
            tref=self.minStartTime,
            minStartTime=self.minStartTime,
            maxStartTime=self.maxStartTime,
            detectors="H1,L1",
            injectSqrtSX=np.repeat(self.sqrtSX, 2),
            minCoverFreq=self.F0 - 0.1,
            maxCoverFreq=self.F0 + 0.1,
            BSGL=True,
        )
        lnBSGL = search_H1L1.get_fullycoherent_twoF(
            tstart=self.minStartTime,
            tend=self.maxStartTime,
            F0=self.F0,
            F1=self.F1,
            F2=self.F2,
            Alpha=self.Alpha,
            Delta=self.Delta,
        )
        self.assertTrue(lnBSGL < 0)
        # now with an added signal, expect lnBSGL>0
        search_H1L1 = pyfstat.ComputeFstat(
            tref=self.minStartTime,
            minStartTime=self.minStartTime,
            maxStartTime=self.maxStartTime,
            detectors="H1,L1",
            injectSqrtSX=np.repeat(self.sqrtSX, 2),
            injectSources="{{Alpha={:g}; Delta={:g}; h0={:g}; cosi={:g}; Freq={:g}; f1dot={:g}; f2dot={:g}; refTime={:d};}}".format(
                self.Alpha,
                self.Delta,
                self.h0,
                self.cosi,
                self.F0,
                self.F1,
                self.F2,
                self.tref,
            ),
            minCoverFreq=self.F0 - 0.1,
            maxCoverFreq=self.F0 + 0.1,
            BSGL=True,
        )
        lnBSGL = search_H1L1.get_fullycoherent_twoF(
            tstart=self.minStartTime,
            tend=self.maxStartTime,
            F0=self.F0,
            F1=self.F1,
            F2=self.F2,
            Alpha=self.Alpha,
            Delta=self.Delta,
        )
        self.assertTrue(lnBSGL > 0)


class ComputeFstatNoNoise(Test):
    label = "TestComputeFstatSinglePointNoNoise"

    def setup_method(self, method):
        self.Writer = pyfstat.Writer(
            label=self.label,
            outdir=self.outdir,
            add_noise=False,
            duration=86400,
            h0=1,
            sqrtSX=0,
        )
        self.Writer.make_data()
        self.predicted_FS = self.Writer.predict_fstat(assumeSqrtSX=1)

    def test_run_computefstatistic_single_point_no_noise(self):

        search = pyfstat.ComputeFstat(
            tref=self.Writer.tref,
            assumeSqrtSX=1,
            sftfilepattern=os.path.join(
                self.Writer.outdir, "*{}-*sft".format(self.Writer.label)
            ),
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
        )
        FS = search.get_fullycoherent_twoF(
            self.Writer.tstart,
            self.Writer.tend,
            self.Writer.F0,
            self.Writer.F1,
            self.Writer.F2,
            self.Writer.Alpha,
            self.Writer.Delta,
        )
        self.assertTrue(np.abs(self.predicted_FS - FS) / FS < 0.3)

    def test_run_computefstatistic_single_point_no_noise_manual_ephem(self):

        # let's get the default ephemeris files (to be sure their paths exist)
        # and then pretend we pass them manually, to test those class options
        (
            earth_ephem_default,
            sun_ephem_default,
        ) = pyfstat.helper_functions.get_ephemeris_files()

        search = pyfstat.ComputeFstat(
            tref=self.Writer.tref,
            assumeSqrtSX=1,
            sftfilepattern=os.path.join(
                self.Writer.outdir, "*{}-*.sft".format(self.Writer.label)
            ),
            earth_ephem=earth_ephem_default,
            sun_ephem=sun_ephem_default,
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
        )
        FS = search.get_fullycoherent_twoF(
            self.Writer.tstart,
            self.Writer.tend,
            self.Writer.F0,
            self.Writer.F1,
            self.Writer.F2,
            self.Writer.Alpha,
            self.Writer.Delta,
        )
        self.assertTrue(np.abs(self.predicted_FS - FS) / FS < 0.3)


class SemiCoherentSearch(Test):
    label = "TestSemiCoherentSearch"

    def setup_method(self, method):
        self.Writer = pyfstat.Writer(
            label=self.label,
            outdir=self.outdir,
            duration=10 * 86400,
            h0=1,
            sqrtSX=1,
            detectors="H1,L1",
        )
        self.Writer.make_data()

    def test_get_semicoherent_twoF(self):

        search = pyfstat.SemiCoherentSearch(
            label=self.label,
            outdir=self.outdir,
            nsegs=2,
            sftfilepattern=os.path.join(
                self.Writer.outdir, "*{}-*sft".format(self.Writer.label)
            ),
            tref=self.Writer.tref,
            minStartTime=self.Writer.tstart,
            maxStartTime=self.Writer.tend,
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
            BSGL=False,
        )

        search.get_semicoherent_det_stat(
            self.Writer.F0,
            self.Writer.F1,
            self.Writer.F2,
            self.Writer.Alpha,
            self.Writer.Delta,
            record_segments=True,
        )

        # Compute the predicted semi-coherent Fstat for the first segment
        self.Writer.duration /= 2.0
        self.Writer.tend = self.Writer.tstart + self.Writer.duration
        FSA = self.Writer.predict_fstat()

        # same for second segment
        self.Writer.tstart += self.Writer.duration
        self.Writer.tend += self.Writer.duration
        FSB = self.Writer.predict_fstat()

        FSs = np.array([FSA, FSB])
        diffs = (np.array(search.twoF_per_segment) - FSs) / FSs
        self.assertTrue(np.all(diffs < 0.3))

    def test_get_semicoherent_BSGL(self):

        search = pyfstat.SemiCoherentSearch(
            label=self.label,
            outdir=self.outdir,
            nsegs=2,
            sftfilepattern=os.path.join(
                self.Writer.outdir, "*{}-*sft".format(self.Writer.label)
            ),
            tref=self.Writer.tref,
            minStartTime=self.Writer.tstart,
            maxStartTime=self.Writer.tend,
            minCoverFreq=-0.5,
            maxCoverFreq=-0.5,
            BSGL=True,
        )

        BSGL = search.get_semicoherent_det_stat(
            self.Writer.F0,
            self.Writer.F1,
            self.Writer.F2,
            self.Writer.Alpha,
            self.Writer.Delta,
            record_segments=True,
        )
        self.assertTrue(BSGL > 0)


class SemiCoherentGlitchSearch(Test):
    label = "TestSemiCoherentGlitchSearch"

    def test_get_semicoherent_nglitch_twoF(self):
        duration = 10 * 86400
        dtglitch = 0.5 * duration
        delta_F0 = 0
        h0 = 1
        sqrtSX = 1
        Writer = pyfstat.GlitchWriter(
            self.label,
            outdir=self.outdir,
            duration=duration,
            dtglitch=dtglitch,
            delta_F0=delta_F0,
            sqrtSX=sqrtSX,
            h0=h0,
        )

        Writer.make_data()

        keys = ["F0", "F1", "F2", "Alpha", "Delta"]
        search_ranges = {
            key: [
                getattr(Writer, key),
                getattr(Writer, key) + getattr(Writer, "delta_" + key, 0.0),
            ]
            for key in keys
        }
        search = pyfstat.SemiCoherentGlitchSearch(
            label=self.label,
            outdir=self.outdir,
            sftfilepattern=os.path.join(Writer.outdir, "*{}-*sft".format(Writer.label)),
            tref=Writer.tref,
            minStartTime=Writer.tstart,
            maxStartTime=Writer.tend,
            nglitch=1,
            search_ranges=search_ranges,
        )

        FS = search.get_semicoherent_nglitch_twoF(
            Writer.F0,
            Writer.F1,
            Writer.F2,
            Writer.Alpha,
            Writer.Delta,
            Writer.delta_F0,
            Writer.delta_F1,
            search.minStartTime + dtglitch,
        )

        # Compute the predicted semi-coherent glitch Fstat for the first half
        Writer.transientStartTime = Writer.tstart
        Writer.transientTau = dtglitch
        FSA = Writer.predict_fstat()
        # same for the second half (tau stays the same)
        Writer.transientStartTime += dtglitch
        FSB = Writer.predict_fstat()
        predicted_FS = FSA + FSB

        self.assertTrue(np.abs((FS - predicted_FS)) / predicted_FS < 0.3)


class MCMCSearch(Test):
    label = "TestMCMCSearch"
    h0 = 1
    sqrtSX = 1
    F0 = 30
    F1 = -1e-10
    F2 = 0
    minStartTime = 700000000
    duration = 1 * 86400
    maxStartTime = minStartTime + duration
    Alpha = 5e-3
    Delta = 1.2
    tref = minStartTime

    def test_fully_coherent_MCMC_fixedsky(self):

        Writer = pyfstat.Writer(
            F0=self.F0,
            F1=self.F1,
            F2=self.F2,
            label=self.label,
            h0=self.h0,
            sqrtSX=self.sqrtSX,
            outdir=self.outdir,
            tstart=self.minStartTime,
            Alpha=self.Alpha,
            Delta=self.Delta,
            tref=self.tref,
            duration=self.duration,
            Band=4,
        )
        Writer.make_data()

        predicted_FS = Writer.predict_fstat()

        theta = {
            "F0": {"type": "norm", "loc": self.F0, "scale": np.abs(1e-10 * self.F0)},
            "F1": {"type": "norm", "loc": self.F1, "scale": np.abs(1e-10 * self.F1)},
            "F2": self.F2,
            "Alpha": self.Alpha,
            "Delta": self.Delta,
        }

        search = pyfstat.MCMCSearch(
            label=self.label + "FixedSky",
            outdir=self.outdir,
            theta_prior=theta,
            tref=self.tref,
            sftfilepattern=os.path.join(self.outdir, "*{}-*sft".format(self.label)),
            minStartTime=self.minStartTime,
            maxStartTime=self.maxStartTime,
            nsteps=[100, 100],
            nwalkers=100,
            ntemps=2,
            log10beta_min=-1,
        )
        search.run(plot_walkers=False)
        _, FS = search.get_max_twoF()

        print(("Predicted twoF is {} while recovered is {}".format(predicted_FS, FS)))
        self.assertTrue(
            FS > predicted_FS or np.abs((FS - predicted_FS)) / predicted_FS < 0.3
        )

    def test_fully_coherent_MCMC_skyprior(self):

        Writer = pyfstat.Writer(
            F0=self.F0,
            F1=self.F1,
            F2=self.F2,
            label=self.label,
            h0=self.h0,
            sqrtSX=self.sqrtSX,
            outdir=self.outdir,
            tstart=self.minStartTime,
            Alpha=self.Alpha,
            Delta=self.Delta,
            tref=self.tref,
            duration=self.duration,
            Band=4,
        )
        Writer.make_data()

        predicted_FS = Writer.predict_fstat()

        theta = {
            "F0": {"type": "norm", "loc": self.F0, "scale": np.abs(1e-10 * self.F0)},
            "F1": {"type": "norm", "loc": self.F1, "scale": np.abs(1e-10 * self.F1)},
            "F2": self.F2,
            "Alpha": {
                "type": "unif",
                "lower": self.Alpha - 0.01,
                "upper": self.Alpha + 0.01,
            },
            "Delta": {
                "type": "unif",
                "lower": self.Delta - 0.01,
                "upper": self.Delta + 0.01,
            },
        }

        search = pyfstat.MCMCSearch(
            label=self.label + "SkyPrior",
            outdir=self.outdir,
            theta_prior=theta,
            tref=self.tref,
            sftfilepattern=os.path.join(self.outdir, "*{}-*sft".format(self.label)),
            minStartTime=self.minStartTime,
            maxStartTime=self.maxStartTime,
            nsteps=[100, 100],
            nwalkers=100,
            ntemps=2,
            log10beta_min=-1,
        )
        search.run(plot_walkers=False)
        _, FS = search.get_max_twoF()

        print(("Predicted twoF is {} while recovered is {}".format(predicted_FS, FS)))
        self.assertTrue(
            FS > predicted_FS or np.abs((FS - predicted_FS)) / predicted_FS < 0.3
        )


class GridSearch(Test):
    F0s = [29, 31, 0.1]
    F1s = [-1e-10, 0, 1e-11]
    tref = 700000000

    def test_grid_search(self):
        search = pyfstat.GridSearch(
            "grid_search",
            self.outdir,
            self.sftfilepath,
            F0s=self.F0s,
            F1s=[0],
            F2s=[0],
            Alphas=[0],
            Deltas=[0],
            tref=self.tref,
        )
        search.run()
        self.assertTrue(os.path.isfile(search.out_file))
        max2F_point = search.get_max_twoF()
        self.assertTrue(
            np.all(max2F_point["twoF"] >= search.data[:, search.keys.index("twoF")])
        )

    def test_grid_search_against_CFSv2(self):
        search = pyfstat.GridSearch(
            "grid_search",
            self.outdir,
            self.sftfilepath,
            F0s=self.F0s,
            F1s=[0],
            F2s=[0],
            Alphas=[0],
            Deltas=[0],
            tref=self.tref,
        )
        search.run()
        self.assertTrue(os.path.isfile(search.out_file))
        pyfstat_out = pyfstat.helper_functions.read_txt_file_with_header(
            search.out_file, comments="#"
        )
        CFSv2_out_file = os.path.join(self.outdir, "CFSv2_Fstat_out.txt")
        CFSv2_loudest_file = os.path.join(self.outdir, "CFSv2_Fstat_loudest.txt")
        cl_CFSv2 = []
        cl_CFSv2.append("lalapps_ComputeFstatistic_v2")
        cl_CFSv2.append("--Alpha 0 --Delta 0")
        cl_CFSv2.append("--AlphaBand 0 --DeltaBand 0")
        cl_CFSv2.append("--Freq {}".format(self.F0s[0]))
        cl_CFSv2.append("--f1dot 0 --f1dotBand 0 --df1dot 0")
        cl_CFSv2.append("--FreqBand {}".format(self.F0s[1] - self.F0s[0]))
        cl_CFSv2.append("--dFreq {}".format(self.F0s[2]))
        cl_CFSv2.append("--DataFiles " + self.sftfilepath)
        cl_CFSv2.append("--refTime {}".format(self.tref))
        earth_ephem, sun_ephem = pyfstat.helper_functions.get_ephemeris_files()
        if earth_ephem is not None:
            cl_CFSv2.append('--ephemEarth="{}"'.format(earth_ephem))
        if sun_ephem is not None:
            cl_CFSv2.append('--ephemSun="{}"'.format(sun_ephem))
        cl_CFSv2.append("--outputFstat " + CFSv2_out_file)
        cl_CFSv2.append("--outputLoudest " + CFSv2_loudest_file)
        # to match ComputeFstat default (and hence PyFstat) defaults on older
        # lalapps_CFSv2 versions, set the RngMedWindow manually:
        cl_CFSv2.append("--RngMedWindow=101")
        cl_CFSv2 = " ".join(cl_CFSv2)
        pyfstat.helper_functions.run_commandline(cl_CFSv2)
        self.assertTrue(os.path.isfile(CFSv2_out_file))
        self.assertTrue(os.path.isfile(CFSv2_loudest_file))
        CFSv2_out = pyfstat.helper_functions.read_txt_file_with_header(
            CFSv2_out_file, comments="%"
        )
        self.assertTrue(
            len(np.atleast_1d(CFSv2_out["2F"]))
            == len(np.atleast_1d(pyfstat_out["twoF"]))
        )
        self.assertTrue(np.max(np.abs(CFSv2_out["freq"] - pyfstat_out["F0"]) < 1e-16))
        self.assertTrue(np.max(np.abs(CFSv2_out["2F"] - pyfstat_out["twoF"]) < 1))
        self.assertTrue(np.max(CFSv2_out["2F"]) == np.max(pyfstat_out["twoF"]))

    def test_semicoherent_grid_search(self):
        search = pyfstat.GridSearch(
            "sc_grid_search",
            self.outdir,
            self.sftfilepath,
            F0s=self.F0s,
            F1s=[0],
            F2s=[0],
            Alphas=[0],
            Deltas=[0],
            tref=self.tref,
            nsegs=2,
        )
        search.run()
        self.assertTrue(os.path.isfile(search.out_file))

    def test_slice_grid_search(self):
        search = pyfstat.SliceGridSearch(
            "slice_grid_search",
            self.outdir,
            self.sftfilepath,
            F0s=self.F0s,
            F1s=self.F1s,
            F2s=[0.0],
            Alphas=[0.0],
            Deltas=[0.0],
            tref=self.tref,
            Lambda0=[30.0, 0.0, 0.0, 0.0],
        )
        fig, axes = search.run(save=False)
        self.assertTrue(fig is not None)

    def test_glitch_grid_search(self):
        search = pyfstat.GridGlitchSearch(
            "grid_grid_search",
            self.outdir,
            self.sftfilepath,
            F0s=self.F0s,
            F1s=self.F1s,
            F2s=[0],
            Alphas=[0],
            Deltas=[0],
            tref=self.tref,
            tglitchs=[self.tref],
        )
        search.run()
        self.assertTrue(os.path.isfile(search.out_file))

    def test_sliding_window(self):
        search = pyfstat.FrequencySlidingWindow(
            "grid_grid_search",
            self.outdir,
            self.sftfilepath,
            F0s=self.F0s,
            F1=0,
            F2=0,
            Alpha=0,
            Delta=0,
            tref=self.tref,
            minStartTime=self.minStartTime,
            maxStartTime=self.maxStartTime,
        )
        search.run()
        self.assertTrue(os.path.isfile(search.out_file))


class TransientGridSearch(Test):
    F0s = [29, 31, 0.1]
    F1s = [-1e-10, 0, 1e-11]
    tref = 700000000

    def test_transient_grid_search(self):
        search = pyfstat.TransientGridSearch(
            "grid_search",
            self.outdir,
            self.sftfilepath,
            F0s=self.F0s,
            F1s=[0],
            F2s=[0],
            Alphas=[0],
            Deltas=[0],
            tref=self.tref,
            minStartTime=self.minStartTime,
            maxStartTime=self.maxStartTime,
            transientWindowType="rect",
            t0Band=self.duration - 3600,
            tauBand=self.duration,
            outputTransientFstatMap=True,
            tCWFstatMapVersion="lal",
        )
        search.run()
        self.assertTrue(os.path.isfile(search.out_file))
        max2F_point = search.get_max_twoF()
        self.assertTrue(
            np.all(max2F_point["twoF"] >= search.data[:, search.keys.index("twoF")])
        )
        tCWfile = (
            search.tCWfilebase
            + "{:.16f}_{:.16f}_{:.16f}_{:.16g}_{:.16g}.dat".format(
                max2F_point["F0"],
                max2F_point["Alpha"],
                max2F_point["Delta"],
                max2F_point["F1"],
                max2F_point["F2"],
            )
        )
        tCW_out = pyfstat.helper_functions.read_txt_file_with_header(
            tCWfile, comments="#"
        )
        max2Fidx = np.argmax(tCW_out["2F"])
        self.assertTrue(
            np.isclose(max2F_point["twoF"], tCW_out["2F"][max2Fidx], rtol=1e-6, atol=0)
        )
        self.assertTrue(max2F_point["t0"] == tCW_out["t0s"][max2Fidx])
        self.assertTrue(max2F_point["tau"] == tCW_out["taus"][max2Fidx])


if __name__ == "__main__":
    unittest.main()
