#!/usr/bin/env python3
# coding: utf-8
# XMM/INT Python Parameter Archive Plotting Libary: paPlot
# (c) 2020 Nikolai von Krusenstiern
# Based on provided MustLink code
# License (TBD)
# In[2]:
# DEBUG Global variables
# Flag by Hand for interactive CODE testing
forceCronMinutes = 60
forceVerbose = True
forceDebug = False
forceInspect = False
forceTimer = False
forceQuickCheck = False

# Needed for first function
DEBUG = ""


# In[3]:


import sys

# How to install packages into Jupyter:
# From: https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/
#!{sys.executable} -m pip install requests_cache


# In[4]:


## Imports

# Read Configuration JSON file: config.json
import json
from json_minify import json_minify  # Allows Comments in JSON Config files :-)


import pandas as pd
import matplotlib.pyplot as plt

# import matplotlib.dates as dates

# To avoid a "OverflowError: Exceeded cell block limit (set 'agg.path.chunksize' rcparam)"
# See https://stackoverflow.com/questions/37470734/matplotlib-giving-error-overflowerror-in-draw-path-exceeded-cell-block-limit
import matplotlib as mpl

mpl.rcParams["agg.path.chunksize"] = 10000

import re
from IPython.display import display

# import collections

import datetime as DT
import subprocess
import os

# import logging
from pathlib import Path


import functools
import time
from time import process_time

import inspect

if sys.version_info[0] >= 3 and sys.version_info[1] >= 7:
    from contextlib import nullcontext

from requests.exceptions import ConnectionError, Timeout


# In[5]:


import socket

# JSON Cache Manager
import requests
import requests_cache
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# In[6]:


# assert False


# In[7]:


# Parameter Archive (PA) Global Varaiables

paUser = ""
paHost = ""
paPath = ""

paBaseUrl = ""
paCredentials = ""
paLinkToken = ""

# API: http://testsenmust.esoc.esa.int:8083/webclient-must/mustlink/api-docs/index.html


# In[8]:


# Plot Global Variables

# Files
stdDataProvider = ""

# Request
stdTimeOut = 150.0  # 2,5 Minutes
stdTimeOutShort = 30.0  # Seconds
stdTimeOutLong = 600.0  # 10 Minutes

# JSON Cache
stdChop = ""

# Data
stdDays = ""
stdResampleTime = ""

# Plot Name Meta
stdPlotTitle = ""  # Tank_Tempertures
stdFileNameBase = ""  # Tanks_All
stdFileNameAddOn = ""  # 1w
stdFileNameExtension = ""  # png

# Plot Meta
stdColorList = {}
stdXLabel = ""

stdTimeStart = ""
stdTimeStop = ""

# Plot Data
tmName = {}
tmUnit = {}
unitLeft = ""
unitRight = ""

# SCP
filesToScp = []

# Global Time
stdTimeStamp = ""
stdTimeStampStr = ""
stdDateToday = ""
stdDateTodayNoon = ""
stdDateTodayEvening = ""


# In[9]:


def readConfig():
    """
    - read configuration from configuration JSON file: config.json
    """
    debug()

    global paLinkToken
    global paBaseUrl
    global paCredentials

    # Read Config JSON FIle
    with open("config.json.works") as configFile:
        config = json.loads(json_minify(configFile.read()))

        # get Values
        paBaseUrl = config["_ppLinkBaseUrl"]

        paCredentials = {
            "username": config["_ppLinkUsername"],
            "password": config["_ppLinkPassword"],
        }


# In[10]:


def getEnviroment():
    """
    Get Enviroment from calling shell, if any
    - will overwrite settings in config.json
    """
    debug()

    global CRON
    global VERBOSE
    global DEBUG
    global INSPECT
    global TIMER

    CRON = os.environ.get("cron")
    if forceCronMinutes:
        CRON = forceCronMinutes
    elif CRON is not None and CRON:
        CRON = CRON
    else:
        CRON = False

    VERBOSE = os.environ.get("verbose")
    if forceVerbose or (VERBOSE is not None and VERBOSE):
        VERBOSE = True
    else:
        VERBOSE = False

    # debug from Enviroment
    DEBUG = os.environ.get("debug")
    if forceDebug or (DEBUG is not None and DEBUG):
        DEBUG = True
    else:
        DEBUG = False

    # inspect from Enviroment
    INSPECT = os.environ.get("inspect")
    if forceInspect or (INSPECT is not None and INSPECT):
        INSPECT = True
    else:
        INSPECT = False

    # timer from Enviroment
    TIMER = os.environ.get("timer")
    if forceTimer or (TIMER is not None and TIMER):
        TIMER = True
    else:
        TIMER = False


# In[11]:


def debug():
    """
    Log function name to stdOut
    """
    if DEBUG:
        print(f"Function: {inspect.stack()[1].function}")


# In[12]:


def verbose(verboseString):
    """
    Log STRING to stdOut
    """
    if VERBOSE:
        print(f"Verbose: {inspect.stack()[1].function}: {verboseString}")


# In[13]:


def timer(func):
    """
    Print runtime of the decorated function
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1

        value = func(*args, **kwargs)

        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3

        if TIMER:
            print(f"Finished {func.__name__!r} in {run_time:.0f} secs")

        return value

    return wrapper_timer


# In[14]:


def installRequestCache():
    """
    init request Cache Manager
    """
    debug()

    requests_cache.install_cache(
        "PA_cache", backend="sqlite", expire_after=60 * 60 * 24 * 2
    )

    requests_cache.remove_expired_responses()


# In[15]:


def login(timeOut=None):
    """
   Login to MUSTLink with credentials from config.json
   """
    if timeOut is None:
        timeOut = stdTimeOut

    debug()
    global paLinkToken

    # Build URI
    header = {"content-type": "application/json"}

    verbose(f"Login - Timeout: {timeOut}")

    # Login
    try:
        response = requests.post(
            paBaseUrl + "/auth/login",
            data=json.dumps(paCredentials),
            headers=header,
            timeout=timeOut,
        )
    except ConnectionError as e:
        print(e)
        response = None

    except Timeout as e:
        print(e)
        response = None

    # Check
    if response is not None and response.status_code == 200:
        paLinkToken = response.json()["token"]
        verbose("Logged in successfully")
        return True
    else:
        print("Login failed")
        return False


# In[16]:


def mustLinkRequest(
    path, mode="GET", payload=None, cache=None, timeOut=None,
):
    """
    Do a GET or POST request
    For performing HTTP requests to mustlink.
    It is implemented here for reusability, as all subsequent MUSTLink requests will call this function.
    It attempts to authenticate first if needed.
    """
    debug()

    if cache is None:
        cache = False
    if timeOut is None:
        timeOut = stdTimeOut

    url = paBaseUrl + path

    # Not logged in yet, attempt to login and return if it fails
    if paBaseUrl == "" or paLinkToken == "":
        if not login(timeOut=stdTimeOutShort):
            return

    # Build URI
    header = {
        "Authorization": paLinkToken,
        "content-type": "application/json",
    }

    # With or Without cache...
    if mode == "GET":

        verbose(f"Get - Timeout: {timeOut}")

        if cache and sys.version_info[0] >= 3 and sys.version_info[1] >= 7:
            cm = nullcontext()
        else:
            cm = requests_cache.disabled()

        # Query Must
        with cm:
            response = requests.get(paBaseUrl + path, headers=header, timeout=timeOut,)

    elif mode == "POST":
        verbose(f"Post - Timeout: {timeOut}")
        response = requests.post(
            paBaseUrl + path, data=json.dumps(payload), headers=header, timeout=timeOut,
        )

    # Check
    if response.status_code == 401:
        print("Not authorized, attempting to log in again")

        if login(timeOut=stdTimeOutShort):
            return mustLinkRequest(path, mode, payload)
        else:
            return
    else:
        return response


# In[17]:


def getFromMustDataProviders():
    """
    get List of Data Providers
    """
    debug()

    return mustLinkRequest("/dataproviders", cache=False, timeOut=stdTimeOutShort,)

    # INTEGRAL
    # INTEGRALAND
    # INTEGRALGRD
    # INTEGRALRT
    # INTEGRALRTGRD
    # Profiles
    # Scripts
    # XMM
    # XMMAND
    # XMMGRD


# In[18]:


def getFromMustAsJson(
    myParameterList,
    dataProvider=None,
    timeStart=None,
    timeStop=None,
    cache=None,
    timeOut=None,
):
    """
    get from dataProvider
    myParameterList
    from: timeStart
    to: timeStop
    """

    if dataProvider is None:
        dataProvider = stdDataProvider
    if timeStart is None:
        timeStart = stdTimeStart
    if timeStop is None:
        timeStop = stdTimeStop

    if cache is None:
        cache = False
    if timeOut is None:
        timeOut = stdTimeOut

    debug()

    # We need a long csv String, not a List
    myParameterNames = ",".join(map(str, myParameterList))

    verbose(f"Request: {dataProvider} {myParameterList} from {timeStart} to {timeStop}")

    # Get the DATA from MUST
    response = mustLinkRequest(
        f"/dataproviders/{dataProvider}/parameters/data?key=name&values={myParameterNames}&from={timeStart}&to={timeStop}",
        cache=cache,
    )

    verbose(f"Request: done")

    return response


# In[19]:


def getFromMustAsDataFrame(
    myParameterList,
    dataProvider=None,
    timeStart=None,
    timeStop=None,
    cache=None,
    timeOut=None,
):
    if dataProvider is None:
        dataProvider = stdDataProvider
    if timeStart is None:
        timeStart = stdTimeStart
    if timeStop is None:
        timeStop = stdTimeStop
    if cache is None:
        cache = False
    if timeOut is None:
        timeOut = stdTimeOut

    # Init
    debug()
    global tmUnit
    global unitLeft
    global unitRight

    dfMust = pd.DataFrame()
    tmUnit.clear()
    unitLeft = ""
    unitRight = ""

    # Get JSON
    response = getFromMustAsJson(
        myParameterList,
        dataProvider=dataProvider,
        timeStart=timeStart,
        timeStop=timeStop,
        cache=cache,
        timeOut=timeOut,
    )

    # Lopp through the TM Parameters
    for element in response.json():

        # Get from JSON
        dfData = pd.DataFrame(element["data"])
        dfMeta = pd.DataFrame(element["metadata"])

        if len(dfData) <= 0:

            # Empty JSON
            dfMust = None

        else:
            # Convert date to UTC timestamp and set it as index
            dfData["date"] = pd.to_datetime(dfData["date"], unit="ms", utc=True)
            dfData = dfData.set_index("date")

            # Replace the column name of the dataframe from value to the parameter name
            parameterNameArray = dfMeta.loc[dfMeta["key"] == "name"]["value"]
            parameterDescriptionArray = dfMeta.loc[dfMeta["key"] == "description"][
                "value"
            ]
            parameterUnitArray = dfMeta.loc[dfMeta["key"] == "unit"]["value"]

            # get Meta Details
            parameterName = parameterNameArray[1]
            parameterDescription = parameterDescriptionArray[2]

            # Some TM does NOT have a UNIT
            try:
                parameterUnit = parameterUnitArray[6]
            except (IndexError, KeyError):
                parameterUnit = ""

            # Rename Column Header with Parameter Description and Name
            newName = f"{parameterDescription} ({parameterName})"
            dfData = dfData.rename(columns={"value": newName})

            # Handle Units
            tmUnit[parameterName] = parameterUnit

            if parameterUnit:
                if not unitLeft:
                    unitLeft = parameterUnit
                else:
                    if not unitRight and parameterUnit != unitLeft:
                        unitRight = parameterUnit

            # Append to DF
            dfTemp = dfMust.append(dfData, sort=False)
            dfMust = dfTemp

            if INSPECT:
                display(dfMust)
                display(dfMeta)

    return dfMust


# In[20]:


def getAsDataFrame(
    myParameterList,
    dataProvider=None,
    chop=None,
    timeStart=None,
    timeStop=None,
    timeOut=None,
):
    if dataProvider is None:
        dataProvider = stdDataProvider
    if chop is None:
        chop = stdChop
    if timeOut is None:
        timeOut = stdTimeOut
    if timeStart is None:
        timeStart = stdTimeStart
    if timeStop is None:
        timeStop = stdTimeStop

    debug()

    # Get Data from Must
    # Chop
    timeStartDT = pd.to_datetime(timeStart, utc=True)
    timeStopDT = pd.to_datetime(timeStop, utc=True)

    if chop and timeStartDT < stdDateToday < timeStopDT:
        beforeToday = stdDateToday - DT.timedelta(seconds=1)

        verbose(f"df1: {timeStart}-{beforeToday}: True")
        df1 = getFromMustAsDataFrame(
            myParameterList,
            dataProvider=dataProvider,
            timeStart=timeStartDT,
            timeStop=beforeToday,
            cache=True,
            timeOut=timeOut,
        )

        if stdTimeStamp > stdDateTodayEvening:
            beforeTodayEvening = stdDateTodayEvening - DT.timedelta(seconds=1)

            verbose(f"dfa: {stdDateToday}-{beforeTodayEvening}: True")
            dfa = getFromMustAsDataFrame(
                myParameterList,
                dataProvider=dataProvider,
                timeStart=stdDateToday,
                timeStop=beforeTodayEvening,
                cache=True,
                timeOut=timeOut,
            )

            verbose(f"dfb: {stdDateTodayEvening}-{timeStop}: False")
            dfb = getFromMustAsDataFrame(
                myParameterList,
                dataProvider=dataProvider,
                timeStart=stdDateTodayEvening,
                timeStop=timeStopDT,
                cache=False,
                timeOut=timeOut,
            )

            if dfb is not None:
                df2 = pd.concat([dfa, dfb])
            else:
                df2 = dfa

        else:
            verbose(f"df2: {stdDateToday}-{timeStop}: False")
            df2 = getFromMustAsDataFrame(
                myParameterList,
                dataProvider=dataProvider,
                timeStart=stdDateToday,
                timeStop=timeStopDT,
                cache=False,
                timeOut=timeOut,
            )

        if df2 is not None:
            df = pd.concat([df1, df2])
            verbose("CONCAT")
        else:
            df = df1
            verbose("SINGLE")

    else:
        verbose(f"df: {timeStart}-{timeStop}: False")
        df = getFromMustAsDataFrame(
            myParameterList,
            dataProvider=dataProvider,
            timeStart=timeStartDT,
            timeStop=timeStopDT,
            cache=False,
            timeOut=timeOut,
        )

    # We don't need this column
    df.drop(["calibratedValue"], axis=1, inplace=True)

    if INSPECT:
        display(df)

    return df


# In[21]:


def getTimeRangeOfDataFrame(df):
    debug()

    # get first and last element of DF
    timeFirst = df.index[0]
    timeLast = df.index[-1]

    # cast to String
    timeFirstStr = timeFirst.strftime("%Y-%m-%d %H:%M")
    timeLastStr = timeLast.strftime("%Y-%m-%d %H:%M")

    return (timeFirstStr, timeLastStr)


# In[22]:


def linePloter(
    df,
    myParameterList,
    resampleTime=None,
    timeFirstStr=None,
    timeLastStr=None,
    fileName=None,
    plotTitle=None,
    colorList=None,
    xLabel=None,
    y1Label=None,
    y2Label=None,
    y1Lim=None,
    y2Lim=None,
):

    # Get uniq list of UNITS
    # unitList = set( unit for dic in tmUnit for unit in tmUnit.values())
    # print(unitList)

    verbose(fileName)

    if y1Label is None:
        y1Label = unitLeft
    if y2Label is None:
        y2Label = unitRight

    # Collect TM Parameter wich havbe a different Unit that y1Label, for right Axis
    if y1Label:
        axis2List = [
            x
            for x in df.columns
            if (
                tmUnit[re.search(r"\((\w+)\)", x).group(1)].casefold()
                != (y1Label).casefold()
            )
        ]

    # Set Plot Title
    if resampleTime is None or resampleTime == 0:
        resampleString = ""
    else:
        resampleString = f"Resampled every {resampleTime}. "

    title = f"{plotTitle}: Data from {timeFirstStr}z to {timeLastStr}z. {resampleString}Plotted @ {stdTimeStampStr}z (NvK/{stdLocalHostName})"
    verbose(f"Ploting {title}")

    # Plot
    ax = df.plot(
        title=title, color=colorList, x_compat=True, grid=True, secondary_y=axis2List
    )

    # Prepare for potential 2nd axis
    fig = ax.get_figure()
    ax = fig.get_axes()

    # Add lables
    ax[0].set_ylabel(y1Label)
    ax[0].set_ylim(y1Lim)
    ax[0].set_xlabel(xLabel)

    # Add 2nd Axis
    if axis2List:
        ax[1].set_ylabel(y2Label)
        ax[1].set_ylim(y2Lim)

    # Save as PNG or other, depending on file name suffix
    plt.tight_layout()
    plt.savefig(
        fileName, dpi=300,
    )
    plt.close()

    # add to list to SCP later
    filesToScp.append(fileName)

    verbose(fileName)


# In[23]:


@timer
def linePlotTm(
    myParameterList,
    dataProvider=None,
    chop=None,
    timeOut=None,
    timeStart=None,
    timeStop=None,
    resampleTime=None,
    plotTitle=None,
    fileName=None,
    fileNameBase=None,
    fileNameAddOn=None,
    fileNameExtension=None,
    colorList=None,
    xLabel=None,
    y1Label=None,
    y2Label=None,
    y1Lim=None,
    y2Lim=None,
):

    global filesToScp

    if dataProvider is None:
        dataProvider = stdDataProvider
    if chop is None:
        chop = stdChop
    if timeOut is None:
        timeOut = stdTimeOut

    if resampleTime is None:
        resampleTime = stdResampleTime

    if plotTitle is None:
        plotTitle = stdPlotTitle
    if fileNameBase is None:
        fileNameBase = f"{urlify(plotTitle)}"
    if fileNameAddOn is None:
        fileNameAddOn = stdFileNameAddOn
    if fileNameExtension is None:
        fileNameExtension = stdFileNameExtension

    if colorList is None:
        colorList = stdColorList
    if xLabel is None:
        xLabel = stdXLabel

    # File Name handling
    if fileName is None:
        fileName = f"{fileNameBase}_{fileNameAddOn}.{fileNameExtension}"
    if os.path.splitext(fileName)[1] is None:
        fileName = f"{fileName}.{fileNameExtension}"

    debug()

    # Skip, in case CRON Jobs overrun each other ...
    if CRON and isinstance(CRON, int) and CRON > 1 and os.path.isfile(fileName):
        if int((time.time() - os.path.getmtime(fileName)) / 60) < int(CRON * 0.9):
            return "Skipped"

    # touch file, so others can skip
    Path(fileName).touch(exist_ok=True)

    # Get data from Must
    dfIn = getAsDataFrame(
        myParameterList,
        dataProvider=dataProvider,
        chop=chop,
        timeStart=timeStart,
        timeStop=timeStop,
        timeOut=timeOut,
    )
    if y1Label is None:
        y1Label = unitLeft

    # Resample in DF
    if resampleTime != 0:
        df = dfIn.resample(resampleTime).last()
    else:
        df = dfIn

    # Get first and last Sample in DF
    (timeFirstStr, timeLastStr) = getTimeRangeOfDataFrame(df)

    # Optional: Beautify TM Description
    ## What a HACK, had to inclute the RE inside the List Comprehension
    df.columns = [
        tmName[re.search(r"\((\w+)\)", x).group(1)]
        if re.search(r"\((\w+)\)", x).group(1) in tmName
        else x
        for x in df.columns
    ]

    # Now PLOT!
    linePloter(
        df,
        myParameterList,
        timeFirstStr=timeFirstStr,
        timeLastStr=timeLastStr,
        resampleTime=resampleTime,
        fileName=fileName,
        plotTitle=plotTitle,
        colorList=colorList,
        xLabel=xLabel,
        y1Label=y1Label,
        y2Label=y2Label,
        y1Lim=y1Lim,
        y2Lim=y2Lim,
    )

    return plotTitle


# In[24]:


def urlify(string):

    # Remove all non-word characters (everything except numbers and letters)
    string = re.sub(r"[^\w\s]", "", string)

    # Replace all runs of whitespace with a single dash
    string = re.sub(r"\s+", "-", string)

    return string


# In[25]:


def scpFiles(remoteUser=None, remoteHost=None, remotePath=None):
    """
    SCP PNG files to web-server
    """
    debug()

    if remoteUser is None:
        remoteUser = paUser
    if remoteHost is None:
        remoteHost = paHost
    if remotePath is None:
        remotePath = paPath

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((remoteHost, 22))
    if result == 0:
        filesToScpCount = len(filesToScp)
        verbose(f"SCP: {filesToScp}: {filesToScpCount}")

        remote_url = f"{remoteUser}@{remoteHost}:{remotePath}"

        for file in filesToScp:
            process = subprocess.Popen(
                ["scp", file, remote_url], stdout=subprocess.PIPE
            )
            pid, exit_code = os.waitpid(process.pid, 0)
            if exit_code != 0:
                print(f"Error {exit_code}: scp {file} {remote_url}")
    else:
        debug(f"SCP: could not connect to {remoteHost}")


# In[26]:


def setGlobalPlotSettings():
    debug()
    plt.style.use("seaborn-darkgrid")


params = {
    "figure.figsize": (15, 10),  # 15" x 10" (inch)
    "legend.fontsize": "x-large",
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "x-large",
    "ytick.labelsize": "x-large",
}

plt.rcParams.update(params)


# In[27]:


def setGlobalTimeStamps(days=None, timeStart=None, timeStop=None):
    """
    Set Start & End dates: 1 week back, until "now"
    """
    debug()

    global stdTimeStamp
    global stdTimeStampStr

    global stdTimeStart
    global stdTimeStop

    global stdDateToday
    global stdDateTodayNoon
    global stdDateTodayEvening

    # Capture 'Now' in TimeSamps and do Date calculations
    timeStamp = DT.datetime.utcnow()
    dateToday = timeStamp.date()

    stdTimeStampStr = timeStamp.strftime("%Y-%m-%d %H:%M")

    # Handle Days ago
    if days is None:
        days = stdDays
    dateDaysAgo = dateToday - DT.timedelta(days=days)
    dateTodayNoon = pd.to_datetime(dateToday, utc=True) + DT.timedelta(hours=12)
    dateTodayEvening = pd.to_datetime(dateToday, utc=True) + DT.timedelta(hours=18)
    dateTomorrow = dateToday + DT.timedelta(days=1)

    stdTimeStamp = pd.to_datetime(timeStamp, utc=True)

    stdDateToday = pd.to_datetime(dateToday, utc=True)
    stdDateTodayNoon = pd.to_datetime(dateTodayNoon, utc=True)
    stdDateTodayEvening = pd.to_datetime(dateTodayEvening, utc=True)

    # Handle Start and Stop Times
    if timeStart is None:
        timeStart = dateDaysAgo
    if timeStop is None:
        timeStop = dateTomorrow
    stdTimeStart = pd.to_datetime(timeStart, utc=True)
    stdTimeStop = pd.to_datetime(timeStop, utc=True)

    # verbose(f'stdTimeStart: {stdTimeStart}')
    # verbose(f'stdDateToday: {stdDateToday}')
    # verbose(f'stdDateTodayNoon: {stdDateTodayNoon}')
    # verbose(f'stdDateTodayEvening: {stdDateTodayEvening}')
    # verbose(f'stdTimeStop: {stdTimeStop}')

    # verbose(f'stdFileNameAddOn: {stdFileNameAddOn}')

    # verbose(f'stdTimeStamp: {stdTimeStamp}')


# In[28]:


def setGlobalStandardSettings(
    chop=None, fileNameAddOn=None,
):
    debug()

    global stdLocalHostName

    global stdDataProvider
    global stdFileBase
    global stdFileNameExtension

    global stdDays
    global stdFileNameAddOn

    global stdColorList
    global stdColorList_5_2
    global stdColorList_3322_10
    global stdXLabel
    global stdResampleTime

    global stdChop

    # Host Name
    stdLocalHostName = socket.gethostname()

    # File
    stdDataProvider = "XMM"
    stdFileBase = f"{stdDataProvider}_TM_Plot"
    stdFileNameExtension = "png"

    # Data
    stdDays = 7
    if fileNameAddOn is None:
        stdFileNameAddOn = "1w"
    else:
        stdFileNameAddOn = fileNameAddOn

    # Plot
    stdColorList = [
        "red",
        "blue",
        "green",
        "gold",
        "orangered",
        "cornflowerblue",
        "limegreen",
        "yellow",
    ]
    stdColorList_5_2 = [
        "red",
        "blue",
        "green",
        "gold",
        "indigo",
        "orangered",
        "cornflowerblue",
        "limegreen",
        "yellow",
        "blueviolet",
    ]
    stdColorList_3322_10 = [
        "red",
        "red",
        "red",
        "blue",
        "blue",
        "blue",
        "green",
        "green",
        "gold",
        "gold",
    ]
    stdXLabel = "DateTime"
    stdResampleTime = "40 s"

    # JSON
    if chop is None:
        stdChop = True
    else:
        stdChop = chop

    # INTEGRAL
    # INTEGRALAND
    # INTEGRALGRD
    # INTEGRALRT
    # INTEGRALRTGRD
    # Profiles
    # Scripts
    # XMM
    # XMMAND
    # XMMGRD


# In[29]:


def setGlobalScpSettings():
    debug()

    global paHost, paUser, paPath

    paHost = "xmm.esoc.esa.int"
    # remoteHost = '10.32.60.81'
    paUser = "webadmin"
    paPath = "/home/webadmin/htdocs/information/tm_plots/"


# In[30]:


def testConnection():
    """
    Test the connetion to the Parameter Archive
    """

    response = getFromMustDataProviders()

    if response:
        verbose("Have Must Link :-)")
    else:
        print("Error: No Must Link :-(")
        assert False
        exit()


# In[31]:


def setGlobalSettings():
    debug()

    readConfig()
    getEnviroment()
    installRequestCache()

    setGlobalStandardSettings()
    setGlobalTimeStamps()
    setGlobalTmNames()
    setGlobalScpSettings()
    setGlobalPlotSettings()

    testConnection()


# In[32]:


def setGlobalTmNames():

    # OPTIONAL: If you dont like the Descrition in WODB, overwrite it here

    debug()

    global tmName

    tmName["AD046"] = "SAS Roll Angle (AD046)"
    tmName["AD047"] = "SAS Pitch Angle (AD047)"
    tmName["AD065"] = "IMU Yaw Angle (AD065)"

    tmName["T6044"] = "THR 1A (T6044)"
    tmName["T6045"] = "THR 1B (T6045)"
    tmName["T6046"] = "THR 2A (T6046)"
    tmName["T6047"] = "THR 2B (T6047)"
    tmName["T6048"] = "THR 3A (T6048)"
    tmName["T6049"] = "THR 3B (T6049)"
    tmName["T6050"] = "THR 4A (T6050)"
    tmName["T6051"] = "THR 4B (T6051)"

    tmName["T6072"] = "Tank 1 TOP (T6072)"
    tmName["T6073"] = "Tank 1 EXT (T6073)"
    tmName["T6074"] = "Tank 2 TOP (T6074)"
    tmName["T6075"] = "Tank 2 EXT (T6075)"
    tmName["T6076"] = "Tank 3 TOP (T6076)"
    tmName["T6077"] = "Tank 3 EXT (T6077)"
    tmName["T6078"] = "Tank 4 EXT (T6078)"
    tmName["T6071"] = "Tank 4 TOP (T6071)"


# In[33]:


def doPlots(
    days=None, chop=None, fileNameAddOn=None, timeStart=None, timeStop=None,
):
    debug()

    # Supress Plots
    if forceQuickCheck:
        return

    setGlobalTimeStamps(
        days=days, timeStart=timeStart, timeStop=timeStop,
    )

    setGlobalStandardSettings(
        chop=chop, fileNameAddOn=fileNameAddOn,
    )

    # SVM near Tank 2
    response = linePlotTm(
        ["T6070", "T6003", "A5016"], fileNameBase="Tank2SVM", plotTitle="Tank 2 SVM",
    )
    verbose(f"{response}")

    # IMU Electric Box near Tank 2, 50 Ohm
    response = linePlotTm(
        ["T6009", "T6010", "T6011", "P1013"],
        fileNameBase="Tank2IMUE",
        plotTitle="Tank 2 IMU Electric Box",
    )
    verbose(f"{response}")

    ####################################################################

    # RCS Pipeworks @ Tank 1
    response = linePlotTm(
        ["T6030", "T6038", "T6042", "A5016"],
        y1Lim=(18, 48),
        fileNameBase="Tank1Pipe",
        plotTitle="Tank 1 Pipeworks Temperatures",
    )
    verbose(f"{response}")

    # RCS Pipeworks @ Tank 2
    response = linePlotTm(
        ["T6042", "T6031", "T6036", "T6039", "T6052", "T6053", "T6043", "A5016"],
        y1Lim=(18, 48),
        fileNameBase="Tank2Pipe",
        plotTitle="Tank 2 Pipeworks Temperatures",
    )
    verbose(f"{response}")

    # RCS Pipeworks @ Tank 3
    response = linePlotTm(
        ["T6043", "T6032", "T6034", "T6035", "T6037", "T6040", "T6054", "T6055", "A5016"],
        y1Lim=(18, 48),
        fileNameBase="Tank3Pipe",
        plotTitle="Tank 3 Pipeworks Temperatures",
    )
    verbose(f"{response}")

    # RCS Pipeworks @ Tank 4
    response = linePlotTm(
        ["T6055", "T6033", "T6041", "A5016"],
        y1Lim=(18, 48),
        fileNameBase="Tank4Pipe",
        plotTitle="Tank 4 Pipeworks Temperatures",
    )
    verbose(f"{response}")

    # Tank 1A
    response = linePlotTm(
        ["T6072", "T6073", "P1024", "T1000", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank1A",
        plotTitle="Tank 1A",
    )
    verbose(f"{response}")

    # Tank 1B
    response = linePlotTm(
        ["T6072", "T6073", "P1052", "T1024", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank1B",
        plotTitle="Tank 1B",
    )
    verbose(f"{response}")

    # Tank 1Boost
    response = linePlotTm(
        ["T6072", "T6073", "P1055", "T1046", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank1Boost",
        plotTitle="Tank 1Boost",
    )
    verbose(f"{response}")

    # Tank 2A
    response = linePlotTm(
        ["T6074", "T6075", "P1025", "T1006", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank2A",
        plotTitle="Tank 2A",
    )
    verbose(f"{response}")

    # Tank 2B
    response = linePlotTm(
        ["T6074", "T6075", "P1053", "T1030", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank2B",
        plotTitle="Tank 2B",
    )
    verbose(f"{response}")

    # Tank 3A
    response = linePlotTm(
        ["T6076", "T6077", "P1027", "T1018", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank3A",
        plotTitle="Tank 3A",
    )
    verbose(f"{response}")

    # Tank 3B
    response = linePlotTm(
        ["T6076", "T6077", "P1055", "T1042", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank3B",
        plotTitle="Tank 3B",
    )
    verbose(f"{response}")

    # Tank 4A
    response = linePlotTm(
        ["T6078", "T6071", "P1025", "T1007", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank4A",
        plotTitle="Tank 4A",
    )
    verbose(f"{response}")

    # Tank 4B
    response = linePlotTm(
        ["T6078", "T6071", "P1053", "T1031", "A5016"],
        y1Label="degC",
        y1Lim=(18, 36),
        y2Lim=(-1, 17),
        fileNameBase="Tank4B",
        plotTitle="Tank 4B",
    )
    verbose(f"{response}")

    # Plot Wheel Profile
    response = linePlotTm(
        ["AD001", "AD002", "AD003", "AD004"],
        fileNameBase="Wheels",
        plotTitle="Wheel Profile",
    )
    verbose(f"{response}")

    # Plot RCS Pressure
    response = linePlotTm(
        ["A9901", "A9902", "A9903"], fileNameBase="Pressure", plotTitle="RCS Pressure",
    )
    verbose(f"{response}")

    # Plot S/C Attitude
    response = linePlotTm(
        ["AD010", "AD009", "A5016"], fileNameBase="Attitude", plotTitle="S/C Attitude",
    )
    verbose(f"{response}")

    # Plot Thruster Tempertures
    response = linePlotTm(
        ["T6044", "T6046", "T6048", "T6050", "T6045", "T6047", "T6049", "T6051", "A5016"],
        fileNameBase="ThrusterTemp",
        plotTitle="Thruster Temperatures",
    )
    verbose(f"{response}")

    # Plot Thruster Tempertures 1 108,0
    response = linePlotTm(
        ["T6044", "T6045", "P1027", "T1019", "T1043", "A5016"],
        fileNameBase="Tank1ThrusterTemp",
        plotTitle="Tank 1 Thruster Temperatures",
    )
    verbose(f"{response}")

    # Plot Thruster Tempertures 2 107,4
    response = linePlotTm(
        ["T6046", "T6047", "P1025", "T1008", "T1032", "A5016"],
        fileNameBase="Tank2ThrusterTemp",
        plotTitle="Tank 2 Thruster Temperatures",
    )
    verbose(f"{response}")

    # Plot Thruster Tempertures 3 107,8
    response = linePlotTm(
        ["T6048", "T6049", "P1027", "T1020", "T1044", "A5016"],
        fileNameBase="Tank3ThrusterTemp",
        plotTitle="Tank 3 Thruster Temperatures",
    )
    verbose(f"{response}")

    # Plot Thruster Tempertures 4 107,9
    response = linePlotTm(
        ["T6050", "T6051", "P1027", "T1021", "T1045", "A5016"],
        fileNameBase="Tank4ThrusterTemp",
        plotTitle="Tank 4 Thruster Temperatures",
    )
    verbose(f"{response}")

    # Plot Mirror Support Platform Tempertures

    # MSP-1A
    response = linePlotTm(
        ["T2005", "T2037", "TD001", "T2105", "P4100", "A5016"],
        fileNameBase="MSP_1A",
        plotTitle="Tank 1A Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-2A
    response = linePlotTm(
        ["T2020", "T2012", "TD002", "T2104", "P4100", "A5016"],
        fileNameBase="MSP_2A",
        plotTitle="Tank 2A Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-3A
    response = linePlotTm(
        ["T2028", "T2013", "TD003", "T2103", "P4100", "A5016"],
        fileNameBase="MSP_3A",
        plotTitle="Tank 3A Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-4A
    response = linePlotTm(
        ["T2004", "T2045", "TD004", "T2102", "P4101", "A5016"],
        fileNameBase="MSP_4A",
        plotTitle="Tank 4A Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-5A
    response = linePlotTm(
        ["T2053", "T2061", "TD005", "T2101", "P4101", "A5016"],
        fileNameBase="MSP_5A",
        plotTitle="Tank 5A Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-6A
    response = linePlotTm(
        ["TD006", "T2100", "P4101", "A5016"],
        fileNameBase="MSP_6A",
        plotTitle="Tank 6A Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    """
        TSW1 T2005 T2037 T0012 MSP-1A MPS TD001 40 15 14	 44,2	1A	P4100
        TSW2 T2020 T2012 T0022 MSP-2A MPS TD002 40 70 69	 38,5	1A
        TSW3 T2028 T2013 T0032 MSP-3A MPS TD003 40 40 40	206,8	1A
        TSW4 T2004 T2045 T0042 MSP-4A MPS TD004 40 72 72	 61,4	2A	P4101
        TSW5 T2053 T2061 T0052 MSP-5A MPS TD005 40 37 37	 70,0	2A
        TSW6 'All'       T0062 MSP-6A MPS TD006			 22,8	2A
    """

    # MSP-1B
    response = linePlotTm(
        ["T2005", "T2037", "TD007", "T2129", "P4108", "A5016"],
        fileNameBase="MSP_1B",
        plotTitle="Tank 1B Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-2B
    response = linePlotTm(
        ["T2020", "T2012", "TD008", "T2128", "P4108", "A5016"],
        fileNameBase="MSP_2B",
        plotTitle="Tank 2B Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-3B
    response = linePlotTm(
        ["T2028", "T2013", "TD009", "T2127", "P4108", "A5016"],
        fileNameBase="MSP_3B",
        plotTitle="Tank 3B Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-4B
    response = linePlotTm(
        ["T2004", "T2045", "TD010", "T2126", "P4109", "A5016"],
        fileNameBase="MSP_4B",
        plotTitle="Tank 4B Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-5B
    response = linePlotTm(
        ["T2053", "T2061", "TD011", "T2125", "P4109", "A5016"],
        fileNameBase="MSP_5B",
        plotTitle="Tank 5B Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # MSP-6B
    response = linePlotTm(
        ["TD012", "T2124", "P4109", "A5016"],
        fileNameBase="MSP_6B",
        plotTitle="Tank 6B Mirror Support Platform (MSP)",
    )
    verbose(f"{response}")

    # Plot Mirror Support Platform Tempertures
    response = linePlotTm(
        [
            "T2045",
            "T2028",
            "T2013",
            "T2053",
            "T2061",
            "T2037",
            "T2005",
            "T2020",
            "T2012",
            "T2004", "A5016",
        ],
        fileNameBase="MSP_Temps",
        plotTitle="Mirror Support Platform (MSP) Temperatures",
        colorList=stdColorList_3322_10,
    )
    verbose(f"{response}")

    """
	'T2045' 1 'T2028' 1&OM 'T2013' 1&OM
	'T2053' 2 'T2061' 2 'T2037' 2
    	'T2005' 3 'T2020' 3
	'T2012' 4 'T2004' 4
    """

    # Tank 1 MSP
    response = linePlotTm(
        ["T2045", "T2028", "T2013", "A5016"],
        fileNameBase="Tank1_MSP",
        plotTitle="Tank 1 Mirror Support Platform (MSP) Temperatures",
    )
    verbose(f"{response}")

    # Tank 2 MSP
    response = linePlotTm(
        ["T2053", "T2061", "T2037", "A5016"],
        fileNameBase="Tank2_MSP",
        plotTitle="Tank 2 Mirror Support Platform (MSP) Temperatures",
    )
    verbose(f"{response}")

    # Tank 3 MSP
    response = linePlotTm(
        ["T2005", "T2020", "A5016"],
        fileNameBase="Tank3_MSP",
        plotTitle="Tank 3 Mirror Support Platform (MSP) Temperatures",
    )
    verbose(f"{response}")

    # Tank 4 MSP
    response = linePlotTm(
        ["T2012", "T2004", "A5016"],
        fileNameBase="Tank4_MSP",
        plotTitle="Tank 4 Mirror Support Platform (MSP) Temperatures",
    )
    verbose(f"{response}")

    # Plot Tank Tempertures
    response = linePlotTm(
        ["T6073", "T6074", "T6076", "T6078", "A5016"],
        y1Lim=(20, 35),
        fileNameBase="TankAll",
        plotTitle="Tank Temperatures",
    )
    verbose(f"{response}")


# In[36]:


def ptTwoYears():
    # PT 1, 2: two years

    VERBOSE = True
    DEBUG = False
    INSPECT = False
    TIMER = True

    # Plot RCS Pressure
    response = linePlotTm(
        ["A9901", "A9902"],
        fileNameBase="RCS Pressure 2y",
        plotTitle="RCS Pressure last 2 years",
        # timeStart = "2018-01-01 00:00:00",
        timeStart="2020-06-16 00:00:00",
        resampleTime=0,
        timeOut=stdTimeOutLong,
        chop=False,
    )
    verbose(f"{response}")


# In[41]:


def tank2Extra():
    doPlots(
        chop=False,
        fileNameAddOn="DOY193-195",
        timeStart="2020-07-11 00:00:00",
        timeStop="2020-07-13 23:59:59",
    )


def replWeeks():
    # Special Plots for Calendar Weeks (cw)

    # KW24
    doPlots(
        chop=False,
        fileNameAddOn="kw24",
        timeStart="2020-06-08 00:00:00",
        timeStop="2020-06-14 23:59:59",
    )

    # KW25
    doPlots(
        chop=False,
        fileNameAddOn="kw25",
        timeStart="2020-06-15 00:00:00",
        timeStop="2020-06-21 23:59:59",
    )

    # KW26
    doPlots(
        chop=False,
        fileNameAddOn="kw26",
        timeStart="2020-06-22 00:00:00",
        timeStop="2020-06-28 23:59:59",
    )


# In[44]:


def replDays():

    # 15
    doPlots(
        chop=False,
        fileNameAddOn="15",
        timeStart="2020-06-15 00:00:00",
        timeStop="2020-06-15 23:59:59",
    )

    # 16
    doPlots(
        chop=False,
        fileNameAddOn="16",
        timeStart="2020-06-16 00:00:00",
        timeStop="2020-06-16 23:59:59",
    )

    # 17
    doPlots(
        chop=False,
        fileNameAddOn="17",
        timeStart="2020-06-17 00:00:00",
        timeStop="2020-06-17 23:59:59",
    )

    # 18
    doPlots(
        chop=False,
        fileNameAddOn="18",
        timeStart="2020-06-18 00:00:00",
        timeStop="2020-06-18 23:59:59",
    )

    # 19
    doPlots(
        chop=False,
        fileNameAddOn="19",
        timeStart="2020-06-19 00:00:00",
        timeStop="2020-06-19 23:59:59",
    )

    # 20
    doPlots(
        chop=False,
        fileNameAddOn="20",
        timeStart="2020-06-20 00:00:00",
        timeStop="2020-06-20 23:59:59",
    )

    # 21
    doPlots(
        chop=False,
        fileNameAddOn="21",
        timeStart="2020-06-21 00:00:00",
        timeStop="2020-06-21 23:59:59",
    )


# In[35]:
# MAIN
def main():

    # Init
    setGlobalSettings()

    #### START PLOTTING
    t1_start = process_time()

    # Extra tank 2 plots
    # tank2Extra()

    # Now do the Standard 1 week Plots
    doPlots()

    # Additional 1 Day Plots
    doPlots(days=1, fileNameAddOn="1d")

    t1_stop = process_time()
    tmin, tsec = divmod((t1_stop - t1_start), 60)
    verbose(
        f"Elapsed time for data retrival and plotting in [min:sec]: {int(tmin)}:{int(tsec):02}"
    )

    #### STOP PLOTTING
    # SCP to Webserver
    scpFiles(remotePath="/home/webadmin/htdocs/information/sc_data/Replenishing/")


# MAIN ?
if __name__ == "__main__":
    main()
