# Copyright 2023 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

# Contact: Dougie Squire
# To run:
#     python mesh_from_hgrid.py hgrid_filename mask_filename mesh_filename
# in an environment with argparse, xarray, numpy and pandas 

import os
import subprocess
from datetime import datetime

import argparse
import xarray as xr
import numpy as np
import pandas as pd


def is_git_repo():
    """
    Return True/False depending on whether or not the current directory is a git repo.
    """
    
    return subprocess.call(
        ['git', '-C', '.', 'status'],
        stderr=subprocess.STDOUT,
        stdout = open(os.devnull, 'w')
    ) == 0

def git_info():
    """
    Return the git repo origin url, relative path to this file, and latest commit hash.
    """
    
    url = subprocess.check_output(
        ["git", "remote", "get-url", "origin"]
    ).decode('ascii').strip()
    top_level_dir = subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel']
    ).decode('ascii').strip()
    rel_path = os.path.relpath(__file__, top_level_dir)
    short_hash = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']
    ).decode('ascii').strip()

    return url, rel_path, short_hash
    

def mesh_from_hgrid(hgrid_filename, mask_filename, mesh_filename):
    """
    Create an ESMFMESH file from MOM hgrid and mask netcdf files.
    
    Parameters
    ----------
    hgrid_filename : str
        The path to the MOM hgrid file.
    mesh_filename : str
        The path to the mesh file to create.
    """
    
    hgrid = xr.open_dataset(hgrid_filename)
    mask = xr.open_dataset(mask_filename)
    
    x = hgrid.x.values
    y = hgrid.y.values
    area = hgrid.area.values

    # prep x corners
    ll = x[:-2:2, :-2:2]
    lr = x[:-2:2, 2::2]
    ul = x[2::2, :-2:2]
    ur = x[2::2, 2::2]

    # order: ll, lr, ur, ul
    x_corners = np.stack((ll.flatten(), lr.flatten(), ur.flatten(), ul.flatten()), axis=1).flatten()
    x_centres = x[1:-1:2, 1:-1:2].flatten()

    # prep y corners
    ll = y[:-2:2, :-2:2]
    lr = y[:-2:2, 2::2]
    ul = y[2::2, :-2:2]
    ur = y[2::2, 2::2]

    # order: ll, lr, ur, ul
    y_corners = np.stack((ll.flatten(), lr.flatten(), ur.flatten(), ul.flatten()), axis=1).flatten()
    y_centres = y[1:-1:2, 1:-1:2].flatten()

    # calculate element centres
    centres = np.stack((x_centres, y_centres), axis=1)

    corners_df = pd.DataFrame(
            {"x": x_corners, "y": y_corners}
        )

    # calculate indexes of corner nodes per element
    elem_conn = (
        corners_df.groupby(['x','y'], sort=False).ngroup()+1
    ).to_numpy().reshape((-1,4))

    # calculate corner nodes
    nodes = corners_df.drop_duplicates().to_numpy()

    # sum areas in elements
    area = np.lib.stride_tricks.sliding_window_view(
        area, 
        window_shape=(2,2)
    )[::2,::2].sum(axis=(-2,-1)).flatten()

    # process mask
    mask = mask["mask"].values.flatten()
    
    # create new dataset for output
    out = xr.Dataset()
    out['nodeCoords'] = xr.DataArray(
        nodes.astype(np.float64),
        dims=('nodeCount', 'coordDim'),
        attrs={'units': 'degrees'}
    )
    out['elementConn'] = xr.DataArray(
        elem_conn.astype(np.int32),
        dims=('elementCount', 'maxNodePElement'),
        attrs={'long_name': 'Node indices that define the element connectivity'}
    )
    out['numElementConn'] = xr.DataArray(
        4 * np.ones(x_centres.size, dtype=np.int32),
        dims=('elementCount'),
        attrs={'long_name': 'Number of nodes per element'}
    )
    out['centerCoords'] = xr.DataArray(
        centres.astype(np.float64),
        dims=('elementCount', 'coordDim'),
        attrs={'units': 'degrees'}
    )
    out["elementArea"] = xr.DataArray(
        area.astype(np.float64),
        dims=('elementCount'),
    )
    out["elementMask"] = xr.DataArray(
        mask.astype(np.int8),
        dims=('elementCount'),
    )

    # force no _FillValue (for now)
    for v in out.variables:
        if '_FillValue' not in out[v].encoding:
            out[v].encoding['_FillValue'] = None

    # add global attributes
    out.attrs = {
        "gridType" : "unstructured mesh",
        "inputFile": f"{hgrid_filename}, {mask_filename}",
        "timeGenerated": f"{datetime.now()}",
        "created_by": "Dougie Squire"
    }
    
    # add git info to history
    if is_git_repo():
        url, rel_path, short_hash = git_info()
        out.attrs["history"] = f"Created using commit {short_hash} of {rel_path} in {url}"

    # write output file
    out.to_netcdf(mesh_filename)
    
def main():
    parser = argparse.ArgumentParser(
        description="Create an ESMF mesh file from MOM hgrid and mask netcdf files."
    )
    parser.add_argument(
        "hgrid_filename",
        type=str,
        help="The path to the MOM hgrid supergrid file.",
    )
    parser.add_argument(
        "mask_filename",
        type=str,
        help="The path to the MOM mask file.",
    )
    parser.add_argument(
        "mesh_filename",
        type=str,
        help="The path to the mesh file to create.",
    )

    args = parser.parse_args()
    hgrid_filename = args.hgrid_filename
    mask_filename = args.mask_filename
    mesh_filename = args.mesh_filename
    
    mesh_from_hgrid(hgrid_filename, mask_filename, mesh_filename)
    
if __name__ == "__main__":
    main()
