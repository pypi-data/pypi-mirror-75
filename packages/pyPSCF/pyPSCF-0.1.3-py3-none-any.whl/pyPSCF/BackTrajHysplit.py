import os
import sys
from pathlib import Path
import numpy as np
import time
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar
import re
import json
import shutil
import pandas as pd
from multiprocessing import Process


class BT():

    """
    Compute the back-trajectory for the given station between dateMin and
    dateMax.

    Parameters
    ----------
    station : str
        The station
    lat : float
        Latitude of the starting point
    lon : float
        Longitude of the starting point
    alt : float
        Altitude of the starting point
    dateMin : str
        Starting date "YYYY-MM-DD HH:MM"
    dateMax : str
        Ending date "YYYY-MM-DD HH:MM"
    stepHH : int
        Interval between 2 starting hour
    hBT : int (negative)
        Number of hour to go in the past
    dirOutput : str
        path to the output directory
    dirGDAS : str
        path to the GDAS meteorological directory
    dirHysplit : str
        path to the hysplit root directory
    cpu : int
        Number of CPU to use. Beware, each of them is use to its maximum.

    """

    def __init__(self, station=None, lat=None, lon=None, alt=None,
                 dateMin=None, dateMax=None, stepHH=None, hBT=None,
                 dirOutput=None, dirGDAS=None, dirHysplit=None, cpu=None):

        # TODO: Check types of user input and if path actually exist.
        self.station = station
        self.dirOutput = Path(dirOutput).resolve()
        self.dirGDAS = Path(dirGDAS).resolve()

        self.dirHysplit = Path(dirHysplit).resolve()
        self.HysplitExecFile = (self.dirHysplit / "exec" / "hyts_std").resolve()
        if sys.platform == "win32":
            self.HysplitExecFile = (self.HysplitExecFile.with_suffix(".exe")).resolve()
        self.HysplitWorkingDir = (self.dirHysplit / "working").resolve()
        self.HysplitControlFile = (self.HysplitWorkingDir / "CONTROL").resolve()
        self.HysplitSetupFile = (self.HysplitWorkingDir / "SETUP.CFG").resolve()

        self.dateMin = pd.to_datetime(dateMin)
        self.dateMax = pd.to_datetime(dateMax)
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.stepHH = stepHH
        self.hBT = hBT
        self.cpu = cpu

        self.CONTROL_tpl = """{YY} {MM} {DD} {HH}
1
{lat} {lon} {alt}
{hBT}
0
10000.0
{nfiles}
{dirGDASandfile}
{dirOutput}/
{currentFile}
"""

        self.SETUP_tpl = """&SETUP
tratio = 0.25,
tout = 60,
tm_tpot = 0,
tm_tamb = 0,
tm_rain = 1,
tm_mixd = 0,
tm_relh = 0,
tm_sphu = 0,
tm_mixr = 0,
tm_dswf = 0,
tm_terr = 0,
/
"""


    def get_currentFile(self, station, d):
        """
        Return the name of the file given a station and a date

        Parameters
        ---------
        station : str
            The name of the station
        d : datetime
            The datetime of the backtrajectory

        Returns
        -------
        currentFile : str
            traj_{station}_{YYMMDDHH}
        """
        formatDate = dt.datetime.strftime(d, "%y%m%d%H")
        return "traj_"+station+"_"+formatDate

    def update_date(self, d, stepHH):
        """
        Update the date by a given step

        Parameters
        ----------
        d : datetime
            Previous datetime
        stepHH : int
            Number of hour to go forward

        Returns
        -------
        datetime : datetime
            d + stepHH
        """
        return d + pd.Timedelta(str(stepHH)+"H")

    def write_CONTROL_file(self, curDate, currentFile):
        """
        Create the correct CONTROL file for the given date

        Parameters
        ----------
        curDate : datetime
            The datetime to compute
        currentFile : str
            The name of the file
        """
        preDate = curDate + relativedelta(months=-1)
        mon = dt.datetime.strftime(preDate, "%b").lower()
        year = dt.datetime.strftime(preDate, "%y")
        files = []
        # previous month
        files = ["gdas1.{mon}{year}.w{i}".format(mon=mon, year=year, i=i) for i in range(3, 6)]
        # other file (all the current month)
        mon = dt.datetime.strftime(curDate, "%b").lower()
        year = dt.datetime.strftime(curDate, "%y")
        files += ["gdas1.{mon}{year}.w{i}".format(mon=mon, year=year, i=i) for i in range(1, 6)]
        for f in files:
            if not (self.dirGDAS / f).exists():
                files.remove(f)

        dirGDASandfile = ""
        for file in files:
            dirGDASandfile += "{dirGDAS}/\n{file}\n".format(dirGDAS=self.dirGDAS, file=file)
        dirGDASandfile = dirGDASandfile.strip()

        # Write the CONTROL file
        YY = dt.datetime.strftime(curDate, "%y")
        MM = dt.datetime.strftime(curDate, "%m")
        DD = dt.datetime.strftime(curDate, "%d")
        HH = dt.datetime.strftime(curDate, "%H")

        CONTROL = self.CONTROL_tpl.format(
            YY=YY, MM=MM, DD=DD, HH=HH,
            lat=self.lat, lon=self.lon, alt=self.alt, hBT=self.hBT,
            nfiles=len(files), dirGDASandfile=dirGDASandfile,
            dirOutput=self.dirOutput, currentFile=currentFile
        )

        with self.HysplitControlFile.open("w") as f:
            f.write(CONTROL)

    def write_SETUP_file(self):
        """Well... write the setup file
        """
        SETUP = self.SETUP_tpl.format()
        with self.HysplitSetupFile.open("w") as f:
            f.write(SETUP)

    def compute_BT(self, date, filename):
        """
        Compute the BT for the given datetime

        Parameters
        ----------
        date : datetime
            The datetime to compute
        filename : str
            The name of the output file
        """

        # Write the SETUP file
        self.write_SETUP_file()

        # Write the CONTROL file
        self.write_CONTROL_file(date, filename)

        # Execute hysplit
        print("Processing : ", filename)
        os.system(str(self.HysplitExecFile))

    def compute_BTs(self):
        """
        Compute all the BT from dateMin to dateMax
        """

        os.chdir(str(self.HysplitWorkingDir))
        curDate = self.dateMin
        while curDate <= self.dateMax:
            currentFile = self.get_currentFile(self.station, curDate)
            if Path(self.dirOutput / currentFile).exists():
                print("File already exist: ", currentFile)
                curDate = self.update_date(curDate, self.stepHH)
                continue
            with self.HysplitControlFile.open() as f:
                cfile = f.readlines()
            if cfile and (currentFile in cfile[-1].strip()):
                print("File is already processing: ", currentFile)
                curDate = self.update_date(curDate, self.stepHH)
                time.sleep(np.random.rand()*2)
                continue

            self.compute_BT(curDate, currentFile)
            curDate = self.update_date(curDate, self.stepHH)

    def run(self):
        """
        Run compute_BTs one time per cpu each in a subprocess.
        """

        for i in range(self.cpu):
            time.sleep(1)
            p = Process(target=self.compute_BTs)
            p.start()
        # block until the last process finish
        p.join()
