# -----------------------------------------------------------------------------
# Name:        datatypes.py (part of PyGMI)
#
# Author:      Patrick Cole
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2013 Council for Geoscience
# Licence:     GPL-3.0
#
# This file is part of PyGMI
#
# PyGMI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyGMI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
"""Module for vector data types."""

import numpy as np


class PData():
    """
    Class for point data.

    Attributes
    ----------
    xdata : numpy array
        array of x coordinates
    ydata : numpy array
        array of y coordinates
    zdata : numpy array
        array of z coordinates
    dataid : str
        data description
    """

    def __init__(self):
        self.xdata = np.array([])
        self.ydata = np.array([])
        self.zdata = np.array([])
        self.dataid = ''


class LData():
    """
    Class for line data.

    Attributes
    ----------
    xchannel : string
        channel for x coordinates
    ychannel : string
        channel for y coordinates
    zchannel : string
        channel for z coordinates
    data : dictionary
        dictionary of groups/lines, each having a structured array of data
    dataid : str
        data description
    nullvalue : int
        Nullvalue used in data.
    """

    def __init__(self):
        self.xchannel = ''
        self.ychannel = ''
        self.zchannel = ''
        self.data = {}
        self.dataid = ''
        self.nullvalue = -99999


class VData():
    """
    Class for Vector data. Typically used for storage of shape files.

    Attributes
    ----------
    crds : list
        List of coordinates
    attrib : list
        list of dictionaries, where each dictionary is the column in a table
    dataid : str
        data description
    dtype : str
        type of data - Line, Point, Poly
    """

    def __init__(self):
        # Since each line can have variable amount of points, it is best to
        # store in a list
        self.crds = []
        self.attrib = [{}]
        self.dataid = ''
        self.dtype = ''


def line_to_point(ldata):
    """
    Convert LData to PData

    Parameters
    ----------
    ldata : LData
        Line data type.

    Returns
    -------
    pdata : PData.
        Point data type

    """

    tmp = {}
    pdata = []

    for i in ldata.data:
        for j in ldata.data[i].dtype.names:
            if j == ldata.xchannel or j == ldata.ychannel:
                continue
            if j not in tmp:
                tmp[j] = PData()
                tmp[j].dataid = j
            tmp[j].xdata = np.append(tmp[j].xdata,
                                     ldata.data[i][ldata.xchannel])
            tmp[j].ydata = np.append(tmp[j].ydata,
                                     ldata.data[i][ldata.ychannel])
            tmp[j].zdata = np.append(tmp[j].zdata, ldata.data[i][j])

    for i in tmp:
        pdata.append(tmp[i])

    return pdata