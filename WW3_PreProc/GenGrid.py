#!/usr/bin/env python3
"""
WWIII Grid Generation Script

This script generates a grid from OM2 Ocean_hgrid and topog files for use with the WAVEWATCH III (WW3) model.
It is adapted from Shou Li's config and modified to work with the current version of WW3 in access-OM3.

Author: Ezhilsabareesh Kannadasan

Usage:
    ./GenGrid.py

Input: ocean_hgrid.nc, topog.nc
Output: dat files containing Lat, Lon, Mask and Obstruction grid

"""

import numpy as np
import netCDF4 as NC

grid_handle = NC.Dataset('/g/data/ik11/inputs/access-om3/0.x.0/1deg/mom/ocean_hgrid.nc', mode='r')
topog_handle = NC.Dataset('/g/data/ik11/inputs/access-om3/0.x.0/1deg/share/topog.nc', mode='r')

# Read in Grid
Lon = grid_handle.variables['x'][:, :]
Lat = grid_handle.variables['y'][:, :]
H_DPT = topog_handle.variables['depth'][:, :]

# Convert the data to a NumPy array
H_DPT = np.array(H_DPT)

# Replace masked values with zeros
H_DPT[H_DPT == -9999.0] = 0.0

print(np.shape(H_DPT))

H_MSK6 = np.ones(np.shape(H_DPT))

H_LAT = np.zeros(np.shape(H_DPT))
H_LON = np.zeros(np.shape(H_DPT))

H_LAT = Lat[1::2, 1::2]
H_LON = Lon[1::2, 1::2]

LLAT = len(H_LAT[:, 0])
LLON = len(H_LAT[0, :])

GRIDNAME = 'OM2_1'

with open(GRIDNAME + '.Mask', 'w') as f6, open(GRIDNAME + '.Dpt', 'w') as f7, open(GRIDNAME + '.Obstr', 'w') as f9, open(
        GRIDNAME + '.Lat', 'w') as f10, open(GRIDNAME + '.Lon', 'w') as f11:
    for ii in np.arange(0, LLAT):
        for jj in np.arange(0, LLON):
            f6.write(str(int(H_MSK6[ii,jj]))+' ')
            f7.write(str(-abs(H_DPT[ii,jj]))+' ')
            f9.write(str(0)+' ')
            f10.write(format(H_LAT[ii, jj], '.7e') + '   ')
            f11.write(format(H_LON[ii, jj], '.7e') + '   ')
        f6.write('\n')
        f7.write('\n')
        f9.write('\n')
        f10.write('\n')
        f10.write('   ')
        f11.write('\n')
        f11.write('   ')

    for ii in np.arange(0,LLAT):
        for jj in np.arange(0, LLON):
            f9.write(str(0) + ' ')
        f9.write('\n')

# Close the files
f6.close()
f7.close()
f9.close()
f10.close()
f11.close()

