#!/bin/bash
# patch for https://github.com/open-mpi/ompi/issues/12141
if ! [ -f work/GMOM_JRA.cice.r.* ] 
then 
# no restart files yet, use initial conditions
IC=$(readlink work/input/iced.1900-01-01-10800.nc)
rm work/input/iced.1900-01-01-10800.nc
cp $IC work/input/iced.1900-01-01-10800.nc
else
# change restart symlink to hardlink
RESTART=$(echo work/GMOM_JRA.cice.r.*)
ln -f $(readlink $RESTART) $RESTART
fi