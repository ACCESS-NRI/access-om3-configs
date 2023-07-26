# Copyright 2023 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

# Contact: Dougie Squire
# To run:
#     python generate_mesh.py --grid_type=<gridtype> --grid_filename=<grid_file> \
#         --mask_filename=<mask_file> --mesh_filename=<output_file>
# in an environment with argparse, xarray, numpy and pandas 

import os
import subprocess
from datetime import datetime

import argparse
import numpy as np
import xarray as xr
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
    hash = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']
    ).decode('ascii').strip()

    return url, rel_path, hash
    
    
class BaseGrid:

    def __init__(self, x_centres, y_centres, x_corners, y_corners, area=None, mask=None, inputs=None):
        """
        Initialise a mesh object

        Parameters
        ----------
        x_centres: len(elementCount) array-like
            Longitudinal positions of the element centre coords
        y_centres: len(elementCount) array-like
            Latitudinal positions of the element centre coords
        x_corners: (elementCount x 4) array-like
            Longitudinal positions of the corner nodes of each element, ordered ll, lr, ur, ul
        y_corners: (elementCount x 4) array-like
            LongitLatitudinaludinal positions of the corner nodes of each element, ordered ll, lr, ur, ul
        area: len(elementCount) array-like, optional
            Areas of each element
        mask: len(elementCount) array-like
            Mask values for each element, optional
        inputs: str or list of str, optional
            Paths to the files used to create the grid
        """
        
        self.x_centres = x_centres
        self.y_centres = y_centres

        self.x_corners = x_corners.flatten()
        self.y_corners = y_corners.flatten()
        
        self.area = area
        self.mask = mask

        if isinstance(inputs, str):
            inputs = [inputs]
        self.inputs = inputs

        self.mesh = None

    def create_mesh(self):
        """
        Create the mesh as an xarray Dataset
        """
        
        centres = np.stack((self.x_centres, self.y_centres), axis=1)
        corners_df = pd.DataFrame({"x": self.x_corners, "y": self.y_corners})
    
        # calculate indexes of corner nodes per element
        elem_conn = (
            corners_df.groupby(['x','y'], sort=False).ngroup()+1
        ).to_numpy().reshape((-1,4))
    
        # calculate corner nodes
        nodes = corners_df.drop_duplicates().to_numpy()
    
        # create mask if we don't have one
        if self.mask is None:
            self.mask = np.ones_like(self.x_centres, dtype=np.int8)
        
        # create a new dataset for the mesh
        ds = xr.Dataset()
        ds['nodeCoords'] = xr.DataArray(
            nodes.astype(np.float64),
            dims=('nodeCount', 'coordDim'),
            attrs={'units': 'degrees'}
        )
        ds['elementConn'] = xr.DataArray(
            elem_conn.astype(np.int32),
            dims=('elementCount', 'maxNodePElement'),
            attrs={'long_name': 'Node indices that define the element connectivity'}
        )
        ds['numElementConn'] = xr.DataArray(
            4 * np.ones_like(self.x_centres, dtype=np.int32),
            dims=('elementCount'),
            attrs={'long_name': 'Number of nodes per element'}
        )
        ds['centerCoords'] = xr.DataArray(
            centres.astype(np.float64),
            dims=('elementCount', 'coordDim'),
            attrs={'units': 'degrees'}
        )
        
        ds["elementMask"] = xr.DataArray(
            self.mask.astype(np.int8),
            dims=('elementCount'),
        )

        if self.area is not None:
            ds["elementArea"] = xr.DataArray(
                self.area.astype(np.float64),
                dims=('elementCount'),
            )
            
        # force no _FillValue (for now)
        for v in ds.variables:
            if '_FillValue' not in ds[v].encoding:
                ds[v].encoding['_FillValue'] = None
    
        # add global attributes
        ds.attrs = {
            "gridType" : "unstructured mesh",
            "timeGenerated": f"{datetime.now()}",
            "created_by": f"{os.environ.get('USER')}"
        }
        if self.inputs:
            ds.attrs["inputFile"] = ", ".join(self.inputs)

        # add git info to history
        if is_git_repo():
            url, rel_path, hash = git_info()
            ds.attrs["history"] = f"Created using commit {hash} of {rel_path} in {url}"

        self.mesh = ds
    
    def write(self, filename):
        """
        Save the mesh to a file
        """
        
        if self.mesh is None:
            self.create_mesh()
        
        self.mesh.to_netcdf(filename)


class MomSuperGrid(BaseGrid):

    def __init__(self, hgrid_filename, mask_filename=None):
        """
        Initialise a mesh representation of h-cells from a MOM supergrid

        Parameters
        ----------
        hgrid_filename: str
            Path to the MOM hgrid netcdf file
        mask_filename: str, optional
            Path to a netcdf file containing a mask corresponding to the MOM hgrid
        """
        
        grid = xr.open_dataset(hgrid_filename)
        inputs = [hgrid_filename]
        
        if mask_filename:
            mask = xr.open_dataset(mask_filename).mask.values.flatten()
            inputs += [mask_filename]
        else:
            mask = None
        
        # sum areas in elements
        area = grid.area.values
        area = (
            area[::2, ::2] + area[1::2, ::2] + area[1::2, 1::2] + area[::2, 1::2]
        ).flatten()

        x = grid.x.values
        y = grid.y.values
    
        # prep x corners
        ll = x[:-2:2, :-2:2]
        lr = x[:-2:2, 2::2]
        ul = x[2::2, :-2:2]
        ur = x[2::2, 2::2]
        x_corners = np.stack((ll.flatten(), lr.flatten(), ur.flatten(), ul.flatten()), axis=1)
        x_centres = x[1:-1:2, 1:-1:2].flatten()
    
        # prep y corners
        ll = y[:-2:2, :-2:2]
        lr = y[:-2:2, 2::2]
        ul = y[2::2, :-2:2]
        ur = y[2::2, 2::2]
        y_corners = np.stack((ll.flatten(), lr.flatten(), ur.flatten(), ul.flatten()), axis=1)
        y_centres = y[1:-1:2, 1:-1:2].flatten()

        super().__init__(
            x_centres=x_centres, 
            y_centres=y_centres, 
            x_corners=x_corners, 
            y_corners=y_corners, 
            area=area, 
            mask=mask,
            inputs=inputs,
        )


class LatLonGrid(BaseGrid):

    def __init__(self, grid_filename, mask_filename=None, lon_dim="lon", lat_dim="lat", area_var="area"):
        """
        Initialise a mesh representation from lat/lon locations

        Parameters
        ----------
        grid_filename: str
            Path to a netcdf file containing a lat/lon grid
        mask_filename: str, optional
            Path to a netcdf file containing a mask corresponding to the lat/lon grid
        lon_dim: str, optional
            The name of the longitude dimension
        lat_dim: str, optional
            The name of the latitude dimension
        area_var: str, optional
            The name of the area variable if one exists
        """

        grid = xr.open_dataset(grid_filename, chunks={})
        inputs = [grid_filename]
        
        if mask_filename:
            mask = xr.open_dataset(mask_filename).values.flatten()
            inputs += [mask_filename]
        else:
            mask = None
        
        if area_var in grid:
            area = grid[area_var].values.flatten()
        else:
            area = None

        x_centres = grid[lon_dim].values
        y_centres = grid[lat_dim].values

        has_lon_bounds = hasattr(grid[lon_dim], "bounds") and grid[lon_dim].bounds in grid
        has_lat_bounds = hasattr(grid[lat_dim], "bounds") and grid[lat_dim].bounds in grid
        
        if has_lon_bounds:
            lon_bnds = grid[getattr(grid[lon_dim], "bounds")]
            
            # flip and concat for ll, lr, ur, ul
            x_corners = np.concatenate([lon_bnds.values, lon_bnds[...,::-1].values], axis=-1)
        else:
            # Average neighbouring cells to get bounds
            ext = np.pad(x_centres, (1,),  mode='reflect', reflect_type='odd')
            bnds = (ext[:-1] + ext[1:]) / 2
            
            # stack as ll, lr, ur, ul
            x_corners = np.stack([bnds[:-1], bnds[1:], bnds[1:], bnds[:-1]], axis=1)
        
        if has_lat_bounds:
            lat_bnds = grid[getattr(grid[lat_dim], "bounds")]
            # repeat for ll, lr, ur, ul
            y_corners = np.repeat(lat_bnds.values, 2, axis=1)
        else:
            # Average neighbouring cells to get bounds
            ext = np.pad(y_centres, (1,),  mode='reflect', reflect_type='odd')
            bnds = (ext[:-1] + ext[1:]) / 2
            
            # stack as ll, lr, ur, ul
            y_corners = np.stack([bnds[:-1], bnds[:-1], bnds[1:], bnds[1:]], axis=1)
        
        # broadcast corners
        x_corners, y_corners = np.broadcast_arrays(
            np.expand_dims(x_corners, axis=0), 
            np.expand_dims(y_corners, axis=1)
        )
        x_corners = x_corners.reshape(-1, 4)
        y_corners = y_corners.reshape(-1, 4)
        
        # broadcast centres
        x_centres, y_centres = np.broadcast_arrays(
            np.expand_dims(x_centres, axis=0), 
            np.expand_dims(y_centres, axis=1)
        )
        x_centres = x_centres.flatten()
        y_centres = y_centres.flatten()

        super().__init__(
            x_centres=x_centres, 
            y_centres=y_centres, 
            x_corners=x_corners, 
            y_corners=y_corners, 
            area=area, 
            mask=mask,
            inputs=inputs,
        )

gridtype_dispatch = {
    "latlon": LatLonGrid,
    "mom": MomSuperGrid,
}
            
def main():
    parser = argparse.ArgumentParser(
        description="Create an ESMF mesh file from a grid in a netcdf file."
    )

    parser.add_argument(
        "--grid_type",
        choices=gridtype_dispatch.keys(),
        required=True,
        help='The type of grid in the netcdf file.', 
    )
    parser.add_argument(
        "--grid_filename",
        type=str,
        required=True,
        help="The path to the netcdf file specifying the grid.", 
    )
    parser.add_argument(
        "--mask_filename",
        type=str,
        default=None,
        help="The path to a netcdf file specifying the mask.",
    )
    parser.add_argument(
        "--mesh_filename",
        type=str,
        required=True,
        help="The path to the mesh file to create.", 
    )

    args = parser.parse_args()
    grid_type = args.grid_type
    grid_filename = args.grid_filename
    mask_filename = args.mask_filename
    mesh_filename = args.mesh_filename

    mesh = gridtype_dispatch[grid_type](grid_filename, mask_filename)
    mesh.write(mesh_filename)
    
if __name__ == "__main__":
    main()
